from django.contrib import admin
from .models import *

admin.site.register(DefProduit)
admin.site.register(Option)
admin.site.register(Client)
admin.site.register(FinProduit)
admin.site.register(Panier)
admin.site.register(CarteBancaire)

