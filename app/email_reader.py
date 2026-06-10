import os
import requests # type: ignore

class EmailService:
    def __init__(self):
        self.tenant_id = os.getenv('AZURE_TENANT_ID')
        self.client_id = os.getenv('AZURE_CLIENT_ID')
        self.client_secret = os.getenv('AZURE_CLIENT_SECRET')
        self.email_alvo = os.getenv('EMAIL_ALVO')

        # URL base oficial da API da Microsoft
        self.base_url = "https://graph.microsoft.com/v1.0"

    def _obter_token_de_acesso(self):
        """ Gera um token de segurança temporario (OAuth2) """
        url_token = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        payload = {
            "client_id":self.client_id,
            "scope":"https://graph.microsoft.com/.default",
            "client_secret":self.client_secret,
            "grant_type":"client_credentials"
        }

        resposta = requests.post(url_token, data=payload)

        if resposta.status_code == 200:
            return resposta.json().get("access_token")
        else:
            print(f'[ERRO] Falha ao autenticar no Azure: {resposta.text}')
            return None
    
    def verificar_novos_emails(self):
        print("Buscando novos e-mails via Microsoft Graph API...")

        # 1. Pega a "Chave de entrada" para a API
        token = self._obter_token_de_acesso()
        if not token:
            print("[ERRO] Não foi possível obter o token de acesso.")
            return []

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # 2. Faz a requisição para pegar os e-mails
        # Endpoint focado apenas na pasta "Caixa de Entrada" do usuário alvo
        endpoint = f'{self.base_url}/users/{self.email_alvo}/mailFolders/Inbox/messages'

        # OData Query: Filtra não lidos, assuntos contendo 'PLANILHAR' e já seleciona só os dados úteis
        params = {
            "$filter": "isRead eq false and contains(subject, 'PLANILHAR')",
            "$select": "id,subject,from,hasAttachments"
        }

        # 3. Faz a requisição para buscar os e-mails
        resposta = requests.get(endpoint, headers=headers, params=params)

        if resposta.status_code == 200:
            emails = resposta.json().get("value", [])
            print(f'{len(emails)} E-mail(s) Encontrado(s) para processar.')

            for email in emails:
                id_mensagem = email.get("id")
                assunto = email.get("subject")
                remetente = email.get("from", {}).get("emailAddress", {}).get("address")
                tem_anexo = email.get("hasAttachments")

                print(f'-> E-mail de: {remetente}')
                print(f'   Assunto: {assunto}')
                print(f'   Tem Anexo? {"Sim" if tem_anexo else "Não"}')
                print("-" * 40)

                # Se tiver anexo, o sistema baixa os PDFs
                if tem_anexo:
                    self.baixar_anexos(id_mensagem, token)
                
        else:
            print(f'[ERRO] Falha ao buscar e-mails: {resposta.text}')