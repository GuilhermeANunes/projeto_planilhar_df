import win32com.client #type: ignore


class EmailService:
    
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 é a pasta de entrada
    messages = inbox.Items

    for message in list(messages):
        if message.Subject == "PLANILHAR" and message.UnRead:
            print(f'Mensagem de: {message.SenderEmailAddress}')
            print(f"Assunto: {message.Subject}")
            remetente = message.SenderEmailAddress
            message.UnRead = False  # Marcar como lida
            attachments = message.Attachments
            for attachment in attachments:
                attachment.SaveAsFile(f"C:\\Users\\gui_a\\OneDrive\\Área de Trabalho\\projeto_planilhar_df\\assets\\{attachment.FileName}")