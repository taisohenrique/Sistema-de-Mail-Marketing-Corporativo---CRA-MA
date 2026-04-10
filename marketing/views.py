from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Cria o usuário, mas ainda não salva no banco
            user = form.save(commit=False)
            
            # ATENÇÃO: Como o seu sistema roda dentro do painel /admin, 
            # o usuário precisa da flag "is_staff" para conseguir logar lá.
            user.is_staff = True 
            user.save()
            
            messages.success(request, 'Conta criada com sucesso! Agora você pode fazer o login.')
            return redirect('login') # Redireciona para a tela de login
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/registrar.html', {'form': form})
# Create your views here.

from django.core import signing # Biblioteca de criptografia do Django
from django.http import HttpResponse
from .models import Contato # Precisamos importar o modelo Contato no topo!

# ... (Mantenha sua função registrar() aqui em cima) ...

def descadastrar(request, token):
    try:
        # Descriptografa o token de volta para o ID do contato
        contato_id = signing.loads(token)
        contato = Contato.objects.get(id=contato_id)
        
        # Desativa o contato
        contato.ativo = False
        contato.save()
        
        # Uma tela simples de confirmação
        html = """
        <div style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h2 style="color: #4CAF50;">Descadastro realizado com sucesso.</h2>
            <p>Você não receberá mais as campanhas do CRA-MA.</p>
        </div>
        """
        return HttpResponse(html)
        
    except (signing.BadSignature, Contato.DoesNotExist):
        return HttpResponse("<h2 style='text-align: center; color: red; margin-top: 50px;'>Link inválido ou expirado.</h2>")