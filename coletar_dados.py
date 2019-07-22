from googlesearch import search
from bs4 import BeautifulSoup
from PIL import Image

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

def verificar_parametro(questao_resposta):
    """
    função responsavel por verificar se foi posto um valor valido na
    função extrair_dados e retorna o valor valido como uma string
    que vai ser usada na função extrair_dados.

    questao_resposta - número inteiro
    """

    if questao_resposta == 0:
        return "(questoes-descricao)"
    
    elif questao_resposta == 1:
        return "(resposta-descricao)"
    
    else:
        raise "Tipo de dado para questao_resposta invalido."


def extrair_dados(site, questao_resposta):
    """
    função que serve para extrair as questões ou respostas do site Brasil escola.

    site - objeto do tipo request.
    questao_resposta - número inteiro: 0 para as questões ou 1 para as respostas
    """

    tipo_dado = verificar_parametro(questao_resposta)
    dados = []

    site = BeautifulSoup(site.text, features='html.parser')
    pattern = re.compile(tipo_dado)
    comparate = re.findall(pattern, str(site))

    if comparate:
        site = site.find_all(attrs={'class':comparate[0]})

        for tipo_de_dado in site:
            dado = ''
            paragrafos = tipo_de_dado.find_all('p')

            for paragrafo in paragrafos:
                dado += (paragrafo.text + '\n')
            
            dados.append(dado)

    return dados


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
    links = acessar_links(buscar_links("Geografia", "Neoliberalismo"))
    escrever_prova("Geografia", "Neoliberalismo", extrair_dados(links[0], 3), "questoes")
    escrever_prova("Geografia", "Neoliberalismo", extrair_dados(links[0], 1), "respostas")

    