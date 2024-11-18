import requests as rq
import pandas as pd
import streamlit as st

#identificando as mulheres
url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=F&ordem=ASC&ordenarPor=nome'
resposta = rq.get(url)
dadosJSON = resposta.json()
dfMulheres = pd.DataFrame(dadosJSON['dados'])
dfMulheres['sexo'] = 'F'

#item 4
#identificando os homens
url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?siglaSexo=M&ordem=ASC&ordenarPor=nome'
resposta = rq.get(url)
dadosJSON = resposta.json()
dfHomens = pd.DataFrame(dadosJSON['dados'])
dfHomens['sexo'] = 'M'

#unindo os dataframes
df = pd.concat([dfMulheres, dfHomens])

#Filtrando df por sexo
#inserindo um selectbox
opcao = st.selectbox(
    'Qual o sexo?',
     df['sexo'].unique())

dfFiltrado = df[df['sexo'] == opcao]
st.title('Deputados do sexo ' + opcao)

#ocorrencias totais
#procurando no chat GPT: Como calcular a quantidade de deputados por estado?
ocorrencias = dfFiltrado['siglaUf'].value_counts()
dfEstados = pd.DataFrame({
    'siglaUf': ocorrencias.index,
    'quantidade': ocorrencias.values}
    )

#total de homens
totalHomens = dfHomens['id'].count()
st.metric('Total de Homens', totalHomens)

#total de mulheres
totalMulheres = dfMulheres['id'].count()
st.metric('Total de Mulheres', totalMulheres)

st.write('Total de deputadas do sexo ' + opcao)
st.bar_chart(dfEstados, x = 'siglaUf', y = 'quantidade', x_label='Siglas dos estados', y_label='Quantidade de deputados')

st.dataframe(dfFiltrado)

