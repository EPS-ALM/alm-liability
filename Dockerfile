# Usar a imagem base oficial do Python
FROM python:3.11-slim

# Configurar o diretório de trabalho no contêiner
WORKDIR /app

# Adicionar o diretório raiz ao PYTHONPATH
ENV PYTHONPATH=/app

# Copiar os arquivos do projeto para o contêiner
COPY . /app

# Copiar o requirements.txt para o contêiner
COPY requirements.txt /app/requirements.txt

# Instalar as dependências
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expor a porta do serviço
EXPOSE 4201

# Comando para rodar o script
CMD ["python", "service/router/passives.py"]
