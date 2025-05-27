# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação Flask/Waitress usará
EXPOSE 5000

# Comando para rodar a aplicação usando Waitress
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "main:app_dispatch"]

