import requests  # Biblioteca para fazer requisições HTTP
import json      # Para trabalhar com os dados JSON

# Definir o endpoint base da API
BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados"

# Função para obter os dados da API
def get_selic_data(data_inicial, data_final):
    """
    Busca os dados da taxa Selic entre duas datas específicas.

    Parâmetros:
    - data_inicial: Data de início no formato DD/MM/AAAA.
    - data_final: Data de término no formato DD/MM/AAAA.

    Retorno:
    - Lista de dicionários com os dados da taxa Selic.
    """
    params = {
        "formato": "json",
        "dataInicial": data_inicial,
        "dataFinal": data_final,
    }
    
    try:
        # Fazer a requisição à API
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Lança um erro se o status for diferente de 200
        
        # Retornar os dados em formato JSON
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return []

# Função para exibir os dados
def exibir_dados(dados):
    """
    Exibe os dados da taxa Selic formatados.

    Parâmetros:
    - dados: Lista de dicionários com os dados da taxa Selic.
    """
    if not dados:
        print("Nenhum dado disponível.")
        return

    print("\nTaxa Selic (em %):")
    for item in dados:
        print(f"Data: {item['data']}, Taxa: {item['valor']}%")

# Executar o script
if __name__ == "__main__":
    # Solicitar datas ao usuário
    data_inicial = input("Digite a data inicial (formato DD/MM/AAAA): ")
    data_final = input("Digite a data final (formato DD/MM/AAAA): ")

    # Obter os dados da API
    dados_selic = get_selic_data(data_inicial, data_final)

    # Exibir os dados
    exibir_dados(dados_selic)