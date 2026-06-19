import os
from typing import Dict, List
from pydantic import BaseModel, Field #type: ignore
from google import genai
from google.genai import types #type: ignore

# 1. Definindo o contrato de dados (Schema) usando Pydantic
# para que a IA SEMPRE retorne os campos exatamente com esses nomes e tipos

class ItemConta(BaseModel):
    nome_conta: str = Field(description="Nome exato da conta contábil (Ex: 'Caixa e Bancos', 'FATUR. BRUTO')")
    valor: float = Field(description="Saldo numérico da conta (float)")

class DadosAnuais(BaseModel):
    ano: str = Field(description="Ano das informações financeiras. ")
    contas: List[ItemConta] = Field(
        description="""
        Dicionário onde a chave é o nome exato da conta e o valor é o saldo numérico.
        Exemplos de chaves válidas: 'Caixa e Bancos', 'FATUR. BRUTO', 'Empréstimos Bancários', 'PATRIMONIO LIQUIDO'.
        """
    )

class RelatorioEmpresa(BaseModel):
    nome_empresa: str = Field(description="Nome oficial, Razão Social ou Denominação Comercial da empresa")
    balancos: List[DadosAnuais] = Field(description="Lista contendo os dados extraídos de cada ano contábil")

class GrupoRelatorios(BaseModel):
    empresas: List[RelatorioEmpresa] = Field(
        description="Lista contendo as empresas identificadas nos documentos fornecidos. Se todos os PDFs forem da mesma empresa, esta lista terá apenas 1 elemento."
    )

class FinancialExtractorService:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"

    def extrair_dados_pdf(self, caminhos_pdfs: List[str]) -> GrupoRelatorios:
        print(f"Processando arquivos com IA...")

        conteudos_request = []

        for caminho in caminhos_pdfs:
            with open(caminho, "rb") as f:
                pdf_bytes = f.read()

            conteudos_request.append(types.Part.from_bytes(
                data=pdf_bytes,
                mime_type="application/pdf"
                ))

        prompt = """
        Atue como um auditor contábil sênior. Analise o PDF anexo e extraia as informações financeiras.
        Você deve mapear os saldos encontrados para as seguintes nomenclaturas de contas:
        
        valores_ativo: 'Caixa e Bancos', 'Aplicações Financeiras', 'Contas a Receber', 'Cooperados', 'CVA', 'Estoques', 'Adiant. a Fornecedores', 'Créditos a Fumicultores', 'Despesas Antecipadas', 'Impostos a Recuperar', 'Dividendos a Receber', 'Imposto Diferido', 'Outros Operac.', 'Outros Nao Operac.', 'Contas a Receber LP', 'Cooperados LP', 'C/C Coligadas/Acionistas', 'Depósitos Judiciais', 'Imposto Diferido LP', 'Créditos a Fumicultores LP', 'CTNs', 'Outros Operac. LP', 'Outros Nao Operac. LP', 'Imobilizado Técnico', 'Investimentos', 'Diferido/Intangível'.
        
        valores_passivo_e_pl: 'Fornecedores Nacionais', 'Fornecedores Estrangeiros', 'Empréstimos Bancários', 'Financiamentos Operacionais', 'Financiamentos c/ Tradings', 'Parcelas Correntes Financ. L.P.', 'Debêntures', 'Swap', 'Securitização', 'Leasing', 'Salários e Encargos', 'Tributos e Obrigações Fiscais', 'Tributos Parcelados', 'Adiantamento de Clientes', 'Custo Orçado', 'Terrenos', 'Outorga', 'Compromissos Consorciados', 'Plano de Previdênciário', 'Dividendos a pagar', 'Provisão para Contingência', 'C/C Coligadas/Acionistas Passivo', 'Outros Operac. Passivo', 'Outros Nao Operac. Passivo', 'Empréstimos e Financiamentos LP', 'Debêntures LP', 'Leasing LP', 'Financiamentos c/ Tradings LP', 'Securitização LP', 'Custo Orçado LP', 'Terrenos LP', 'Outorga LP', 'Compromissos Consorciados LP', 'Plano de Previdênciário LP', 'Dividendos a pagar LP', 'Provisão para Contingência LP', 'Tributos Parcelados LP', 'C/C Coligadas/Acionistas LP', 'Outros Operac. LP', 'Outros Nao Operac. LP', 'PATRIMONIO LIQUIDO'.
        
        valores_dre: 'N° MESES DO PERIODO', 'FATUR. BRUTO', 'Impostos/Deduções', 'Depreciação/Amortização', 'Arrendamento Mercantil', 'Custos Diretos', 'Despesas Comerciais', 'Despesas Administrativas', 'Despesas c/ Depreciação', 'Despesas Financeiras', 'Receitas Financeiras', 'Variações Monetárias Líq. LP', 'Outras Rec./(Desp.) Operac.', 'Equivalência Patrimonial', 'Res. não Operacional', 'Correção Monetária', 'Desp. c/ Amortização de Ágio/(Deságio)', 'Prov. I.R./Contrib. Soc.', 'Participação Minoritária'.
        
        Ignore linhas de totais ou subtotais, pois a planilha onde vou colar essas informações já calcula isso via fórmulas.
        Você pode consolidar informações semelhantes em uma única linha, mas deve manter a nomenclatura exata das contas conforme listado acima.
        Caso não haja valores correspondentes a uma conta específica, retorne 0 para essa conta.
        Extraia os valores com base mil, e lembre-se de que o valor do ativo total tem que ser o mesmo do passivo total + Patrimonio liquido.
        """
        conteudos_request.append(prompt)

        try:
            # Faz a chamada especificando que queremos uma resposta estruturada (JSON) baseada no nosso modelo Pydantic
            resposta = self.client.models.generate_content(
                model=self.model_name,
                contents=conteudos_request,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=GrupoRelatorios,
                    temperature=0.1 # Temperatura baixa para manter a IA factual e evitar alucinações
                ),
            )

            return GrupoRelatorios.model_validate_json(resposta.text)

        except Exception['error']['code'] == 503:
            print(f"[ERRO GENAI] IA com alta demanda. Estamos tentando novamente.")
            return self.extrair_dados_pdf(caminhos_pdfs) # Tenta novamente em caso de erro 503 (Service Unavailable)

        except Exception as e:
            print(f"[ERRO GENAI] Falha ao processar o documento com IA: {e}")
            return None