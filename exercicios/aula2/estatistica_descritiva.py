# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import plotly.express as px

# 1. Carregamento e Preparação dos Dados
# Deixe o arquivo 'pesquisa_2.csv' na mesma pasta do script
caminho_arquivo = 'pesquisa_2.csv'
df = pd.read_csv(caminho_arquivo, sep=',', encoding='UTF-8')

# Renomeação e tratamento de tipos
df = df.rename(columns={'Qual o número de seu calçado?': 'tamanho_calçado'})
df['tamanho_calçado'] = df['tamanho_calçado'].replace(
    {'43-44': str((43 + 44) / 2), '40/41': str((40 + 41) / 2)}
)
df['tamanho_calçado'] = df['tamanho_calçado'].astype(float)

print('--- Primeiras Linhas dos Dados Tratados ---')
print(df.head())
print(f'\nDimensões do DataFrame: {df.shape}')
print(f'Tipos de dados:\n{df.dtypes}\n')

# 2. Medidas de Tendência Central (Coluna 'altura(m)')
altura = df['altura(m)']

print('--- Medidas de Tendência Central ---')
print(f'Média: {altura.mean():.4f}')
print(f'Média (arredondada): {round(altura.mean(), 2)}')
print(f'Mediana: {altura.median()}')
print(f'Moda:\n{altura.mode().to_string(index=False)}\n')

# 3. Medidas de Dispersão
variancia_amostral = altura.var()
variancia_populacional = altura.var(ddof=0)
desvio_padrao_amostral = altura.std()
desvio_padrao_populacional = np.sqrt(variancia_populacional)
soma_desvio_absoluto = (altura - altura.mean()).abs().sum()

print('--- Medidas de Dispersão ---')
print(f'Variância Amostral: {variancia_amostral:.4f}')
print(f'Variância Populacional: {variancia_populacional:.4f}')
print(f'Desvio Padrão Amostral: {desvio_padrao_amostral:.4f}')
print(f'Desvio Padrão Populacional: {desvio_padrao_populacional:.4f}')
print(f'Soma do Desvio Absoluto: {soma_desvio_absoluto:.4f}\n')

# 4. Medidas de Posição (Quartis e Percentis)
print('--- Medidas de Posição ---')
print(f'Mínimo: {altura.min()}')
print(f'1º Quartil (Q1 - 25%): {altura.quantile(0.25)}')
print(f'2º Quartil (Mediana - 50%): {altura.quantile(0.50)}')
print(f'3º Quartil (Q3 - 75%): {altura.quantile(0.75)}')
print(f'Percentil 90 (P90): {altura.quantile(0.90)}')
print(f'Máximo: {altura.max()}\n')

# 5. Resumo Estatístico Geral
print('--- Resumo Estatístico (describe) ---')
print(df.describe())

# 6. Visualização Gráfica (BoxPlot)
grafico = px.box(df, y='altura(m)', title='BoxPlot - Altura (m)')
grafico.show()
