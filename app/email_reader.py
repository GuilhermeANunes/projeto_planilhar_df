import win32com.client #type: ignore


class EmailService:
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 é a pasta de entrada
    messages = inbox.Items

    for message in list(messages):
        if message.Subject == "PLANILHAR":
            attachments = message.Attachments
            for attachment in attachments:
                attachment.SaveAsFile(f"C:\\Users\\gui_a\\OneDrive\\Área de Trabalho\\projeto_planilhar_df\\assets\\{attachment.FileName}")