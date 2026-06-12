import win32com.client #type: ignore
import os

class EmailService:
    def __init__(self):
        # Inicializa a conexão com o Outlook local
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.inbox = self.outlook.GetDefaultFolder(6)  # 6 é a pasta de entrada (Inbox)
        
        # Define a pasta de destino usando raw string (r"") para evitar problemas com barras dadas pelo Windows
        self.pasta_assets = r"C:\Users\gui_a\OneDrive\Área de Trabalho\projeto_planilhar_df\assets"

    def processar_emails_financeiros(self):
        print("Iniciando varredura da caixa de entrada do Outlook...")
        messages = self.inbox.Items

        # Cria um filtro nativo do Outlook: apenas e-mails NÃO lidos E com o assunto exato
        filtro = "[UnRead] = true AND [Subject] = 'PLANILHAR'"
        
        # Aplica o filtro diretamente no Outlook (extremamente rápido)
        mensagens_filtradas = messages.Restrict(filtro)

        # Garante que a pasta de destino existe antes de baixar
        if not os.path.exists(self.pasta_assets):
            os.makedirs(self.pasta_assets)

        # Iterar sobre as mensagens filtradas
        for message in list(mensagens_filtradas):
            # Validação de segurança: Class 43 garante que o item é estritamente um e-mail (MailItem)
            if message.Class == 43:
                remetente = message.SenderEmailAddress
                assunto = message.Subject
                
                print(f"\nProcessando e-mail de: {remetente}")
                print(f"Assunto: {assunto}")

                attachments = message.Attachments
                if attachments.Count > 0:
                    for attachment in attachments:
                        # Monta o caminho completo de forma segura usando o os.path.join
                        caminho_salvamento = os.path.join(self.pasta_assets, attachment.FileName)
                        
                        # Salva o arquivo na pasta configurada
                        attachment.SaveAsFile(caminho_salvamento)
                        print(f" -> Anexo salvo com sucesso: {attachment.FileName}")
                else:
                    print(" -> Este e-mail não continha anexos.")

                # O e-mail só é marcado como lido APÓS o processamento dos anexos terminar com sucesso
                message.UnRead = False
                print(" -> Mensagem marcada como lida.")