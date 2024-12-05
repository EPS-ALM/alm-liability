import pandas as pd

def coletar_dados_faixa_etaria_horizontal(arquivo, nome_planilha, ano_inicio, ano_fim, sigla='BR', sexo='Ambos'):
    # Carregar o arquivo Excel
    df = pd.read_excel(arquivo, sheet_name=nome_planilha, header=None)

    # Buscar as células que contêm "IDADE", "SEXO", "SIGLA" e os anos (2000 a 2070)
    idade_coluna, sexo_coluna, sigla_coluna, anos_colunas = None, None, None, []

    # A linha com os cabeçalhos dos anos está na linha 6 (index 5)
    for col in range(len(df.iloc[5])):
        header = str(df.iloc[5, col]).strip().upper()
        
        header = header.replace('.0','')     

        if 'IDADE' in header:
            idade_coluna = col
        elif 'SEXO' in header:
            sexo_coluna = col
        elif 'SIGLA' in header:
            sigla_coluna = col
        # Verificar se o cabeçalho é um ano entre 2000 e 2070
        elif header.isdigit():
            ano = int(header)
            if ano_inicio <= ano <= ano_fim:
                anos_colunas.append(col)

    # Verificar se todas as colunas foram identificadas corretamente
    if None in (idade_coluna, sexo_coluna, sigla_coluna) or not anos_colunas:
        raise ValueError("As colunas 'IDADE', 'SEXO', 'SIGLA' ou os anos (2000 a 2070) não foram identificados corretamente.")

    # Coletar os dados para as faixas etárias, sexo "Ambos", sigla "BR" e os anos solicitados
    dados_filtrados = []
    
    for i in range(6, len(df)):  # Começar após a linha de cabeçalho (linha 6, index 5)
        idade_valor = df.iloc[i, idade_coluna]
        sexo_valor = df.iloc[i, sexo_coluna]
        sigla_valor = df.iloc[i, sigla_coluna]

        # Verificar se a linha atende aos filtros
        if str(idade_valor).strip() in [f"{x}" for x in range(14, 65)] and sexo_valor == sexo and sigla_valor == sigla:
            dados_ano_populacao = []
            
            # Coletar dados para todos os anos entre 2000 e 2070
            for col in anos_colunas:
                ano = int(df.iloc[5, col])  # Ano da coluna
                ano_valor = df.iloc[i, col]
                dados_ano_populacao.append({'ano': ano, 'população': int(ano_valor)})
            
            # Adicionar os dados da faixa etária com os anos e populações
            dados_filtrados.append((idade_valor, sexo_valor, sigla_valor, dados_ano_populacao))

    return dados_filtrados

# Teste do código
arquivo = "../dataset/projecoes_2024_tab1_idade_simples.xlsx"
nome_planilha = "1) POP_IDADE SIMPLES"
ano_inicio = 2000
ano_fim = 2070
sigla = "BR"
sexo = "Ambos"

try:
    resultados = coletar_dados_faixa_etaria_horizontal(arquivo, nome_planilha, ano_inicio, ano_fim, sigla, sexo)
    if resultados:
        for resultado in resultados:
            print(resultado)
    else:
        print("Nenhum resultado encontrado.")
except Exception as e:
    print(f"Erro: {e}")
