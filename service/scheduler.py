import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import schedule
import time
from datetime import datetime, timedelta
from service.repository.update_database import update_selic_data  # Substitua pelo nome correto do arquivo

def daily_task():
    """
    Tarefa diária para atualizar os dados da Selic.
    """
    data_final = datetime.now().strftime("%d/%m/%Y")
    data_inicial = (datetime.now() - timedelta(days=4 * 365)).strftime("%d/%m/%Y")
    print(f"Atualizando dados da API Selic de {data_inicial} a {data_final}...")
    update_selic_data(data_inicial, data_final)

# Agendar a tarefa para rodar todos os dias às 03:00 AM
schedule.every().day.at("03:00").do(daily_task)

print("Agendamento iniciado. O script está rodando...")

# Loop infinito para manter o script rodando
while True:
    schedule.run_pending()
    time.sleep(1)
