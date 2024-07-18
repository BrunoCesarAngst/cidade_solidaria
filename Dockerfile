# Use a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Exponha a porta que o Streamlit usa
EXPOSE 8501

# Comando para rodar a aplicação
CMD ["streamlit", "run", "streamlit_app.py"]
