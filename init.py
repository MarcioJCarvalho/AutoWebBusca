# biblioteca Selenium: controla o navegador
# 1ª instalar o selenium
# 2º baixar o webdriver

# criação do navegador
from pandas.io.sql import table_exists
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import pandas as pd
s = Service("D:\Faculdade\Inensivão de Python\AULA-03\AutoWebBuscaInfo\chromedriver.exe") # usado assim caso o chromedriver estiver na mesma pasta da aplicação em python
navegador = webdriver.Chrome(service = s)

# Baixar o arquivo inicial
# Baixar a base de dados

# Passo 1: pegar a cotação do dolar
navegador.get("https://www.google.com/")
navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/div[2]/input').send_keys("cotação dolar")
navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/div[2]/input').send_keys(Keys.ENTER)
cotacao_dolar = navegador.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
print(cotacao_dolar)

# Passo 2: pegar a cotação do euro
# limpando o buscador
navegador.find_element(By.XPATH, '/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/div[2]/div/div[3]/div[1]/span[1]').send_keys(Keys.ENTER)
navegador.find_element(By.XPATH, '/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/div[2]/div/div[2]/input').send_keys("cotação euro")
navegador.find_element(By.XPATH, '/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/div[2]/div/div[2]/input').send_keys(Keys.ENTER)
cotacao_euro = navegador.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')
print(cotacao_euro)

# Passo 3: pegar a cotação do ouro
navegador.get("https://www.melhorcambio.com/ouro-hoje")
cotacao_ouro = navegador.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div/input[2]').get_attribute("value")
cotacao_ouro = cotacao_ouro.replace(",", ".")
print(cotacao_ouro)

# fechando o navegador
navegador.quit()

# Passo 4: importar e atualizar as cotações na base de dados
tabela = pd.read_excel("D:\Faculdade\Inensivão de Python\AULA-03\AutoWebBuscaInfo\Produtos.xlsx")
print(tabela)

# Passo 5: Calcular os novos preços e salvar/exportar a base de dados 
# isso no pandas é a mesma coisa que fize-se um if para comparar se a moéda for igual a dolar preenche com a cotação do dolar
tabela.loc[tabela['Moeda'] == 'Dólar', 'Cotação'] = float(cotacao_dolar)
tabela.loc[tabela['Moeda'] == 'Euro', 'Cotação'] = float(cotacao_euro)
tabela.loc[tabela['Moeda'] == 'Ouro', 'Cotação'] = float(cotacao_ouro)

# atualizar as colunas
# preço de compra = preço original * cotação
tabela["Preço de Compra"] = tabela["Preço Original"] * tabela["Cotação"]

# preço de venda = preço compra * margem
tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]


# exportando a tabela
# index=False para não pegar os indices com python
tabela.to_excel("D:\Faculdade\Inensivão de Python\AULA-03\AutoWebBuscaInfo\Produtos Novo.xlsx", index=False)
nova_tabela = pd.read_excel("D:\Faculdade\Inensivão de Python\AULA-03\AutoWebBuscaInfo\Produtos Novo.xlsx")
print(nova_tabela )