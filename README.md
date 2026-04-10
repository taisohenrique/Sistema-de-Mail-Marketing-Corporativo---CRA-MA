Sistema de Mail Marketing Corporativo - CRA-MA

![Status do Projeto](https://img.shields.io/badge/status-ativo-brightgreen)
![Django](https://img.shields.io/badge/Django-5.0+-092e20?logo=django)
![Docker](https://img.shields.io/badge/Docker-Integrado-2496ed?logo=docker)

Esta plataforma foi desenvolvida para o **Conselho Regional de Administração do Maranhão (CRA-MA)** com o objetivo de centralizar e automatizar o envio de e-mails institucionais, garantindo conformidade com a LGPD e alta performance de disparo.


## Funcionalidades Principais

* **Editor Visual (WYSIWYG):** Criação de e-mails com HTML rico diretamente no painel.
* **Agendamento Inteligente (ETA):** Programação de disparos para datas e horas futuras.
* **Importação em Massa:** Suporte a planilhas Excel e CSV para gestão de contatos.
* **Multi-SMTP:** Configuração de múltiplos servidores de saída para diferentes departamentos.
* **Sistema de Opt-out:** Links de descadastro automáticos e criptografados.

##  Stack Tecnológica

O sistema utiliza uma arquitetura moderna e escalável baseada em micro-serviços:

* **Linguagem:** Python 3.11+
* **Web Framework:** Django
* **Banco de Dados:** PostgreSQL
* **Fila de Processamento:** Celery + Redis
* **Orquestração:** Docker & Docker Compose
* **Interface:** Design customizado "Dark Tech" para o CRA-MA


##  Arquitetura do Sistema

O sistema separa a interface de usuário do processo de envio para evitar travamentos.



1.  **Django (Web):** Recebe as ordens de disparo.
2.  **Redis (Message Broker):** Armazena os e-mails na fila.
3.  **Celery (Worker):** Retira os e-mails da fila e envia um por um.
4.  **SMTP:** O servidor final que entrega a mensagem ao destinatário.


##  Como Executar o Projeto

### Pré-requisitos
* Docker e Docker Compose instalados.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/taisohenrique/Sistema-de-Mail-Marketing-Corporativo---CRA-MA.git](https://github.com/taisohenrique/Sistema-de-Mail-Marketing-Corporativo---CRA-MA.git)
   cd Sistema-de-Mail-Marketing-Corporativo---CRA-MA
Configure as variáveis de ambiente:

Crie um arquivo .env na raiz baseado no .env.example.

Insira sua SECRET_KEY e credenciais do banco.

Suba os containers:

Bash
docker-compose up -d --build
Aplique as migrações e crie o admin:

Bash
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py createsuperuser
O sistema estará disponível em: http://localhost:8000/admin

Conformidade LGPD
O sistema foi construído pensando na privacidade. Cada e-mail enviado contém um token único de descadastro que permite ao usuário remover seu e-mail da base de dados com apenas um clique, sem necessidade de login.

Desenvolvido por Taiso Henrique Estudante de Sistemas de Informação - 7º Período
