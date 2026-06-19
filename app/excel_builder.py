import os
import openpyxl #type: ignore

class ExcelService:
    def __init__(self):
        self.caminho_raiz = r'C:/Users/gui_a/OneDrive/Área de Trabalho/projeto_planilhar_df'
        self.caminho_modelo_excel = os.path.join(self.caminho_raiz, 'assets/modelo_planilhamento.xlsx')
        self.pasta_processados = os.path.join(self.caminho_raiz, 'processados')

        # Índice das colunas por ano: 0=2022, 1=2023, 2=2024, 3=2025
        self.MAPA_ANOS = {"2022": 0, "2023": 1, "2024": 2, "2025": 3}

        self.MAPA_CONTAS = {
            # --- ATIVO CIRCULANTE ---
            "Caixa e Bancos": ["C12", "E12", "G12", "I12"],
            "Aplicações Financeiras": ["C13", "E13", "G13", "I13"],
            "Contas a Receber": ["C14", "E14", "G14", "I14"],
            "Cooperados": ["C15", "E15", "G15", "I15"],
            "CVA": ["C16", "E16", "G16", "I16"],
            "Estoques": ["C17", "E17", "G17", "I17"],
            "Adiant. a Fornecedores": ["C18", "E18", "G18", "I18"],
            "Créditos a Fumicultores": ["C19", "E19", "G19", "I19"],
            "Despesas Antecipadas": ["C20", "E20", "G20", "I20"],
            "Impostos a Recuperar": ["C21", "E21", "G21", "I21"],
            "Dividendos a Receber": ["C22", "E22", "G22", "I22"],
            "Imposto Diferido": ["C23", "E23", "G23", "I23"],
            "Outros Operac.": ["C24", "E24", "G24", "I24"],
            "Outros Nao Operac.": ["C26", "E26", "G26", "I26"],

            # --- REALIZÁVEL A LONGO PRAZO (LP) ---
            "Contas a Receber LP": ["C30", "E30", "G30", "I30"],
            "Cooperados LP": ["C31", "E31", "G31", "I31"],
            "C/C Coligadas/Acionistas": ["C32", "E32", "G32", "I32"],
            "Depósitos Judiciais": ["C33", "E33", "G33", "I33"],
            "Imposto Diferido LP": ["C34", "E34", "G34", "I34"],
            "Créditos a Fumicultores LP": ["C35", "E35", "G35", "I35"],
            "CTNs": ["C36", "E36", "G36", "I36"],
            "Outros Operac. LP": ["C37", "E37", "G37", "I37"],
            "Outros Nao Operac. LP": ["C39", "E39", "G39", "I39"],

            # --- PERMANENTE ---
            "Imobilizado Técnico": ["C43", "E43", "G43", "I43"],
            "Investimentos": ["C44", "E44", "G44", "I44"],
            "Diferido/Intangível": ["C45", "E45", "G45", "I45"],
        
            # --- PASSIVO CIRCULANTE ---
            "Fornecedores Nacionais": ["C52", "E52", "G52", "I52"],
            "Fornecedores Estrangeiros": ["C53", "E53", "G53", "I53"],
            "Empréstimos Bancários": ["C54", "E54", "G54", "I54"],
            "Financiamentos Operacionais": ["C55", "E55", "G55", "I55"],
            "Financiamentos c/ Tradings": ["C56", "E56", "G56", "I56"],
            "Parcelas Correntes Financ. L.P.": ["C57", "E57", "G57", "I57"],
            "Debêntures": ["C58", "E58", "G58", "I58"],
            "Swap": ["C59", "E59", "G59", "I59"],
            "Securitização": ["C60", "E60", "G60", "I60"],
            "Leasing": ["C61", "E61", "G61", "I61"],
            "Salários e Encargos": ["C62", "E62", "G62", "I62"],
            "Tributos e Obrigações Fiscais": ["C63", "E63", "G63", "I63"],
            "Tributos Parcelados": ["C64", "E64", "G64", "I64"],
            "Adiantamento de Clientes": ["C65", "E65", "G65", "I65"],
            "Custo Orçado": ["C66", "E66", "G66", "I66"],
            "Terrenos": ["C67", "E67", "G67", "I67"],
            "Outorga": ["C68", "E68", "G68", "I68"],
            "Compromissos Consorciados": ["C69", "E69", "G69", "I69"],
            "Plano de Previdênciário": ["C70", "E70", "G70", "I70"],
            "Dividendos a pagar": ["C71", "E71", "G71", "I71"],
            "Provisão para Contingência": ["C72", "E72", "G72", "I72"],
            "C/C Coligadas/Acionistas Passivo": ["C73", "E73", "G73", "I73"],
            "Outros Operac. Passivo": ["C74", "E74", "G74", "I74"], 
            "Outros Nao Operac. Passivo": ["C76", "E76", "G76", "I76"],
            # EXIGÍVEL L.P.
            "Empréstimos e Financiamentos LP": ["C80", "E80", "G80", "I80"],
            "Debêntures LP": ["C81", "E81", "G81", "I81"],
            "Leasing LP": ["C82", "E82", "G82", "I82"],
            "Financiamentos c/ Tradings LP": ["C83", "E83", "G83", "I83"],
            "Securitização LP": ["C84", "E84", "G84", "I84"],
            "Custo Orçado LP": ["C85", "E85", "G85", "I85"],
            "Terrenos LP": ["C86", "E86", "G86", "I86"],
            "Outorga LP": ["C87", "E87", "G87", "I87"],
            "Compromissos Consorciados LP": ["C88", "E88", "G88", "I88"],
            "Plano de Previdênciário LP": ["C89", "E89", "G89", "I89"],
            "Dividendos a pagar LP": ["C90", "E90", "G90", "I90"],
            "Provisão para Contingência LP": ["C91", "E91", "G91", "I91"],
            "Tributos Parcelados LP": ["C92", "E92", "G92", "I92"],
            "C/C Coligadas/Acionistas LP": ["C93", "E93", "G93", "I93"],
            "Outros Operac. LP": ["C94", "E94", "G94", "I94"],
            "Outros Nao Operac. LP": ["C95", "E95", "G95", "I95"],

            # --- PATRIMÔNIO LÍQUIDO ---
            "PATRIMONIO LIQUIDO": ["C101", "E101", "G101", "I101"],
        
            # --- DEMONSTRATIVO DE RESULTADOS (DRE) ---
            "N° MESES DO PERIODO": ["C108", "E108", "G108", "I108"],
            "FATUR. BRUTO": ["C111", "E111", "G111", "I111"],
            "Impostos/Deduções": ["C112", "E112", "G112", "I112"],
            "Depreciação/Amortização": ["C115", "E115", "G115", "I115"],
            "Arrendamento Mercantil": ["C117", "E117", "G117", "I117"],
            "Custos Diretos": ["C118", "E118", "G118", "I118"],
            "Despesas Comerciais": ["C121", "E121", "G121", "I121"],
            "Despesas Administrativas": ["C122", "E122", "G122", "I122"],
            "Despesas c/ Depreciação": ["C123", "E123", "G123", "I123"],
            "Despesas Financeiras": ["C126", "E126", "G126", "I126"],
            "Receitas Financeiras": ["C127", "E127", "G127", "I127"],
            "Variações Monetárias Líq. LP": ["C128", "E128", "G128", "I128"],
            "Outras Rec./(Desp.) Operac.": ["C129", "E129", "G129", "I129"],
            "Equivalência Patrimonial": ["C131", "E131", "G131", "I131"],
            "Res. não Operacional": ["C132", "E132", "G132", "I132"],
            "Correção Monetária": ["C133", "E133", "G133", "I133"],
            "Desp. c/ Amortização de Ágio/(Deságio)": ["C134", "E134", "G134", "I134"],
            "Prov. I.R./Contrib. Soc.": ["C136", "E136", "G136", "I136"],
            "Participação Minoritária": ["C138", "E138", "G138", "I138"],
        }

    def preencher_planilha(self, lista_relatorios):
        if not lista_relatorios:
            return
        
        wb = openpyxl.load_workbook(self.caminho_modelo_excel, data_only=False)
        nomes_empresas_salvamento = []
        empresa = ''
        aba_nome = "EMP_1"

        for index, relatorio in enumerate(lista_relatorios[:2]):

            if relatorio.nome_empresa != empresa:
                empresa = relatorio.nome_empresa
                aba_nome = f"EMP_{index + 1}"
                if aba_nome not in wb.sheetnames:
                    continue
            
            sheet = wb[aba_nome]
            print(f"\n[EXCEL] Preenchendo a aba {aba_nome} para a empresa: {relatorio.nome_empresa}")

            sheet["B5"] = relatorio.nome_empresa
            
            # Formatando o nome para compor o nome do arquivo final posteriormente
            nome_limpo = relatorio.nome_empresa.lower().replace(" ", "_").replace("ltda", "").strip("_")
            nomes_empresas_salvamento.append(nome_limpo)

            # Estruturando uma matriz interna local com 0 por padrão para todas as células mapeadas
            # Isso garante o preenchimento com 0 caso a informação não exista no PDF
            dados_consolidados = {ano: {conta: 0.0 for conta in self.MAPA_CONTAS.keys()} for ano in self.MAPA_ANOS.keys()}

            # Sobrepõe os dados reais trazidos pela IA na matriz padrão
            for bloco_anual in relatorio.balancos:
                ano_str = str(bloco_anual.ano).strip()
                if ano_str in dados_consolidados:
                    for item in bloco_anual.contas:
                        nome_da_conta = item.nome_conta.strip()
                        valor_da_conta = item.valor
                        if nome_da_conta in dados_consolidados[ano_str]:
                            dados_consolidados[ano_str][nome_da_conta] = float(valor_da_conta) if valor_da_conta is not None else 0.0
                            
            # Escrevendo na planilha percorrendo o mapa master e os anos
            for conta, lista_celulas in self.MAPA_CONTAS.items():
                for ano_str, idx_ano in self.MAPA_ANOS.items():
                    coordenada_celula = lista_celulas[idx_ano]
                    valor_final = dados_consolidados[ano_str][conta]
                    
                    sheet[coordenada_celula] = valor_final

        string_empresas = "_e_".join(nomes_empresas_salvamento)
        nome_arquivo_saida = f"planilhamento_{string_empresas}.xlsx"
        caminho_final = os.path.join(self.pasta_processados, nome_arquivo_saida)

        wb.save(caminho_final)
        wb.close()
        print(f"\n[SUCESSO] Planilha salva em: {caminho_final}")