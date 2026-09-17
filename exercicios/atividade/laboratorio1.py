# -*- coding: utf-8 -*-
"""laboratorio1.ipynb"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from collections import Counter
from scipy.stats import binom, geom, poisson, norm

# -----------------------------------------------------------------------------
# Carregamento do Arquivo Local
# -----------------------------------------------------------------------------
df = pd.read_csv('heart.csv', sep=',', encoding='utf-8')

df.head(20)

"""1) Determine a média, a moda, a mediana, o desvio padrão
e a variância da variável idade. Considere dados amostrais.

Média
"""

df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

media = df['Age'].mean()
print(media)

"""Moda"""

df['Age'].mode()

"""Mediana"""

df['Age'].median()

"""Desvio padrão
"""

df['Age'].std()

"""Variância da variável"""

df['Age'].var()

"""2) Construa um histograma para a variável idade."""

plt.hist(df['Age'], bins=6, color='blue', edgecolor='black')
plt.show()

"""3) Para a variável idade, a média é uma medida que
representa a centralidade dos dados? Justifique.
"""

media = df['Age'].mean()
mediana = df['Age'].median()

print(f"Média: {media:.2f}")
print(f"Mediana: {mediana:.2f}")

"""Sim, porque o valor do resultado é aproximadamente o valor do quartil 2 (mediana)

4) Determine a quantidade de pessoas do sexo feminino e
do sexo masculino em porcentagem. Faça um gráfico com essa
representação.

Sexo Feminino
"""

feminino = df.loc[df.Sex.isin(['F', 'f'])]
porcentagem = (len(feminino) / len(df)) * 100
print(f'{porcentagem:.2f}%')

masculino = df.loc[df.Sex.isin(['M', "m"])]
porcentagem = (len(masculino) / len(df)) * 100
print(f'{porcentagem:.2f}%')

contagem_pct = df['Sex'].str.upper().value_counts(normalize=True) * 100

plt.figure(figsize=(6, 4))
barras = plt.bar(contagem_pct.index, contagem_pct.values, color='#27F59F', edgecolor='black', width=0.5)

for barra in barras:
    altura = barra.get_height()
    plt.annotate(f'{altura:.2f}%',
                 xy=(barra.get_x() + barra.get_width() / 2, altura),
                 xytext=(0, 3),
                 textcoords="offset points",
                 ha='center', va='bottom', fontweight='bold')

plt.xlabel('Sexo')
plt.ylabel('Porcentagem (%)')
plt.title('Distribuição por Sexo')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.show()

"""5) Determine os valores máximo, mínimo e os quartis para a
variável colesterol. Construa um gráfico Boxplot. Essa variável possui
valores missing? Se sim, qual a sua ação com relação a isso?
"""

# Mínimo
df['Cholesterol'].min()

# Máximo
df['Cholesterol'].max()

# Primeiro Quartil
df['Cholesterol'].quantile(q=0.25)

# Segundo Quartil (Mediana)
df['Cholesterol'].quantile(q=0.5)

# Terceiro Quartil
df['Cholesterol'].quantile(q=0.75)

grafico = px.box(df, y="Cholesterol")
grafico.show()

total_vazios = df['Cholesterol'].isna().sum()
print(f"Total de valores vazios na coluna Cholesterol: {total_vazios}")
df = df.dropna(subset=['Cholesterol'])

print(f"Valores vazios restantes: {df['Cholesterol'].isna().sum()}")

df = df.reset_index(drop=True)

"""Após identificar que havia 3 valores vazios, não preenchidos, foi realizada a remoção das linhas.

6) A variável colesterol possui outliers? Se sim, estes valores
outliers são coerentes com a realidade? Qual a sua sugestão para
lidar com estes outliers (manter, excluir, alterar...)?
"""

q1 = df['Cholesterol'].quantile(0.25)
q3 = df['Cholesterol'].quantile(0.75)
iqr = q3 - q1

lim_inf = q1 - 1.5 * iqr
lim_sup = q3 + 1.5 * iqr

outliers = df[(df['Cholesterol'] < lim_inf) | (df['Cholesterol'] > lim_sup)]
print(f"Quantidade de Outliers: {len(outliers)}")
print("Valores iguais a zero:", (df['Cholesterol'] == 0).sum())

# Substituição dos zeros pela mediana dos valores válidos (>0)
mediana_valida = df.loc[df['Cholesterol'] > 0, 'Cholesterol'].median()
df['Cholesterol'] = df['Cholesterol'].replace(0, mediana_valida)

"""Sim, possui. Não são coerentes com a realidade porque 172 linhas estão com valores zero. A sugestão é alterar os valores zerados para a mediana dos dados válidos, para não perder 172 linhas de dados.

7) Qual a média, a moda e a mediana da variável colesterol?

Média
"""

media = df['Cholesterol'].mean()
print(media)

"""Moda"""

df['Cholesterol'].mode()

"""Mediana"""

df['Cholesterol'].median()

"""8) Qual a probabilidade de sortear ao acaso uma pessoa do
sexo masculino com idade inferior a 35 anos?
"""

condicao = (df['Sex'].str.upper() == 'M') & (df['Age'] < 35)
total_casos_favoraveis = len(df[condicao])

total_geral = len(df)

probabilidade = (total_casos_favoraveis / total_geral) * 100

print(f"Probabilidade: {probabilidade:.2f}%")

"""9) Qual a probabilidade de sortear ao acaso uma pessoa do
sexo feminino dado que essa pessoa possui idade inferior a 35 anos,
isto é, com a condição da idade ser inferior a 35 anos?
"""

grupo_condicao = df[df['Age'] < 35]

casos_favoraveis = len(grupo_condicao[grupo_condicao['Sex'].str.upper() == 'F'])

total_grupo = len(grupo_condicao)

probabilidade_condicional = (casos_favoraveis / total_grupo) * 100

print(f"Probabilidade: {probabilidade_condicional:.2f}%")

"""10) Em 20 sorteios, qual a probabilidade de saírem até 8 pessoas com doença cardíaca?"""

p = (df['HeartDisease'] == 1).mean()

n = 20
k = 8

probabilidade = binom.cdf(k, n, p)

print(f"Probabilidade de saírem até 8 pessoas: {probabilidade:.4f} ({probabilidade * 100:.2f}%)")

"""11) A variável Chest Pain Type (tipo de dor no peito)
possui as seguintes classes:

TA: angina típica;
ATA: angina atípica;
NAP: dor não anginosa;
ASY: assintomático.
Construa uma tabela com a frequência absoluta, a frequência
relativa e a frequência acumulada de cada classe.
"""

tabela = pd.DataFrame.from_dict(Counter(df['ChestPainType']), orient='index')
tabela = tabela.sort_index(ascending=True).reset_index()
tabela = tabela.rename(columns={'index': 'valor', 0: 'freq_abs'})

# Frequências relativas e acumuladas
tabela['freq_rel'] = tabela['freq_abs'] / tabela['freq_abs'].sum()
tabela['freq_rel_perc'] = np.round(tabela['freq_rel'] * 100, 2)
tabela['freq_acum'] = tabela['freq_abs'].cumsum()
print(tabela)

"""12) Simule uma apresentação dos resultados como se fosse
apresentar para a diretoria. Faça no próprio Colab mesmo, ao final das
análises dos itens anteriores.
"""

dicionario_variaveis = {
    'Variável': [
        'Age', 'Sex', 'Chest Pain Type', 'Resting BP', 'Cholesterol',
        'Fasting BS', 'Resting ECG', 'Max HR', 'Exercise Angina',
        'Old Peak', 'ST_Slope', 'Heart Disease'
    ],
    'Tipo': [
        'Quantitativa Contínua', 'Qualitativa Nominal', 'Qualitativa Nominal',
        'Quantitativa Contínua', 'Quantitativa Contínua', 'Qualitativa Nominal',
        'Qualitativa Nominal', 'Quantitativa Contínua', 'Qualitativa Nominal',
        'Quantitativa Contínua', 'Qualitativa Ordinal', 'Qualitativa Nominal'
    ],
    'Descrição': [
        'Idade do paciente',
        'Sexo biológico',
        'Tipo de dor no peito referida',
        'Pressão arterial sistólica em repouso',
        'Nível de colesterol sérico',
        'Glicemia em jejum',
        'Resultado do eletrocardiograma em repouso',
        'Frequência cardíaca máxima atingida',
        'Presença de angina induzida por esforço',
        'Depressão de ST induzida por esforço vs repouso',
        'Inclinação do segmento ST no pico do esforço',
        'Diagnóstico de doença cardíaca'
    ],
    'Valores / Categorias': [
        'Anos (ex: 20 a 80)',
        '0 = Masculino, 1 = Feminino',
        '0 = TA, 1 = ATA, 2 = NAP, 3 = ASY',
        'mmHg',
        'mg/dl',
        '0 = < 120 mg/dl, 1 = >= 120 mg/dl',
        '0 = Normal, 1 = ST, 2 = LVH',
        'Batimentos por minuto (bpm)',
        '0 = Não, 1 = Sim',
        'Valor numérico (mm)',
        '0 = Up, 1 = Flat, 2 = Down',
        '0 = Não possui, 1 = Possui'
    ]
}

tabela_dados = pd.DataFrame(dicionario_variaveis)

tabela_dados

sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 10})

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle('PAINEL EXECUTIVO: FATORES DE RISCO E PERFIL CARDÍACO',
             fontsize=16, fontweight='bold', y=0.98)

ax1 = axes[0, 0]
sns.countplot(data=df, x='Sex', hue='HeartDisease', palette=['#2b5c8f', '#d95f02'], ax=ax1)
ax1.set_title('1. Incidência por Sexo', fontweight='bold')
ax1.set_xlabel('Sexo (0 = Masculino, 1 = Feminino)')
ax1.set_ylabel('Total de Pacientes')
ax1.legend(['Saudável (0)', 'Com Doença (1)'], title='Diagnóstico')

ax2 = axes[0, 1]
sns.scatterplot(data=df, x='Age', y='MaxHR', hue='HeartDisease',
                palette=['#2b5c8f', '#d95f02'], alpha=0.7, ax=ax2)
ax2.set_title('2. Idade vs. Frequência Cardíaca Máxima (Max HR)', fontweight='bold')
ax2.set_xlabel('Idade (anos)')
ax2.set_ylabel('Frequência Cardíaca Máx.')
ax2.legend(['Saudável (0)', 'Com Doença (1)'], title='Diagnóstico')

ax3 = axes[1, 0]
sns.countplot(data=df, x='ChestPainType', hue='HeartDisease', palette=['#2b5c8f', '#d95f02'], ax=ax3)
ax3.set_title('3. Perfil de Risco por Tipo de Dor no Peito', fontweight='bold')
ax3.set_xlabel('Tipo de Dor (0: TA, 1: ATA, 2: NAP, 3: ASY)')
ax3.set_ylabel('Total de Pacientes')
ax3.legend(['Saudável (0)', 'Com Doença (1)'], title='Diagnóstico')

ax4 = axes[1, 1]
sns.boxplot(data=df, x='HeartDisease', y='Cholesterol', palette=['#2b5c8f', '#d95f02'], ax=ax4)
ax4.set_title('4. Níveis de Colesterol por Diagnóstico', fontweight='bold')
ax4.set_xlabel('Diagnóstico (0 = Saudável, 1 = Com Doença)')
ax4.set_ylabel('Colesterol Sérico (mg/dl)')

plt.tight_layout()
plt.show()
