# Usando uma imagem do Python
FROM python:3.13

# Definindo a pasta de trabalho dentro do contêiner
WORKDIR /app

# Copiando o arquivo de bibliotecas primeiro
COPY requirements.txt .

# Instalando as bibliotecas necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copiando todo o resto do código para dentro do contêiner
COPY . .

# Comando final que vai manter a aplicação rodando continuamente
CMD ["python", "main.py"]