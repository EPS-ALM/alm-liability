import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.graph_objects as go
import json
from service.repository.scripts.passives import fig

app = FastAPI()

# Funções e geração de dados (coletar_selic_anos, coletar_tcv, etc.) mantidas aqui.

@app.get("/grafico", response_class=HTMLResponse)
async def obter_grafico_html():
    # Converte o gráfico para JSON
    grafico_json = fig.to_json()

    # HTML da página
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>Gráfico - ALM Gestão de Passivos</h1>
        <div id="grafico"></div>
        <script>
            const graficoData = {grafico_json};  // Dados do gráfico
            Plotly.newPlot('grafico', graficoData.data, graficoData.layout);
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4200)