# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from scipy.stats import binom, geom, norm, poisson

# 1. Carregamento e visão geral dos dados
caminho_arquivo = 'enem_cidade_sp.csv'
enem_sp = pd.read_csv(caminho_arquivo, sep=',', encoding='iso-8859-1')

print('--- Visão Inicial dos Dados do ENEM SP ---')
print(enem_sp.head(2))
print(f'\nDimensões do DataFrame: {enem_sp.shape}\n')

# 2. Distribuição Binomial
# Proporção de mulheres no conjunto de dados (sucesso p)
mulher_enem = enem_sp.loc[enem_sp['SEXO'] == 'F']
p_mulher = len(mulher_enem) / len(enem_sp)

print('--- Distribuição Binomial (Amostra n = 10) ---')
print(f'Proporção de mulheres (p): {p_mulher:.4f}\n')

# Exatamente 4 mulheres em 10 amostras
prob_exat_4 = binom.pmf(4, 10, p_mulher)
print(f'P(X = 4): {prob_exat_4:.4f} ({prob_exat_4 * 100:.2f}%)')

# Até 4 mulheres em 10 amostras
prob_ate_4 = binom.cdf(4, 10, p_mulher)
print(f'P(X <= 4): {prob_ate_4:.4f} ({prob_ate_4 * 100:.2f}%)')

# Pelo menos 1 mulher em 10 amostras (1 - P(X = 0))
prob_pelo_menos_1 = 1 - binom.pmf(0, 10, p_mulher)
print(f'P(X >= 1): {prob_pelo_menos_1:.4f} ({prob_pelo_menos_1 * 100:.2f}%)')

# Mais do que 2 mulheres em 10 amostras (1 - P(X <= 2))
prob_mais_de_2 = 1 - binom.cdf(2, 10, p_mulher)
print(f'P(X > 2): {prob_mais_de_2:.4f} ({prob_mais_de_2 * 100:.2f}%)')

# Mais do que 3 mulheres em 10 amostras (1 - P(X <= 3))
prob_mais_de_3 = 1 - binom.cdf(3, 10, p_mulher)
print(f'P(X > 3): {prob_mais_de_3:.4f} ({prob_mais_de_3 * 100:.2f}%)')

# Mais do que 8 mulheres em 10 amostras (1 - P(X <= 8))
prob_mais_de_8 = 1 - binom.cdf(8, 10, p_mulher)
print(f'P(X > 8): {prob_mais_de_8:.4f} ({prob_mais_de_8 * 100:.2f}%)\n')

# 3. Distribuição Geométrica
# Probabilidade do primeiro sucesso (mulher) ocorrer na 4ª tentativa
prob_geom_4 = geom.pmf(4, p_mulher)
print('--- Distribuição Geométrica ---')
print(f'P(Primeira mulher na 4ª tentativa): {prob_geom_4:.4f} ({prob_geom_4 * 100:.2f}%)\n')

# 4. Distribuição de Poisson
# Exemplo teórico: k = 2 ocorrências para taxa média lambda = 5
prob_poisson_exata = poisson.pmf(2, 5)
prob_poisson_acum = poisson.cdf(2, 5)

print('--- Distribuição de Poisson (lambda = 5) ---')
print(f'P(X = 2): {prob_poisson_exata:.4f} ({prob_poisson_exata * 100:.2f}%)')
print(f'P(X <= 2): {prob_poisson_acum:.4f} ({prob_poisson_acum * 100:.2f}%)\n')

# 5. Distribuição Contínua (Normal)
# Exemplo teórico: x = 4.5, média = 4.8, desvio padrão = 0.5
prob_norm_exemplo = norm.cdf(4.5, loc=4.8, scale=0.5)
print('--- Distribuição Normal (Exemplo Teórico) ---')
print(f'P(X <= 4.5 | mu=4.8, sigma=0.5): {prob_norm_exemplo:.4f}\n')

# Aplicação com a coluna IDADE do ENEM SP
media_idade = enem_sp['IDADE'].mean()
desvio_idade = enem_sp['IDADE'].std()

print('--- Distribuição Normal Aplicada à IDADE (ENEM 2019) ---')
print(f'Média de Idade: {media_idade:.2f}')
print(f'Desvio Padrão de Idade: {desvio_idade:.2f}\n')

# P(Idade < 17 anos)
prob_idade_menor_17 = norm.cdf(17, loc=media_idade, scale=desvio_idade)
print(f'P(Idade < 17): {prob_idade_menor_17:.4f} ({prob_idade_menor_17 * 100:.2f}%)')

# P(Idade > 50 anos)
prob_idade_maior_50 = 1 - norm.cdf(50, loc=media_idade, scale=desvio_idade)
print(f'P(Idade > 50): {prob_idade_maior_50:.4f} ({prob_idade_maior_50 * 100:.2f}%)')

# P(20 <= Idade <= 30 anos)
prob_idade_20_a_30 = norm.cdf(30, loc=media_idade, scale=desvio_idade) - norm.cdf(20, loc=media_idade, scale=desvio_idade)
print(f'P(20 <= Idade <= 30): {prob_idade_20_a_30:.4f} ({prob_idade_20_a_30 * 100:.2f}%)')
