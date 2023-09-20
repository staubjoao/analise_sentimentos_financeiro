import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sys


headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"}

def scrape_specific_news(url):
    req = urllib.request.Request(url=url, headers=headers) 
    resp = urllib.request.urlopen(req)

    status_code = resp.getcode()  # Obtenha o código de status HTTP

    if status_code == 200:
        soup = BeautifulSoup(resp, 'html.parser')

        titulo = soup.find('h1', class_='articleHeader').text

        span_data_hora = soup.find_all('div', class_='contentSectionDetails')

        data = None
        hora = None
        for elemento_span in span_data_hora:
            span_text = elemento_span.get_text(strip=True)
            if 'Publicado' in span_text:
                aux = span_text.split('Atualizado')
                aux = aux[0].split('Publicado')
                aux = aux[1].split(' ')
                data, hora = aux[1], aux[2]

        corpo = soup.find('div', class_='articlePage')
        textos = corpo.find_all('p')

        texto = []
        for i, txt in enumerate(textos):
            if txt.find('strong') != None:
                break
            
            if 'Posição adicionada com êxito a' not in txt.text:
                texto.append(txt.text)
                
        if len(texto) <= 1:
            return None

        print(data, hora)
        print(titulo)
        print(texto)

        print()

        noticia = {
            "titulo": titulo,
            "data": data,
            "hora": hora,
            "texto": texto,
        }
    
        return noticia
    else:
        print(f'Erro ao acessar a página: {status_code}')
        return None

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def scrape_investing_news(url):
    # Fazer a solicitação HTTP para a página de notícias da ação
    req = urllib.request.Request(url=url, headers=headers) 
    resp = urllib.request.urlopen(req)
    
    status_code = resp.getcode()  # Obtenha o código de status HTTP
    
    if status_code == 200:
        soup = BeautifulSoup(resp, 'html.parser')
        
        # Encontrar os elementos que contêm as notícias
        news_elements = soup.find_all('div', class_='mb-4')

        news_element = news_elements[0]

        news_elements = news_element.find('ul')

        links = news_elements.find_all('a', href=True)
        
        news = []

        for link in links:
            aux = link['href']
            aux = aux.split("#")
            aux = aux[0]
            news.append(aux)
        news = f7(news)
        return ((len(news)), news)

    else:
        print(f'Erro ao acessar a página: {status_code}')
        return 0

def scrape_investing_news_period(url, inicio, dias):
    # Fazer a solicitação HTTP para a página de notícias da ação
    req = urllib.request.Request(url=url, headers=headers) 
    resp = urllib.request.urlopen(req)
    
    status_code = resp.getcode()  # Obtenha o código de status HTTP
    
    if status_code == 200:
        soup = BeautifulSoup(resp, 'html.parser')
        
        # Encontrar os elementos que contêm as notícias
        news_elements = soup.find_all('div', class_='mb-4')

        news_element = news_elements[0]

        news_elements = news_element.find('ul')

        links = news_elements.find_all('a', href=True)
        
        news = []

        for link in links:
            aux = link['href']
            aux = aux.split("#")
            aux = aux[0]
            news.append(aux)
        news = f7(news)
        return ((len(news)), news)

    else:
        print(f'Erro ao acessar a página: {status_code}')
        return 0
    
def main():
    if len(sys.argv) == 1:
        print("Utilize 'web_scraping.py -h' para listar os comandos")
        sys.exit(1)
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            print('Utilize \'-all\' para realizar o web_scraping de todos')
            print('Utilize \'-d <data>\' para definir a data da noticia que deseja com')
    urls_noticias = ["magaz-luiza-on-nm-news", "b2w-varejo-on-nm-news", "petrobras-pn-news"]
    cod_noticias = ["MGLU3", "AMER3", "PETR4"]

    for i in range(len(urls_noticias)): 
        print(f"Notícias do {cod_noticias[i]}\n")
        cont = 50
        cont_aux = cont
        noticias = []
        pag_noticias = 1

        while cont > 0:
            res = scrape_investing_news(f"https://br.investing.com/equities/{urls_noticias[i]}/{pag_noticias}")

            if res == None:
                print("Teste")
                continue
            else:
                aux = res[0]
                urls = res[1]
                for j in range(aux):
                    print(f"indice: {cont_aux-cont}\n")
                    informacao = scrape_specific_news('https://br.investing.com' + urls[j])
                    if informacao != None:
                        noticias.append(informacao)
                        cont -= 1
                        if cont == 0:
                            break
                pag_noticias += 1
        df = pd.DataFrame(noticias)
        arquivo = f"{cod_noticias[i]}.csv"
        df.to_csv(arquivo)

if __name__ == "__main__":
    main()