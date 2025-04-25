# Modulo para controlar o navegador
from selenium import webdriver

# Localizador de elementos
from selenium.webdriver.common.by import By

# Serviço para configurar o caminho do executável chromedriver
from selenium.webdriver.chrome.service import Service

# Classe que permite executar ações avançadas, como por exemplo o mover o mouse, o click e arrasta e etc..
from selenium.webdriver.common.action_chains import ActionChains

# Classe que espera de forma explicita até que uma condição seja satisfeita
# Condição (ex: Que um elemento apareça)
from selenium.webdriver.support.ui import WebDriverWait

# Condições esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Trabalhar com DataFrame
import pandas as pd

# Uso de funções relacionadas ao tempo
import time 

from selenium.common.exceptions import TimeoutException

# Definir o caminho do chromeDriver 
chrome_driver_path = "c:\\Program Files\\chromedriver-win64\\chromedriver.exe" # Onde esta armazenado o caminho do driver

# configuração ao WebDriver
service = Service(chrome_driver_path) #navegador controlado pelo Selenium
options = webdriver.ChromeOptions() # configura opções do navegador
options.add_argument("--disable-gpu") # evita possíveis erros gráficos
options.add_argument("--window-size=1920,1080") # define uma resolução fixa

# incialização ao WebDriver
driver = webdriver.Chrome(service=service, options=options) # inicialização do navegador

# URl inicial
url_base = "https://www.kabum.com.br/audio/fone-de-ouvido/headphone"
driver.get(url_base)
time.sleep(5) # aguarda 5 segundos para garantir que a pág carregue

#criar um dicionário vazio para armazenar as marcas para armazenar as marcas e preços das cadeiras
dic_produtos = {"marca": [], "preco": []}

# vamos iniciar na página 1 e incrementos a cada troca de página
pagina = 1

while True:
    print(f"\n Coletando dados da página {pagina}...")

    try:
    #WebDriverWait(driver,10): cria uma espera de até 10 segundos
    #until: faz com que o código espere até que a condição seja verdadeira
    #ec.presence_of_all_elements_locatedverifica se todos os elementos "productCard" estão acessíveis
    #By.CLASS_NAME, "productCard": indica que a busca será feita através da classe css
        WebDriverWait(driver,10).until(
            ec.presence_of_element_located((By.CLASS_NAME, "productCard"))
        )
        print("Elementos encontrados com sucesso!")
    except TimeoutException:
        print("Tempo de espera execido!")

    produtos = driver.find_elements(By.CLASS_NAME, "productCard")

    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME, "nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME, "priceCard").text.strip()

            print(f"{nome} - {preco}")

            dic_produtos["marca"].append(nome)
            dic_produtos["preco"].append(preco)

        except Exception as e:
            print("Erro ao coletar dados:", e)

# Encontar botão da próxima página
    try:
        botao_proximo = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )
        if botao_proximo:
            driver.execute_script("arguments[0].scrollIntoView();", botao_proximo)
            time.sleep(1)

            # Clicar no botão
            driver.execute_script("arguments[0].click();", botao_proximo)
            print(f"Indo para a pagina {pagina}")
            pagina += 1

            time.sleep(1)

        else:
            print("Você chegou na ultima página")
            break
    
    except Exception as e:
        print("Erro ao tentar avançar para a próxima página", e)
        break


# Fechar o navegador
driver.quit()

# DataFrame
df = pd.DataFrame(dic_produtos)

# Salvar os dados em excel
df.to_excel("headphones.xlsx", index= False)

print(f"Arquivo 'headphones' salvo com sucesso! {len(df)} produtos capturados") 

