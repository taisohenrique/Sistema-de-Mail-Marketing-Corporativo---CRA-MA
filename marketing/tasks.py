from celery import shared_task
import time
from .models import Contato, Campanha, ConfiguracaoSMTP
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core import signing # <--- Importação da criptografia do Django

@shared_task
def disparar_campanha_task(campanha_id):
    try:
        # 1. Busca a campanha e o remetente vinculado a ela
        campanha = Campanha.objects.get(id=campanha_id)
        config = campanha.remetente 
        
        if not config:
            return f"Erro: A campanha '{campanha.assunto}' não possui um remetente configurado."

    except Campanha.DoesNotExist:
        return "Erro: Campanha não encontrada."

    # 2. Lógica Inteligente de Destinatários
    if campanha.destinatarios.exists():
        contatos = campanha.destinatarios.filter(ativo=True)
    else:
        contatos = Contato.objects.filter(ativo=True)

    if not contatos.exists():
        return "Nenhum contato ativo encontrado para esta campanha."

    sucessos = 0
    erros = 0

    try:
        # 3. Abre a conexão usando as credenciais do remetente
        conexao = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=config.servidor,
            port=config.porta,
            username=config.usuario,
            password=config.senha,
            use_ssl=True if config.porta == 465 else False,
            use_tls=True if config.porta in [587, 25] else False,
        )
        conexao.open() 
        
    except Exception as e:
        return f"Erro ao conectar no servidor {config.nome_identificador}: {str(e)}"

    # 4. Loop de envio com proteção e Link de Opt-out automático
    for contato in contatos:
        try:
            # --- INÍCIO DA MÁGICA DO DESCADASTRO ---
            # Gera um token seguro e invisível com o ID do contato
            token = signing.dumps(contato.id)
            
            # ATENÇÃO: Link apontando para o seu ambiente local (localhost)
            link_optout = f"http://localhost:8000/descadastrar/{token}/"
            
            # Cria o rodapé com o link formatado
            rodape_html = f"""
            <br><br><hr style="border: 0; border-top: 1px solid #eee; margin-top: 20px;">
            <p style="font-size: 11px; color: #888; text-align: center; font-family: sans-serif;">
                Você está recebendo este e-mail porque está cadastrado em nossa base do CRA-MA.<br>
                Se não deseja mais receber nossos informativos, <a href="{link_optout}" style="color: #4db8ff; text-decoration: none;">clique aqui para se descadastrar</a>.
            </p>
            """
            
            # Junta o e-mail que você escreveu no painel com o rodapé automático
            corpo_final_html = campanha.corpo_html + rodape_html
            texto_puro_final = strip_tags(corpo_final_html) # O texto puro também vai com o link agora
            # --- FIM DA MÁGICA ---

            email = EmailMultiAlternatives(
                subject=campanha.assunto,
                body=texto_puro_final,
                from_email=f"CRA-MA <{config.usuario}>",
                to=[contato.email],
                connection=conexao
            )
            email.attach_alternative(corpo_final_html, "text/html")
            email.send()
            sucessos += 1
            
        except Exception as e:
            erros += 1
            print(f"Falha ao enviar para {contato.email} via {config.usuario}: {str(e)}")
            
        time.sleep(2) 
            
    conexao.close()
    
    # Marca como enviada apenas se pelo menos um e-mail saiu com sucesso
    if sucessos > 0:
        campanha.enviada = True
        campanha.save()
    
    return f"Relatório: {sucessos} sucessos, {erros} falhas. Remetente: {config.usuario}"