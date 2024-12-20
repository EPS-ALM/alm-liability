import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))



import pandas as pd
import plotly.graph_objects as go
from service.repository.scripts.selic_api import get_selic_data  # API SELIC

# ------------------------------------------------------------------------------------------------------------- #
#                                                   FUNÇÕES

# Coleta dados da API Selic, já fazendo a média por ano com base na data de inicio e fim
def coletar_selic_anos(data_inicial, data_final):
    """
    Coleta os valores da Selic para os anos especificados usando dados de uma API.

    Parâmetros:
    - anos: Lista de anos para os quais a Selic será coletada.
    - data_inicial: Data de início no formato DD/MM/AAAA.
    - data_final: Data de término no formato DD/MM/AAAA.

    Retorna:
    - Um vetor contendo os valores da Selic para os anos fornecidos.
    """
    dados_selic = get_selic_data(data_inicial, data_final)
    
    if not dados_selic:
        print("Nenhum dado foi retornado pela API.")
        ano_inicial = int(data_inicial.split('/')[-1])
        ano_final = int(data_final.split('/')[-1])

        return {i:None for i in range(ano_inicial, ano_final+1)}

    # Processar os dados retornados pela API
    df_selic = pd.DataFrame(dados_selic)
    df_selic['data'] = pd.to_datetime(df_selic['data'], format='%d/%m/%Y').dt.year
    df_selic['valor'] = pd.to_numeric(df_selic['valor'])
    
    # Calcular a média dos valores para cada ano
    medias_anuais = df_selic.groupby('data')['valor'].mean().to_dict()

    return medias_anuais

# Coleta TCV (Taxa de Crescimento Vegetativo) do excel do IBGE
def coletar_tcv(arquivo, nome_planilha, ano_inicio, ano_fim, local=None):
    # Carregar o arquivo Excel
    df = pd.read_excel(arquivo, sheet_name=nome_planilha, header=None)  # Não especifica header inicialmente
    
    # Procurar pelas colunas 'ANO', 'TCV' e 'LOCAL'
    ano_coluna = None
    tcv_coluna = None
    local_coluna = None
    
    for i, row in df.iterrows():
        for j, cell in enumerate(row):
            if isinstance(cell, str) and 'ANO' in cell.upper():
                ano_coluna = j  # Encontrou a coluna do ano
            if isinstance(cell, str) and 'TCV' in cell.upper():
                tcv_coluna = j  # Encontrou a coluna do TCV
            if isinstance(cell, str) and 'LOCAL' in cell.upper():
                local_coluna = j  # Encontrou a coluna do local
            if ano_coluna is not None and tcv_coluna is not None and local_coluna is not None:
                break
        if ano_coluna is not None and tcv_coluna is not None and local_coluna is not None:
            break
    
    if ano_coluna is None or tcv_coluna is None or local_coluna is None:
        raise ValueError("As colunas 'ANO', 'TCV' e 'LOCAL' não foram encontradas na planilha.")
    
    # Agora pegar os dados abaixo de 'ANO', 'TCV' e 'LOCAL'
    anos = df.iloc[1:, ano_coluna].tolist()  # Pega todos os valores abaixo de 'ANO'
    tcv = df.iloc[1:, tcv_coluna].tolist()  # Pega todos os valores abaixo de 'TCV'
    locais = df.iloc[1:, local_coluna].tolist()  # Pega todos os valores abaixo de 'LOCAL'
    
    # Converter os valores de ano para inteiros, se possível
    anos = [int(ano) if isinstance(ano, (int, float, str)) and str(ano).isdigit() else None for ano in anos]
    
    # Filtrar os dados para os anos entre 'ano_inicio' e 'ano_fim' e o local, se fornecido
    if local:
        # Filtra pelos dados do local especificado
        dados_filtrados = [(ano, tcv_valor, local_valor) for ano, tcv_valor, local_valor in zip(anos, tcv, locais) 
                           if ano is not None and ano_inicio <= ano <= ano_fim and local_valor == local]
    else:
        # Se não houver filtro de local, retorna todos os dados
        dados_filtrados = [(ano, tcv_valor, local_valor) for ano, tcv_valor, local_valor in zip(anos, tcv, locais) 
                           if ano is not None and ano_inicio <= ano <= ano_fim]
    
    # Retorna os dados filtrados
    return dados_filtrados

# ------------------------------------------------------------------------------------------------------------- #
#                                            DADOS PARA OS GRÁFICOS

# Dados Selic (data_sensibilidade)
valores_selic = coletar_selic_anos("01/01/2020", "31/12/2024") 
anos = list(valores_selic.keys())  # Lista com os anos gerada pelas chaves do dict de valores
valores_por_ano = [valores_selic[ano] if valores_selic[ano] is not None else 0.0 for ano in anos]  # Lista com os valores de Selic

# Dados TCV (Dataset do IBGE)
valores_tcv = coletar_tcv('/app/service/repository/dataset/projecoes_2024_tab4_indicadores.xlsx', '4) INDICADORES', 2000, 2070, 'Brasil')
anos_tcv = [ano for ano, _, _ in valores_tcv]  # Lista com os anos
tcv = [tcv_valor for _, tcv_valor, _ in valores_tcv]  # Lista com os valores de TCV
anos_tcv_filtrados = [ano for ano in anos_tcv if 2020 <= ano <= 2024]
tcv_filtrado = [tcv_valor for ano, tcv_valor in zip(anos_tcv, tcv) if 2020 <= ano <= 2024]

# Dataset do IBGE (Ativos Vs Aposentados)
data_ativa_vs_aposentados = pd.DataFrame({
    'Ano': [2020, 2021, 2022, 2023, 2024],
    'Economicamente Ativa': [50, 52, 53, 54, 55],
    'Aposentados': [20, 22, 24, 26, 28]
})

# Dataset do IBGE (TCV)
data_taxa_vegetativo = pd.DataFrame({
    'Ano': anos_tcv_filtrados,
    'Crescimento Vegetativo': tcv_filtrado
})

# Dataset Mocado, pois precisa de dados da empresa
data_fluxo_caixa = pd.DataFrame({
    'Ano': [2020, 2021, 2022, 2023, 2024],
    'Entradas': [2, 3, 4, 5, 6],
    'Saídas': [1, 2, 3, 4, 5]
})

# Depende da variável data_fluxo_caixa. É a diferença entre entradas e saídas
data_liquidez = pd.DataFrame({
    'Ano': data_fluxo_caixa['Ano'],
    'Liquidez': data_fluxo_caixa['Entradas'] - data_fluxo_caixa['Saídas']
})

# Consome a API Selic para plotar dados reais da Selic. Os outros cenários dependem das decisões da empresa
data_sensibilidade = pd.DataFrame({
    'Ano': anos,
    'Selic': valores_por_ano,
    'Fidelidade - 5 anos': list(map(lambda selic: 1.8 * (selic / 4.5), valores_por_ano)),
    'Fidelidade - 15 anos': list(map(lambda selic: 2.8 * (selic / 4.5), valores_por_ano)),
    'Fidelidade - 30 anos': list(map(lambda selic: 3.8 * (selic / 4.5), valores_por_ano)),
    'Cenário Exagerado': list(map(lambda selic: 6 * (selic / 4.5), valores_por_ano))
})

# ------------------------------------------------------------------------------------------------------------- #
#                                          EIXOS X E Y DE CADA GRÁFICO

# Criação da figura
fig = go.Figure()

# Simulação de cenários econômicos com base em dados demográficos
fig.add_trace(go.Scatter(x=data_ativa_vs_aposentados['Ano'], 
                         y=data_ativa_vs_aposentados['Economicamente Ativa'], 
                         mode='lines+markers', name="Economicamente Ativa"))
fig.add_trace(go.Scatter(x=data_ativa_vs_aposentados['Ano'], 
                         y=data_ativa_vs_aposentados['Aposentados'], 
                         mode='lines+markers', name="Aposentados"))
fig.add_trace(go.Scatter(x=data_taxa_vegetativo['Ano'], 
                         y=data_taxa_vegetativo['Crescimento Vegetativo'], 
                         mode='lines+markers', name="Crescimento Vegetativo"))

# Previsão de Fluxo de Caixa
fig.add_trace(go.Scatter(x=data_fluxo_caixa['Ano'], 
                         y=data_fluxo_caixa['Entradas'], 
                         mode='lines+markers', line=dict(color='green'), 
                         name="Entradas"))
fig.add_trace(go.Scatter(x=data_fluxo_caixa['Ano'], 
                         y=data_fluxo_caixa['Saídas'], 
                         mode='lines+markers', line=dict(color='red'), 
                         name="Saídas"))

# Gerenciamento de Liquidez
fig.add_trace(go.Scatter(x=data_liquidez['Ano'], 
                         y=data_liquidez['Liquidez'], 
                         mode='lines+markers', name="Liquidez"))

# Análise de Sensibilidade de Carteira
fig.add_trace(go.Scatter(x=data_sensibilidade['Ano'], 
                         y=data_sensibilidade['Selic'], 
                         mode='lines+markers', name="Selic"))
fig.add_trace(go.Scatter(x=data_sensibilidade['Ano'], 
                         y=data_sensibilidade['Fidelidade - 5 anos'], 
                         mode='lines+markers', name="Fidelidade - 5 anos"))
fig.add_trace(go.Scatter(x=data_sensibilidade['Ano'], 
                         y=data_sensibilidade['Fidelidade - 15 anos'], 
                         mode='lines+markers', name="Fidelidade - 15 anos"))
fig.add_trace(go.Scatter(x=data_sensibilidade['Ano'], 
                         y=data_sensibilidade['Fidelidade - 30 anos'], 
                         mode='lines+markers', name="Fidelidade - 30 anos"))
fig.add_trace(go.Scatter(x=data_sensibilidade['Ano'], 
                         y=data_sensibilidade['Cenário Exagerado'], 
                         mode='lines+markers', name="Cenário Exagerado"))

# ------------------------------------------------------------------------------------------------------------- #
#                                       DROPDAWN PARA APLICAÇÃO DE FILTROS

# Configurando os menus dropdown
fig.update_layout(
    updatemenus=[
        {
            "buttons": [
                {"args": [{"visible": [True, True, False, False, False, False, False, False, False, False, False]}], 
                 "label": "População: Ativa vs Aposentados", 
                 "method": "update"},
                {"args": [{"visible": [False, False, True, False, False, False, False, False, False, False, False]}], 
                 "label": "Crescimento Vegetativo", 
                 "method": "update"}
            ],
            "direction": "down",
            "showactive": True,
            "x": 0.642,
            "y": 1.2,
            "xanchor": "right",
            "yanchor": "top"
        },
        {
            "buttons": [
                {"args": [{"visible": [False, False, False, True, True, False, False, False, False, False, False]}], 
                 "label": "Fluxo de Caixa: Entradas e Saídas", 
                 "method": "update"}
            ],
            "direction": "down",
            "showactive": True,
            "x": 0.893,
            "y": 1.2,
            "xanchor": "right",
            "yanchor": "top"
        },
        {
            "buttons": [
                {"args": [{"visible": [False, False, False, False, False, True, False, False, False, False, False]}], 
                 "label": "Liquidez", 
                 "method": "update"}
            ],
            "direction": "down",
            "showactive": True,
            "x": 0.99,
            "y": 1.2,
            "xanchor": "right",
            "yanchor": "top"
        },
        {
            "buttons": [
                {"args": [{"visible": [False, False, False, False, False, False, True, True, True, True, True]}], 
                 "label": "Sensibilidade: Selic e Taxas", 
                 "method": "update"}
            ],
            "direction": "down",
            "showactive": True,
            "x": 1.2,
            "y": 1.2,
            "xanchor": "right",
            "yanchor": "top"
        }
    ]
)

# ------------------------------------------------------------------------------------------------------------- #

# Layout geral
fig.update_layout(
    title="ALM - Gestão de Passivos",
    template='plotly_white',
    height=700,
    width=1200,
    xaxis=dict(
        tickmode='array',
        tickvals=anos,  # Apenas os anos inteiros
        ticktext=['2020', '2021', '2022', '2023', '2024']  # Rótulos correspondentes
    )
)

# fig.show()