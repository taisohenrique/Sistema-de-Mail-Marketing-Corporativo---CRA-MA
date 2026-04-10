from django.contrib import admin
from django.urls import path, include
from marketing import views # Importamos a visualização que vamos criar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    # Rotas de Autenticação nativas do Django (Login, Logout, Senha)
    path('contas/', include('django.contrib.auth.urls')), 
    # rota customizada para criar conta
    path('registrar/', views.registrar, name='registrar'), 
    path('descadastrar/<str:token>/', views.descadastrar, name='descadastrar'),
]