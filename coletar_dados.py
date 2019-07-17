from googlesearch import BeautifulSoup, search
import requests, re

def buscar_links(materia, assunto):
    urls = []

    for resultado in search(f'"Brasil escola {materia} - {assunto} exercicios" stop = 5'):
        if re.search('brasilescola.uol.com.br', resultado):
            urls.append(resultado)
    
    return urls

if __name__ == "__main__":
    urls = buscar_links("geografia", "geopolitica")
    print(urls)