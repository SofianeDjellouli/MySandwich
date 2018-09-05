from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from mainapp.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProduitList.as_view(), name = 'main'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('panier/', panier, name = 'panier'),
    path('<int:pk>', DeleteItem.as_view(), name = 'delete'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name = 'login'),
    path('logout/', logout_view, name = 'logout'),
    path('infos/', clientformview, name = 'clientformview'),
    path('carte/', cartebancaireformview, name = 'cartebancaireformview'),
    path('signup/', signup, name = 'signup'),
    path('tobecontinued/', tobecontinued, name = 'tobecontinued'),
    path('account_activation_sent', account_activation_sent, name='account_activation_sent'),
    re_path(r'^(?P<categorie>[\w.@+-]+)/$', categorie, name = 'categorie'),
    re_path(r'^(?P<categorie>[\w.@+-]+)/(?P<produit>[\w.@+-]+)/$', produit, name = 'produit'),    
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),    
]
