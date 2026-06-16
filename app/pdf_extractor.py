import os
from typing import List
from pydantic import BaseModel, Field #type:ignore
from google import genai
from google.genai import types #type:ignore

# 1- Definindo o modelo de dados para os resultados extraídos

class ItemTransacao(BaseModel):
    periodo_movimento: str = Field(description="Periodo contábil da movimentação no formato MM/AAAA")
    categoria: str = Field(description="Categoria da transação, como 'Caixa', 'Bancos', 'Contas a Receber CP', etc.")
    valor: float = Field(description="Valor da transação, representado como um número decimal")

class RelatorioFinanceiro(BaseModel):
    empresa: str = Field(description="Nome da empresa a que o relatório financeiro pertence")
    transacoes: List[ItemTransacao] = Field(description="Lista de transações financeiras")

class FinancialExtractorService:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = 'gemini-2.5-flash'