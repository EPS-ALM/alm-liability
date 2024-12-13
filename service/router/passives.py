import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


import uvicorn
from fastapi import FastAPI, Query
from sqlalchemy.orm import Session
from service.repository.update_database import SelicData, get_session
import pandas as pd
import plotly.graph_objects as go
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/grafico/ativos-aposentados", response_class=HTMLResponse)
def ativos_aposentados(
    crescimento_ativa: float, crescimento_aposentados: float, anos: int = 5
):
    """
    Retorna o gráfico de População Ativa vs Aposentados com base nas taxas de crescimento fornecidas.
    """
    # Dados iniciais fictícios
    dados = {"Ano": [2020], "Economicamente Ativa": [50], "Aposentados": [20]}

    # Gerar os dados para os próximos anos com base nas taxas de crescimento fornecidas
    for i in range(1, anos + 1):
        ano = dados["Ano"][-1] + 1
        ativa = dados["Economicamente Ativa"][-1] * (1 + crescimento_ativa / 100)
        aposentados = dados["Aposentados"][-1] * (1 + crescimento_aposentados / 100)

        dados["Ano"].append(ano)
        dados["Economicamente Ativa"].append(ativa)
        dados["Aposentados"].append(aposentados)

    df = pd.DataFrame(dados)

    # Criar o gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Ano"], y=df["Economicamente Ativa"], mode="lines+markers", name="Economicamente Ativa"))
    fig.add_trace(go.Scatter(x=df["Ano"], y=df["Aposentados"], mode="lines+markers", name="Aposentados"))

    fig.update_layout(
        title="População Ativa vs Aposentados",
        xaxis_title="Ano",
        yaxis_title="População (milhões)",
        template="plotly_white",
    )

    return fig.to_html(full_html=False)

@app.get("/grafico/crescimento-vegetativo", response_class=HTMLResponse)
def crescimento_vegetativo(tcv_inicial: float, tcv_decaimento: float, anos: int = 5):
    """
    Retorna o gráfico do Crescimento Vegetativo com base nos parâmetros fornecidos.
    """
    # Dados iniciais fictícios
    dados = {"Ano": [2020], "Crescimento Vegetativo": [tcv_inicial]}

    # Gerar os dados para os próximos anos com base no decaimento fornecido
    for i in range(1, anos + 1):
        ano = dados["Ano"][-1] + 1
        tcv = dados["Crescimento Vegetativo"][-1] * (1 - tcv_decaimento / 100)

        dados["Ano"].append(ano)
        dados["Crescimento Vegetativo"].append(tcv)

    df = pd.DataFrame(dados)

    # Criar o gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Ano"], y=df["Crescimento Vegetativo"], mode="lines+markers", name="TCV"))

    fig.update_layout(
        title="Taxa de Crescimento Vegetativo",
        xaxis_title="Ano",
        yaxis_title="Taxa (%)",
        template="plotly_white",
    )

    return fig.to_html(full_html=False)


@app.get("/grafico/fluxo-caixa", response_class=HTMLResponse)
def fluxo_caixa(
    entradas_iniciais: float,
    saidas_iniciais: float,
    crescimento_entradas: float,
    crescimento_saidas: float,
    anos: int = 5,
):
    """
    Retorna o gráfico de Fluxo de Caixa com base nos parâmetros fornecidos.
    """
    # Dados iniciais fictícios
    dados = {"Ano": [2020], "Entradas": [entradas_iniciais], "Saídas": [saidas_iniciais]}

    # Gerar os dados para os próximos anos com base nas taxas de crescimento fornecidas
    for i in range(1, anos + 1):
        ano = dados["Ano"][-1] + 1
        entradas = dados["Entradas"][-1] * (1 + crescimento_entradas / 100)
        saidas = dados["Saídas"][-1] * (1 + crescimento_saidas / 100)

        dados["Ano"].append(ano)
        dados["Entradas"].append(entradas)
        dados["Saídas"].append(saidas)

    df = pd.DataFrame(dados)

    # Criar o gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Ano"], y=df["Entradas"], mode="lines+markers", name="Entradas", line=dict(color="green")))
    fig.add_trace(go.Scatter(x=df["Ano"], y=df["Saídas"], mode="lines+markers", name="Saídas", line=dict(color="red")))

    fig.update_layout(
        title="Fluxo de Caixa: Entradas vs Saídas",
        xaxis_title="Ano",
        yaxis_title="Valores (milhões)",
        template="plotly_white",
    )

    return fig.to_html(full_html=False)

@app.get("/grafico/sensibilidade", response_class=HTMLResponse)
def sensibilidade(
    multiplicador_5_anos: float,
    multiplicador_15_anos: float,
    multiplicador_30_anos: float,
    multiplicador_exagerado: float,
):
    """
    Retorna o gráfico de Sensibilidade baseado na Taxa Selic e multiplicadores fornecidos.
    """
    # Consultar os dados da Taxa Selic no banco
    session = get_session()
    resultados = session.query(SelicData).all()
    session.close()

    if not resultados:
        return "<p>Nenhum dado da Taxa Selic encontrado no banco.</p>"

    # Criar o DataFrame
    df = pd.DataFrame([{"Ano": r.data.year, "Selic": r.valor} for r in resultados])
    df = df.groupby("Ano").mean().reset_index()

    # Adicionar cenários
    df["Fidelidade - 5 anos"] = df["Selic"] * multiplicador_5_anos
    df["Fidelidade - 15 anos"] = df["Selic"] * multiplicador_15_anos
    df["Fidelidade - 30 anos"] = df["Selic"] * multiplicador_30_anos
    df["Cenário Exagerado"] = df["Selic"] * multiplicador_exagerado

    # Criar o gráfico
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Ano"], y=df["Selic"], mode="lines+markers", name="Selic"))
    fig.add_trace(go.Scatter(x=df["Ano"], y=df["Fidelidade - 5 anos"], mode="lines+markers", name="Fidelidade - 5 anos"))
    fig.add_trace(go.Scatter(x=df["Ano"], y=df["Fidelidade - 15 anos"], mode="lines+markers", name="Fidelidade - 15 anos"))
    fig.add_trace(go.Scatter(x=df["Ano"], y=df["Fidelidade - 30 anos"], mode="lines+markers", name="Fidelidade - 30 anos"))
    fig.add_trace(go.Scatter(x=df["Ano"], y=df["Cenário Exagerado"], mode="lines+markers", name="Cenário Exagerado"))

    fig.update_layout(
        title="Sensibilidade da Taxa Selic",
        xaxis_title="Ano",
        yaxis_title="Taxa (%)",
        template="plotly_white",
    )

    return fig.to_html(full_html=False)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4200)