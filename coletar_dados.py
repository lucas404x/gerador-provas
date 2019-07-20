from googlesearch import search
from bs4 import BeautifulSoup

import requests, re

def buscar_links(materia, assunto):
    urls = []
    
    try:
        for resultado in search(f'"Brasil escola {materia} - {assunto} exercicios" stop = 5'):
            if "brasilescola.uol.com.br" in resultado and "exercicios" in resultado:
                urls.append(resultado)
    
    except Exception as e:
        print("Não conseguimos acessar o site.", e)
    
    finally:
        return urls

def extrair_questoes(urls):
    questoes = []

    for url in urls:
        try:
            site = requests.get(url)
        except Exception as e:
            print("Não conseguimos acessar o site.", e)
            return

        site = BeautifulSoup(site.text, features='html.parser')
        pattern = re.compile("(questoes-descricao)")
        comparate = re.findall(pattern, str(site))

        if comparate:
            site = site.find_all(attrs={'class':comparate[0]})
            
            for i in site:
                questao = ''
                paragrafos = i.find_all('p')

                for paragrafo in paragrafos:
                    questao += (paragrafo.text + '\n')
                
                questoes.append(questao)
    
    return questoes

def escrever_questoes(materia, assunto, questoes):

    with open(f'prova_{materia.lower()}_{assunto.lower()}.txt', 'w') as file:
        file.write(f'Prova de {materia.capitalize()} - {assunto.capitalize()}\n')
        file.write('\n')
            
        for i in range(len(questoes)):
            file.write(f'{str(i + 1)} - {questoes[i]}\n')
            file.write('\n')

if __name__ == "__main__":

    materia = input("Materia: ")
    assunto = input("Assunto: ")
    
    print("pesquisando...")
    urls = buscar_links(materia, assunto)
    print("extraindo...")
    questoes = extrair_questoes(urls)
    print("escrevendo...")
    escrever_questoes(materia, assunto, questoes)