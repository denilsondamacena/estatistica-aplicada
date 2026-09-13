# -*- coding: utf-8 -*-
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns

# 1. Carregamento e Preparação dos Dados
# Ajuste o caminho do arquivo para a localização no seu computador
caminho_arquivo = 'dados_tratados_dolar.csv'
df = pd.read_csv(caminho_arquivo, sep=',', encoding='iso-8859-1')

# Conversão da coluna 'datas' para datetime
df['datas'] = pd.to_datetime(df['datas'], format='%d/%m/%Y')
compra = df['compra']

print("--- Visão Inicial dos Dados ---")
print(df.head(3))
print(f"\nDimensões do DataFrame: {df.shape}")
print(f"Tipos de dados:\n{df.dtypes}\n")

# 2. Tabela de Frequência por Valores Individuais
freq_absoluta = Counter(compra)
tabela = pd.DataFrame.from_dict(freq_absoluta, orient='index').sort_index()
tabela.reset_index(inplace=True)
tabela.columns = ['valor', 'freq_abs']

tabela['freq_rel'] = tabela['freq_abs'] / tabela['freq_abs'].sum()
tabela['freq_rel_perc'] = tabela['freq_rel'] * 100
tabela['freq_acum'] = tabela['freq_abs'].cumsum()

print("--- Tabela de Frequências (Valores Individuais) ---")
print(tabela)
print(f"\nValor Mínimo: {tabela.valor.min()}")
print(f"Valor Máximo: {tabela.valor.max()}")
print(f"Amplitude Total: {tabela.valor.max() - tabela.valor.min():.4f}\n")

# 3. Tabela de Distribuição de Frequências por Classes
classes = [5.3, 5.4, 5.5, 5.6, 5.7]
labels = ['5.3 - 5.4', '5.4 - 5.5', '5.5 - 5.6', '5.6 - 5.7']

intervalos = pd.cut(
    x=tabela.valor, bins=classes, labels=labels, include_lowest=True
)

freq_abs = pd.Series(intervalos).value_counts().sort_index()
freq_rel = pd.Series(intervalos).value_counts(normalize=True).sort_index()

dist_freq = pd.DataFrame(
    {'Frequência absoluta': freq_abs, 'Frequência relativa': freq_rel}
)
dist_freq['freq_rel_perc'] = np.round(dist_freq['Frequência relativa'] * 100, 2)
dist_freq['freq_acum'] = dist_freq['Frequência absoluta'].cumsum()

print("--- Distribuição de Frequências por Classes ---")
print(dist_freq)

# 4. Visualizações Gráficas

# Histograma com Matplotlib
plt.figure(figsize=(6, 4))
plt.hist(df['compra'], bins=4, color='#6309BE')
plt.title('Histograma - Matplotlib')
plt.xlabel('Compra')
plt.ylabel('Frequência')
plt.tight_layout()
plt.show()

# Histograma com Seaborn
plt.figure(figsize=(6, 4))
sns.histplot(df['compra'], bins=4, color='#FF7D00', kde=True)
plt.title('Histograma com KDE - Seaborn')
plt.xlabel('Compra')
plt.ylabel('Frequência')
plt.tight_layout()
plt.show()

# Histograma interativo com Plotly
grafico = px.histogram(df, x='compra', nbins=6, title='Histograma - Plotly')
grafico.update_traces(
    marker_color=[
        '#75a59e',
        '#588e7f',
        '#3f775f',
        '#317c53',
        '#2a9d58',
        '#2cbe56',
    ]
)
grafico.update_layout(width=600, height=400)
grafico.show()
