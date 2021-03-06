# Generated by Django 2.0.4 on 2018-05-15 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=100)),
                ('adresse', models.CharField(blank=True, max_length=200)),
                ('code_postal', models.CharField(blank=True, max_length=10)),
                ('ville', models.CharField(blank=True, max_length=5)),
                ('tel', models.CharField(blank=True, max_length=20)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DefProduit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorie', models.CharField(max_length=100)),
                ('produit', models.CharField(max_length=100)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='FinProduit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('nom', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP', models.CharField(max_length=50, null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('commande', models.ManyToManyField(to='mainapp.FinProduit')),
            ],
        ),
        migrations.CreateModel(
            name='Quantite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='finproduit',
            name='finopt',
            field=models.ManyToManyField(to='mainapp.Option'),
        ),
        migrations.AddField(
            model_name='finproduit',
            name='finprod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.DefProduit'),
        ),
        migrations.AddField(
            model_name='finproduit',
            name='finqte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Quantite'),
        ),
    ]
