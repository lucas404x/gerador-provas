from googlesearch import search
from bs4 import BeautifulSoup

import requests
import re


def validar_url(url: str):
	"""
	função que serve verificar se a url pertence a sessão de exercicios da Brasil Escola.
	"""

	if "brasilescola.uol.com.br" in url and "exercicios" in url:
		return True
	return False


def buscar_links(materia: str, assunto: str):
	"""
	função responsavel por pesquisar os links do site da Brasil Escola.
	"""
	return [url for url in search(f"Brasil escola {materia} - {assunto} exercicios", stop = 5)
	if validar_url(url)]


def acessar_links(urls: list):
	"""
	função responsavel por acessar os links do site da Brasil Escola.
	"""
	return [requests.get(site) for site in urls]

def extrair_dados(sites: list, questao_resposta: int):
    """
    função responsavel por extrair as questões/respostas do site Brasil Escola.
    questao_resposta: 0 para extrair as questões e 1 para as respostas.
    """
    
    tipo_dado = verificar_retornar_valor(questao_resposta)
    dados = []
    
    for site in sites:
        site_ = BeautifulSoup(site.text, features='html.parser')
        pattern = re.compile(tipo_dado)
        comparate = re.findall(pattern, str(site.text))
        
        if comparate:
            site_ = site_.find_all(attrs = {'class':comparate[0]})
            for tag in site_:
                dado = ''
                paragrafos = tag.find_all('p')
                for paragrafo in paragrafos:
                    dado += (paragrafo.text + '\n')
                
                dados.append(dado)
                
    return dados

def verificar_retornar_valor(questao_resposta):
    """
    metodo responsavel por verificar se foi posto um valor valido na
    atributo questao_resposta e retorna o valor valido como uma string
    que vai ser usada no metodo extrair_dados.
    para ser valido, o número tem que ser 0 ou 1.
    """
    
    if questao_resposta == 0:
        return "(questoes-descricao)"
    elif questao_resposta == 1:
        return "(resposta-descricao)"
    return

def escrever_prova(materia, assunto, dados, tipo):
    """
    metodo que serve para escrever em um documento .txt as questoes ou respostas da atividade/prova.
    dados - vetor com as N questões ou respostas;
    tipo - string com a palavra "questões" ou "respostas", para diferenciar o texto.
    """
    
    with open(f'prova_{materia.lower()}_{assunto.lower()}_{tipo.lower()}.txt', 'w'
        ,encoding="utf-8") as file:
            file.write(f'Prova de {materia.capitalize()} - {assunto.capitalize()}\n')
            file.write('\n')
            
            for i in range(len(dados)):
                file.write(f'{str(i + 1)} - {dados[i]}\n')
                file.write('\n')