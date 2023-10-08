import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime



headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"}

def scrape_specific_news(url):
    try:
        # print(url)
        req = urllib.request.Request(url=url, headers=headers) 
        resp = urllib.request.urlopen(req)

        status_code = resp.getcode() 

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

            # print(data, hora)
            # print(url)
            # print(texto)
            # print(data)

            # print()

            noticia = {
                "url": url,
                "titulo": titulo,
                "data_hora": f'{data} {hora}',
                "texto": texto,
            }

        
            return noticia
    except Exception as inst:
        print(f'Erro ao acessar a página: {status_code} - {inst}')
        return None

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def scrape_investing_news(url):
    req = urllib.request.Request(url=url, headers=headers) 
    resp = urllib.request.urlopen(req)
    
    status_code = resp.getcode()
    
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
    urls_noticias = ["magaz-luiza-on-nm-news", "b2w-varejo-on-nm-news", "petrobras-pn-news"]
    cod_noticias = ["MGLU3_3", "AMER3_3", "PETR4_3"]

    for i in range(len(urls_noticias)): 
        print(f"Notícias do {cod_noticias[i]}\n")
        cont = 25
        cont_aux = cont
        noticias = []
        pag_noticias = 1

        data_inicial = datetime.datetime.strptime('5.10.2023', '%d.%m.%Y')

        while cont > 0:
            res = scrape_investing_news(f"https://br.investing.com/equities/{urls_noticias[i]}/{pag_noticias}")

            if res == None:
                continue
            else:
                aux = res[0]
                urls = res[1]
                for j in range(aux):
                    informacao = scrape_specific_news('https://br.investing.com' + urls[j])
                    print(f"indice: {cont_aux-cont}\n")
                    if informacao != None and 'data_hora' in informacao:
                        data_aux = informacao['data_hora'].split(' ')
                        data_noticia = datetime.datetime.strptime(data_aux[0], '%d.%m.%Y')

                        if data_inicial is None or (data_inicial - data_noticia).days >= 3:
                            if data_inicial != None:
                                print("diferença", (data_inicial - data_noticia).days)
                            noticias.append(informacao)
                            data_inicial = data_noticia 
                            print(data_noticia)
                            cont -= 1
                            if cont == 0:
                                break
                pag_noticias += 1
        df = pd.DataFrame(noticias)
        arquivo = f"{cod_noticias[i]}.csv"
        df.to_csv(arquivo)

if __name__ == "__main__":
    main()