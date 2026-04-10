from django.db import models
from tinymce.models import HTMLField

class Contato(models.Model):
    CATEGORIAS = [
        ('adm', 'Administrador'),
        ('est', 'Estudante'),
        ('emp', 'Empresa'),
        ('ger', 'Geral'),
    ]
    
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    categoria = models.CharField(max_length=3, choices=CATEGORIAS, default='ger')
    ativo = models.BooleanField(default=True, help_text="Desmarque se o usuário pedir para sair (opt-out)")
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.email} ({self.get_categoria_display()})"

class ConfiguracaoSMTP(models.Model):
    nome_identificador = models.CharField(max_length=100, help_text="Ex: Suporte, Financeiro, Marketing")
    servidor = models.CharField(max_length=200, default='mail.cra-ma.org.br')
    porta = models.IntegerField(default=465)
    usuario = models.EmailField(help_text="E-mail que fará os envios")
    senha = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Configuração SMTP"
        verbose_name_plural = "Configurações SMTP"

    def __str__(self):
        return f"{self.nome_identificador} ({self.usuario})"

class Campanha(models.Model):
    assunto = models.CharField(max_length=255)
    corpo_html = HTMLField(help_text="Use o editor visual para formatar seu e-mail")
    
    remetente = models.ForeignKey(ConfiguracaoSMTP, on_delete=models.PROTECT, null=True, verbose_name="Enviar através de")
    destinatarios = models.ManyToManyField(Contato, blank=True, help_text="Selecione contatos específicos ou deixe vazio para enviar a todos os ativos.")

    # Campo de agendamento adicionado com sucesso!
    data_agendamento = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="Deixe em branco para disparar imediatamente, ou defina uma data para agendar."
    )
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    enviada = models.BooleanField(default=False)

    def __str__(self):
        return self.assunto