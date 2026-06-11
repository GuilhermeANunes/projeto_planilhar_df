from dotenv import load_dotenv  # type: ignore
from app.email_reader import EmailService

# Carregando as credencias do arquivo .env
load_dotenv()

def main():
    EmailService()
    
if __name__ == "__main__":
    main()