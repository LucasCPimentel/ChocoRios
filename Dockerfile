# Use a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt requirements.txt

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Exponha a porta em que o aplicativo Flask está sendo executado
EXPOSE 5000

# Defina as variáveis de ambiente necessárias para o Flask
ENV FLASK_APP=ChocoRios.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para iniciar o aplicativo Flask quando o contêiner for iniciado
CMD ["flask", "run"]