import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from datetime import datetime, timedelta
from service.repository.scripts.selic_api import get_selic_data  # Função já disponível no script
from sqlalchemy.exc import IntegrityError

from service.entity.base import get_session, SelicData

def update_selic_data(data_inicial, data_final):
    """
    Coleta os dados da API e armazena no banco de dados.
    """
    session = get_session()
    try:
        dados_selic = get_selic_data(data_inicial, data_final)

        for item in dados_selic:
            registro = SelicData(
                data=datetime.strptime(item["data"], "%d/%m/%Y").date(),
                valor=float(item["valor"])
            )
            session.add(registro)

        session.commit()
        print(f"Dados de {data_inicial} a {data_final} inseridos com sucesso.")
    except IntegrityError:
        session.rollback()
        print("Dados duplicados detectados. Inserção ignorada.")
    except Exception as e:
        print(f"Erro durante a atualização: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    # Data final é a data atual
    data_final = datetime.now().strftime("%d/%m/%Y")
    # Data inicial é 4 anos antes da data atual
    data_inicial = (datetime.now() - timedelta(days=4 * 365)).strftime("%d/%m/%Y")

    # Atualizar dados da API
    update_selic_data(data_inicial, data_final)


