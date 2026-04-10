from django import forms
from django.contrib import admin
from django.utils import timezone # <--- Módulo de tempo do Django para o agendamento
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Contato, Campanha, ConfiguracaoSMTP
from .tasks import disparar_campanha_task

# --- NOVA LÓGICA DE IMPORTAÇÃO/EXPORTAÇÃO (PLANILHAS) ---
class ContatoResource(resources.ModelResource):
    class Meta:
        model = Contato
        fields = ('id', 'nome', 'email', 'categoria', 'ativo')
        import_id_fields = ['email'] 

# --- FORMULÁRIO DE SEGURANÇA PARA O SMTP ---
class ConfiguracaoSMTPForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoSMTP
        fields = '__all__'
        widgets = {
            'senha': forms.PasswordInput(render_value=True, attrs={'placeholder': 'Digite a senha do e-mail'}),
        }

# --- CONFIGURAÇÃO DO PAINEL DE CONTATOS ---
@admin.register(Contato)
class ContatoAdmin(ImportExportModelAdmin): 
    resource_class = ContatoResource        
    list_display = ('nome', 'email', 'categoria', 'ativo', 'data_cadastro')
    list_filter = ('ativo', 'categoria', 'data_cadastro')
    search_fields = ('nome', 'email')
    list_editable = ('ativo',) 

# --- CONFIGURAÇÃO DO PAINEL DE CAMPANHAS ---
@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    # Adicionamos 'data_agendamento' aqui para você visualizar direto na tabela
    list_display = ('assunto', 'remetente', 'data_agendamento', 'data_criacao', 'enviada')
    list_filter = ('enviada', 'remetente')
    filter_horizontal = ('destinatarios',) 
    
    # Atualizamos o nome da Action para ficar mais claro
    actions = ['disparar_emails']

    @admin.action(description='🚀 Disparar / Agendar Campanha(s) Selecionada(s)')
    def disparar_emails(self, request, queryset):
        for campanha in queryset:
            if not campanha.remetente:
                self.message_user(
                    request, 
                    f"ERRO: A campanha '{campanha.assunto}' não tem um remetente definido!", 
                    level='error'
                )
                continue

            # --- A MÁGICA DO ETA (AGENDAMENTO) ---
            if campanha.data_agendamento and campanha.data_agendamento > timezone.now():
                # Se tem data futura, avisa o Celery para aguardar até lá
                disparar_campanha_task.apply_async(args=[campanha.id], eta=campanha.data_agendamento)
                msg = "agendadas para disparo"
            else:
                # Se não tem data (ou já passou), dispara na hora
                disparar_campanha_task.delay(campanha.id)
                msg = "enviadas para a fila"
            
            campanha.enviada = False # Reset para processamento
            campanha.save()
                
        self.message_user(request, f"Campanhas {msg} com sucesso!")

# --- CONFIGURAÇÃO DO PAINEL SMTP ---
@admin.register(ConfiguracaoSMTP)
class ConfiguracaoSMTPAdmin(admin.ModelAdmin):
    form = ConfiguracaoSMTPForm 
    list_display = ('nome_identificador', 'usuario', 'servidor', 'porta')