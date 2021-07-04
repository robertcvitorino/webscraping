import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import json


#link url da pagina da NBA 
url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"
# Pega link do site da NBA e abre o navegador Firefox
option =Options()
option.headless=True
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get(url)
#Extraindo os dados do HTML
try:
    top10ranking={}
    #Aba da table refente aos seus filtros
    rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}
   #Ação de aceitar os termo de condição dos cookies
    acept_cookies=WebDriverWait(driver,5).until(
        EC.element_to_be_clickable((By.XPATH,"//*[@id='onetrust-accept-btn-handler']"))).click()
    time.sleep(10)

    def buildrank(type):
      field=rankings[type]['field']
      label=rankings[type]['label']
    #Clica no botao de filtro da tabela de jogadores 
      driver.find_element_by_xpath(f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()    
    #Retorna conteudo da tabela  
      element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
      html_content = element.get_attribute('outerHTML')
      #print(html_content)
    #Parsear o conteudo HTML para o BeautilfulSoup  
      soup = BeautifulSoup(html_content, 'html.parser')
      table = soup.find(name='table')
    #Estutua conteudo em um DataFrame com o pandas, conteudo buscado no HTML
      df_full = pd.read_html(str(table))[0].head(10)
    #Limpeza dos dados trazido HTML atravez dos nomes trazidos    
      df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM',label]]
      df.columns = ['pos', 'player', 'team','total']
     
      return df.to_dict('records')
    #Funcao para somente 1 ranking  
    ##top10ranking['points']=buildrank('points')
    #Percorre os ao rankings definidos e comforme o click relaizado na table sao parametrizados no dicionario de dados
    for k in rankings:
        top10ranking[k]=buildrank(k)

    #Salvando em arquivo Json 
    js=json.dumps(top10ranking)
    fp=open('ranking.json','w')
    fp.write(js)
    fp.close()

  


finally:
  #Fecha o navegador
    driver.quit()







