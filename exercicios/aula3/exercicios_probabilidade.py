# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Carregamento dos dados
caminho_arquivo = 'pesquisa_tratada.csv'
dados = pd.read_csv(caminho_arquivo, sep=',', encoding='UTF-8')

print('--- Primeiras Linhas dos Dados ---')
print(dados.head(3))
print(f'\nTotal de registros (Espaço Amostral E): {len(dados)}\n')

# 2. Visualizações Gráficas
contagem_cores = dados['cor_favorita'].value_counts()

# Gráfico de pizza (setor)
plt.figure(figsize=(6, 6))
plt.pie(contagem_cores, labels=contagem_cores.index, autopct='%1.1f%%')
plt.title('Distribuição de Cores Favoritas')
plt.tight_layout()
plt.show()

# Gráfico de barras
plt.figure(figsize=(8, 4))
plt.bar(contagem_cores.index, contagem_cores.values, color='#27F59F')
plt.xlabel('Cores Favoritas')
plt.ylabel('Contagem')
plt.title('Distribuição de Cores Favoritas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Histograma de altura
plt.figure(figsize=(6, 4))
plt.hist(dados['altura'], bins=6, color='black', edgecolor='#F71EE9')
plt.xlabel('Altura')
plt.ylabel('Frequência')
plt.title('Histograma da Altura')
plt.tight_layout()
plt.show()

# 3. Definição de Subconjuntos
cor_preto = dados.loc[dados['cor_favorita'].isin(['preta', 'preto'])]
altura_menor_170 = dados.loc[dados['altura'] < 1.70]
cor_vermelho = dados.loc[dados['cor_favorita'].isin(['vermelha', 'vermelho'])]

total_E = len(dados)
n_preto = len(cor_preto)
n_menor_170 = len(altura_menor_170)
n_vermelho = len(cor_vermelho)

print('--- Contagens dos Eventos ---')
print(f'Pessoas com preferência por preto: {n_preto}')
print(f'Pessoas com altura < 1,70m: {n_menor_170}')
print(f'Pessoas com preferência por vermelho: {n_vermelho}\n')

# 4. Funções de Probabilidade
def calcular_probabilidade(evento, espaco_amostral):
    return (evento / espaco_amostral) * 100

def calcular_probabilidade_nao(evento, espaco_amostral):
    return (1 - (evento / espaco_amostral)) * 100

def calcular_intersecao_com_reposicao(evento_a, evento_b, espaco_amostral, ordem_importa=True):
    fator = 2 if ordem_importa else 1
    return (fator * ((evento_a / espaco_amostral) * (evento_b / espaco_amostral))) * 100

def calcular_uniao(evento_a, evento_b, espaco_amostral):
    p_a = evento_a / espaco_amostral
    p_b = evento_b / espaco_amostral
    return (p_a + p_b - (p_a * p_b)) * 100

def calcular_condicional(intersecao, condicao):
    return (intersecao / condicao) * 100

# 5. Cálculos e Exibição de Resultados
print('--- Resultados de Probabilidade Simples ---')
print(f'P(Cor Preto): {calcular_probabilidade(n_preto, total_E):.2f}%')
print(f'P(Altura < 1.70m): {calcular_probabilidade(n_menor_170, total_E):.2f}%')
print(f'P(Não Vermelho): {calcular_probabilidade_nao(n_vermelho, total_E):.2f}%\n')

print('--- Exercícios de Probabilidade Composta ---')
# Sorteio de 2 pessoas com reposição (qualquer ordem)
prob_duas_pessoas = calcular_intersecao_com_reposicao(n_menor_170, n_preto, total_E, ordem_importa=True)
print(f'P(Uma com < 1.70m e outra com Preto - qualquer ordem): {prob_duas_pessoas:.2f}%')

# Sorteio de 2 pessoas com reposição (ordem fixa)
prob_duas_ordem_fixa = calcular_intersecao_com_reposicao(n_menor_170, n_preto, total_E, ordem_importa=False)
print(f'P(Primeira com < 1.70m e segunda com Preto - ordem fixa): {prob_duas_ordem_fixa:.2f}%')

# União: Cor preta OU altura < 1,70m
prob_uniao = calcular_uniao(n_menor_170, n_preto, total_E)
print(f'P(Preto OU Altura < 1.70m): {prob_uniao:.2f}%\n')

# 6. Probabilidade Condicional
# Interseção real nos dados: pessoas que possuem altura < 1.70 E cor favorita preto/preta
intersecao_real = dados[dados['cor_favorita'].isin(['preto', 'preta']) & (dados['altura'] < 1.70)]
n_intersecao = len(intersecao_real)

print('--- Probabilidade Condicional ---')
prob_preto_dado_altura = calcular_condicional(n_intersecao, n_menor_170)
print(f'P(Preto | Altura < 1.70m): {prob_preto_dado_altura:.2f}%')

prob_altura_dado_preto = calcular_condicional(n_intersecao, n_preto)
print(f'P(Altura < 1.70m | Preto): {prob_altura_dado_preto:.2f}%')
