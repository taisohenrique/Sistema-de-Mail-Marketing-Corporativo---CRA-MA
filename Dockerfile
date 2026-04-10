# Usar uma versão oficial do Python mais leve
FROM python:3.11-slim

# Evita que o Python grave arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Garante que os logs apareçam na tela imediatamente
ENV PYTHONUNBUFFERED 1

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Instala as dependências
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o resto do projeto
COPY . /app/