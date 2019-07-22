from googlesearch import search
from bs4 import BeautifulSoup

import requests, re

def buscar_links(materia, assunto):
    """
    função responsavel por buscar links no site da Brasil Escola.
    materia - materia a ser buscada.
    assunto - assunto a ser buscado.
    """

    urls = []
    
    try:
        for resultado in search(f"Brasil escola {materia} - {assunto} exercicios", stop = 5):
            if "brasilescola.uol.com.br" in resultado and "exercicios" in resultado:
                urls.append(resultado)
    
    except Exception as e:
        print("Não conseguimos acessar o site.", e)
    
    finally:
        return urls

def acessar_links(urls):
    """
    função responsavel por acessar os links do site da Brasil Escola.
    urls - vetor com N url.
    """

    sites = []

    for url in urls:
        try:
            site = requests.get(url)
        
        except Exception as e:
            print("Não conseguimos acessar o site.", e)

        else:
            sites.append(site)

    return sites


def extrair_questoes(site):
    """
    função que serve para extrair as questões do site Brasil escola.

    site - objeto do tipo request.
    """

    questoes = []

    site = BeautifulSoup(site.text, features='html.parser')
    pattern = re.compile("(questoes-descricao)")
    comparate = re.findall(pattern, str(site))

    if comparate:
        site = site.find_all(attrs={'class':comparate[0]})

        for questao_descricao in site:
            questao = ''
            paragrafos = questao_descricao.find_all('p')

            for paragrafo in paragrafos:
                questao += (paragrafo.text + '\n')
            
            questoes.append(questao)

    return questoes

def extrair_respostas(site):
    """
    função que serve para extrair as respostas do site Brasil escola.

    site - objeto do tipo request.
    """
    pass

def escrever_prova(materia, assunto, questoes_ou_respostas, tipo):
    """
    função que serve para escrever em um documento .txt as questoes ou respostas da atividade/prova.

    materia - materia escolhida;
    assunto - assunto escolhido;
    questoes_ou_respostas - vetor com as N questões ou respostas.
    tipo - string com a palavra "questões" ou "respostas", para diferenciar o texto.
    """

    with open(f'prova_{materia.lower()}_{assunto.lower()}_{tipo.lower()}.txt', 'w'
        , encoding="utf-8") as file:

        file.write(f'Prova de {materia.capitalize()} - {assunto.capitalize()}\n')
        file.write('\n')
            
        for i in range(len(questoes_ou_respostas)):
            file.write(f'{str(i + 1)} - {questoes_ou_respostas[i]}\n')
            file.write('\n')

if __name__ == "__main__":
    pass