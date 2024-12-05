# Planejamento dos Gráficos

| **Botão**                          | **Gráfico**                                | **Descrição**                                                                                      | **Tipo de Gráfico**          |
|------------------------------------|--------------------------------------------|----------------------------------------------------------------------------------------------------|------------------------------|
| **1. Simulação de Cenários Econômicos** | População Economicamente Ativa (PEA) VS Aposentados | Comparação entre PEA e aposentados ao longo do tempo.                    | Gráfico de Linhas            |
|                                    | Crescimento Vegetativo (TCV)                      | Evolução da taxa de crescimento vegetativo ao longo do tempo.                                                  | Gráfico de Linhas            |
| **2. Previsão de Fluxo de Caixa**   | Entradas (linha verde)                      | Representa os valores de entrada ao longo do tempo.                                                | Gráfico de Linhas            |
|                                    | Saídas (linha vermelha)                     | Representa os valores de saída ao longo do tempo.                                                  | Gráfico de Linhas            |
|                                    | Entradas e Saídas combinadas                | Mostra as linhas de entrada (verde) e saída (vermelha) no mesmo gráfico para visualização conjunta. | Gráfico de Linhas            |
| **3. Gerenciamento de Liquidez**   | Liquidez ao longo do tempo                  | Diferença absoluta entre entradas e saídas, indicando lucro ou perda ao longo do tempo.            | Gráfico de Linhas            |
| **4. Análise de Sensibilidade de Carteira** | Cenário Selic                               | Impacto da taxa Selic no fundo.                                                                    | Gráfico de Linhas ou Barras  |
|                                    | Cenário Taxa Mínima de Positividade         | Limite da taxa mínima para evitar perdas.                                                         | Gráfico de Linhas            |
|                                    | Cenário Exagerado                           | Simula alta liquidez com muita entrada de dinheiro.                                                | Gráfico de Linhas ou Barras  |

---

### **Justificativa para os Tipos de Gráficos**
1. **Gráficos de Linhas**: 
   - São ideais para dados contínuos ao longo do tempo, como taxas, populações e fluxos financeiros.
   - Facilitam a visualização de tendências e comparações ao longo do tempo.

2. **Gráficos de Barras**:
   - Podem ser úteis para cenários comparativos, como análise de impacto ou simulações com valores discretos (e.g., Selic, alta liquidez).

### Simulação de Cenários Econômicos

#### Gráfico: PEA VS Aposentados
1. Eixo X = Ano
2. Eixo Y = QTD_PESSOAS(15-60), QTD_PESSOAS(61-90)

> Fonte: **População Economicamente Ativa - 2020 à 2070** - [Projeções das Populações, Revisão 2024](https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2024/projecoes_2024_tab1_idade_simples.xlsx) (Referência 2)

#### Gráfico: Crescimento Vegetativo
1. Eixo X = Ano
2. Eixo Y = TCV

> Fonte: **População Economicamente Ativa - 2020 à 2070** - [Projeções das Populações, Revisão 2024](https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2024/projecoes_2024_tab4_indicadores.xlsx)(Referência 2)

### Previsão de Fluxo de Caixa
1. Eixo X = Ano
2. Eixo Y = ENTRADAS, SAÍDAS

### Gerenciamento de Liquidez
1. Eixo X = Ano
2. Eixo Y = ENTRADAS - SAÍDAS

### Análise de Sensibilidade de Carteira
1. Eixo X = Ano
2. Eixo Y = API_SELIC, CENÁRIO_EXAGERADO, PLANO_1, PLANO_2, ..., PLANO_N

> Requirements pra consumir API_SELIC: pip install requests

## Fazer dps

1. Legenda eixo X e Y pra cada gráfico
2. API da Selic
3. Scrapping dos EXCEL

### Referências

> 1. **População Economicamente Ativa - 2020**: https://atlasescolar.ibge.gov.br/mundo/3016-espaco-economico/populacao-economicamente-ativa.html#:~:text=A%20popula%C3%A7%C3%A3o%20economicamente%20ativa%20%C3%A9,servi%C3%A7os%2C%20durante%20um%20per%C3%ADodo%20espec%C3%ADfico.
> 2. **Projeções da População**: https://www.ibge.gov.br/estatisticas/sociais/populacao/9109-projecao-da-populacao.html?edicao=41053
