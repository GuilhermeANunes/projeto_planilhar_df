from dotenv import load_dotenv  # type: ignore
from app.email_reader import EmailService
import time

# Carregando as credencias do arquivo .env
load_dotenv()

def main():
    EmailService()
    
if __name__ == "__main__":

    while True:
        main()
        time.sleep(10)  # Espera 60 segundos antes de verificar novamente