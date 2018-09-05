# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import *
from .tokens import account_activation_token
from .models import *

class Login(LoginView):
    True

def logout_view(request):
    logout(request)
    return redirect('/')

def tobecontinued(request):
    return render(request, 'tobecontinued/tobecontinued.html')

class ProduitList(TemplateView):

    #returns a list of the categories of products

    template_name = 'mainapp/main.html'    
    def c(self):
        return set(DefProduit.objects.values_list('categorie', flat=True).reverse())
             
def categorie(request, categorie):
    
    #returns a list of products for each category
    
    return render(request, 'mainapp/liste_produit.html', 
        {'product_list': DefProduit.objects.filter(categorie=categorie),
         'categorie': categorie})

def produit(request, categorie, produit):    
    if request.method == 'POST':
        finproduitform = FinProduitForm(request.POST)
        if finproduitform.is_valid():
            #if a final product with the same product already exists
            if FinProduit.objects.filter(finprod=finproduitform.cleaned_data['finprod']):
                for produit in FinProduit.objects.filter(finprod=finproduitform.cleaned_data['finprod']):
                    # if it has the same options
                    if produit.finopt.all() == finproduitform.cleaned_data['finopt']:
                        # if it has the same quantity, this final product instance is keeped
                        # to increase the quantity
                        if produit.quantite == finproduitform.cleaned_data['quantite']:
                            instance = produit
                        # otherwise a new instance is saved to increase the quantity
                        else:
                            finproduitform.save(commit=False)
                            finproduitform.save()
                            finproduitform.save_m2m()
                            instance = finproduitform.instance
                    # otherwise a new instance is saved for the new final product
                    else:
                        finproduitform.save(commit=False)
                        finproduitform.save()
                        finproduitform.save_m2m()
                        instance = finproduitform.instance    
            # otherwise a new instance is saved for the new final product     
            else:
                finproduitform.save(commit=False)
                finproduitform.save()
                finproduitform.save_m2m()
                instance = finproduitform.instance   

            if request.user.is_authenticated:
                if not Panier.objects.filter(IP=request.META.get('REMOTE_ADDR'), client=request.user):
                    # if the user is authenticated and created a cart when he wasn't,
                    # this cart is attributed to his user instance
                    Panier.objects.filter(IP=request.META.get('REMOTE_ADDR')).update(client=request.user)
                # otherwise a cart is getted or created and the retreived instance from the form is added
                Panier.objects.get_or_create(IP=request.META.get('REMOTE_ADDR'), client=request.user)[0].add_item(instance)
            # otherwise a cart is getted or created and the retreived instance from the form is added
            # is the user isn't authenticated his IP adress is used to create his cart
            else:
                Panier.objects.get_or_create(IP=request.META.get('REMOTE_ADDR'), client=None)[0].add_item(instance)
            return redirect('panier')
    return render(request, 'mainapp/produit.html', {'produit': DefProduit.objects.get(produit=produit),
                                                 'options': Option.objects.all()})

def panier(request):

    """
    This view handles two situation:
        -if the user has a cart without being logged and then logged,
        his previous cart is attributed to his user instance
        (anonymous cart => client cart)
        -if he is logged and has a cart, then unlogged and add new items,
        and the logged, all his items are fusioned in the same cart
        (client cart => anonymous cart => client cart)
    """

    if request.user.is_authenticated:
        if not Panier.objects.filter(IP=request.META.get('REMOTE_ADDR'), client=request.user):
            Panier.objects.filter(IP=request.META.get('REMOTE_ADDR')).update(client=request.user)
        elif len(Panier.objects.filter(IP=request.META.get('REMOTE_ADDR'))) > 1:
            Panier.objects.get(IP=request.META.get('REMOTE_ADDR'), client=request.user).commande.set(list(Panier.objects.get(IP=request.META.get('REMOTE_ADDR'), client=None).commande.all())
                                                                                                     + list(Panier.objects.get(IP=request.META.get('REMOTE_ADDR'), client=request.user).commande.all()))
            Panier.objects.get(IP=request.META.get('REMOTE_ADDR'), client=None).delete()
        panier = get_object_or_404(Panier, client=request.user).commande.all()
        total = get_object_or_404(Panier, client=request.user).total_prix
        hors_taxes = get_object_or_404(Panier, client=request.user).hors_taxes
    else:
        panier = get_object_or_404(Panier, IP=request.META.get('REMOTE_ADDR'), client=None).commande.all()
        total = get_object_or_404(Panier, IP=request.META.get('REMOTE_ADDR'), client=None).total_prix
        hors_taxes = get_object_or_404(Panier, IP=request.META.get('REMOTE_ADDR'), client=None).hors_taxes   
    if request.method == 'POST':
        FinProduit.objects.filter(pk=request.POST.get('pk')).update(quantite=request.POST.get('quantite'))
        return redirect('panier')
    return render(request, 'mainapp/panier.html', {'panier': panier,
                                                'total': total,
                                                'hors_taxes': hors_taxes})

class DeleteItem(DeleteView):
    def get_queryset(self):
        return FinProduit.objects.filter(id=self.kwargs['pk'])
    success_url = reverse_lazy('panier')
    
def clientformview(request):
    if request.method == 'POST':
        clientform = ClientForm(request.POST)
        if clientform.is_valid():
            client = clientform.save(commit=False)
            client.user = request.user
            client.save()
    else:
        clientform = ClientForm()
    return render(request, 'mainapp/clientform.html', {'clientform':clientform})

def cartebancaireformview(request):
    if request.method == 'POST':
        cartebancaireform = CarteBancaireForm(request.POST)
        if cartebancaireform.is_valid():
            carte = cartebancaireform.save(commit=False)
            carte.user = request.user
            carte.save()
    else:
        cartebancaireform = CarteBancaireForm()
    return render(request, 'mainapp/cartebancaireform.html', {'cartebancaireform':cartebancaireform})
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form,form.is_valid(),form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your mainapp Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.client.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('main')
    else:
        return render(request, 'registration/account_activation_invalid.html')
    
def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

