from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.urls import reverse
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver


class DefProduit(models.Model):
    categorie = models.CharField(max_length=100)
    produit = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return '{} {}'.format(self.categorie, self.produit)


class Option(models.Model): 
    type = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    
    def __str__(self):
        return '{} {}'.format(self.type, self.nom)


class FinProduit(models.Model):

    # This model attaches several options and a quantity to each product

    finprod = models.ForeignKey(DefProduit, on_delete=models.CASCADE)
    finopt = models.ManyToManyField(Option, blank=True)
    quantite = models.IntegerField(default=1)

    @property
    def subtotal(self):
        return self.finprod.prix * self.quantite
    
    def __str__(self):
        return '{} {} {}'.format(self.quantite, self.finprod.produit, self.finopt.all())    


class Panier(models.Model):

    # Each cart has a user and several final products. 
    # We use IP to retrieve clients that aren't logged.

    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    commande = models.ManyToManyField(FinProduit)
    IP = models.CharField(max_length=50, null=True)
    
    @property
    def total_prix(self):
        return sum([finproduit.finprod.prix * finproduit.quantite for finproduit in self.commande.all()])
    
    @property
    def hors_taxes(self):
        return round(sum([sum([finproduit.quantite * finproduit.finprod.prix / Decimal(1.055) for finproduit in self.commande.all() if finproduit.finprod.categorie == 'Boisson']),
            sum([finproduit.quantite * finproduit.finprod.prix / Decimal(1.1) for finproduit in self.commande.all() if finproduit.finprod.categorie != 'Boisson'])]), 2)        

    def add_item(self, item):
        
        # if the final product is already in the cart, increment its number
        # otherwise, add it to the commande

        if self.commande.filter(finprod=item.finprod):
            for produit in self.commande.filter(finprod=item.finprod):
                if list(produit.finopt.all()) == list(item.finopt.all()):
                    produit.quantite += item.quantite
                    produit.save()
                else:
                    self.commande.add(item)
        else:
            self.commande.add(item)
    
    def __str__(self):
        return '{} {}'.format(self.id, self.client)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_complet = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=5)
    tel = models.CharField(max_length=20)
    email_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return '{} client'.format(self.user.username)


class CarteBancaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    numero = models.IntegerField()
    date = models.IntegerField()
    code = models.IntegerField()


# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Client.objects.create(user=instance)
#     instance.client.save()