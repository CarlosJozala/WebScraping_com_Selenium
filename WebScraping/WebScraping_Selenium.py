#!/usr/bin/env python
# coding: utf-8

# # Automação Web e Busca de Informações com Python
# 
# #### Desafio: 
# 
# Trabalhamos em uma importadora e o preço dos nossos produtos é vinculado a cotação de:
# - Dólar
# - Euro
# - Ouro
# 
# Precisamos pegar na internet, de forma automática, a cotação desses 3 itens e saber quanto devemos cobrar pelos nossos produtos, considerando uma margem de contribuição que temos na nossa base de dados.
# 
# Base de Dados: https://drive.google.com/drive/folders/1KmAdo593nD8J9QBaZxPOG1yxHZua4Rtv?usp=sharing
# 
# Para isso, vamos criar uma automação web:
# 
# - Usaremos o selenium
# - Importante: baixar o webdriver

# ### Agora vamos atualiza a nossa base de preços com as novas cotações

# In[28]:


#!pip install selenium


# In[29]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Abrir o Navegador
navegador = webdriver.Edge()

# Entrar no google

navegador.get("https://www.google.com.br/")

# pesquisar cotacao dolar no google

navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação dólar")

navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

# Pegar a cotação do Dolar

cotacao_dolar = navegador.find_element('xpath',
                       '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

print(cotacao_dolar)

# Passo 2 pegar a cotação do Euro

navegador.get("https://www.google.com.br/")

# pesquisar cotacao euro no google

navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação euro")

navegador.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)

# Pegar a cotação do Dolar

cotacao_euro = navegador.find_element('xpath',
                       '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')

print(cotacao_euro)

# Passo 3 pegar a cotação do Ouro

navegador.get("https://www.melhorcambio.com/ouro-hoje")

cotacao_ouro = navegador.find_element('xpath','//*[@id="comercial"]').get_attribute('value')

cotacao_ouro = cotacao_ouro.replace(",",".")

print(cotacao_ouro)

navegador.quit()


# - Importando a base de dados

# In[30]:


# Passo 4 atualizar a base de dados

import pandas as pd

tabela = pd.read_excel("Produtos.xlsx")

display(tabela)


# - Atualizando os preços e o cálculo do Preço Final

# In[31]:


# Passo 5 recalcular os preços

# Atualizar as cotações

tabela.loc[tabela["Moeda"] =="Dólar", "Cotação"] = float(cotacao_dolar)
tabela.loc[tabela["Moeda"] =="Euro", "Cotação"] = float(cotacao_euro)
tabela.loc[tabela["Moeda"] =="Ouro", "Cotação"] = float(cotacao_ouro)

# Preço de compra = Preço Original x Cotação

tabela["Preço de Compra"] = tabela["Preço Original"] = tabela["Cotação"]

# Preço de venda = Preço de Compra x Margem

tabela["Preço de Venda"] = tabela["Preço de Compra"] = tabela ["Margem"]

display(tabela)


# ### Agora vamos exportar a nova base de preços atualizada

# In[32]:


# Passo 6 exportar a base de dados

tabela.to_excel("Produtos Novo.xlsx", index=False)

