from app.email_reader import EmailService
from app.pdf_extractor import FinancialExtractorService
from app.excel_builder import ExcelService
import time
import os
import shutil

def executar_automacao():
    # 1. Busca os e-mails e joga os anexos na pasta assets
    leitor_outlook = EmailService()
    leitor_outlook.processar_emails_financeiros()
    
    caminho_raiz = r"C:\Users\gui_a\OneDrive\Área de Trabalho\projeto_planilhar_df"
    pasta_assets = os.path.join(caminho_raiz, "assets")
    pasta_processados = os.path.join(caminho_raiz, "processados")
    
    arquivos_pdf = [os.path.join(pasta_assets, f) for f in os.listdir(pasta_assets) if f.lower().endswith('.pdf')]
    
    if not arquivos_pdf:
        print("Nenhum novo documento PDF para processar na pasta assets.")
        return

    extrator = FinancialExtractorService()
    gerenciador_excel = ExcelService()
    
    relatorios_finais = []

    # 2. Processa cada documento encontrado
    for caminho_pdf in arquivos_pdf:
        dados_empresa = extrator.extrair_dados_pdf(caminho_pdf)
        
        if dados_empresa:
            relatorios_finais.append(dados_empresa)
                
            # Move o PDF original para a pasta "processados" para não reprocessar na próxima execução
            shutil.move(caminho_pdf, os.path.join(pasta_processados, os.path.basename(caminho_pdf)))

    # 3. Preenche todos os dados coletados de uma vez no modelo Excel
    if relatorios_finais:
        gerenciador_excel.preencher_planilha(relatorios_finais)

if __name__ == "__main__":

    while True:
        executar_automacao()
        