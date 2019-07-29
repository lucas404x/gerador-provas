from googlesearch import search
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from tkinter import filedialog

import requests
import re


def validar_url(url):
	"""
	função que serve verificar se a url pertence a sessão de exercicios da Brasil Escola.
	"""

	if "brasilescola.uol.com.br" in url and "exercicios" in url:
		return True
	return False


def buscar_links(materia, assunto):
	"""
	função responsavel por pesquisar os links do site da Brasil Escola.
	"""
	return [url for url in search("Brasil escola {} - {} exercicios".format(materia, assunto)
    , stop = 5) if validar_url(url)]


def acessar_links(urls):
	"""
	função responsavel por acessar os links do site da Brasil Escola.
	"""
	return [requests.get(site) for site in urls]

def extrair_dados(sites, questao_resposta):
    """
    função responsavel por extrair as questões/respostas do site Brasil Escola.
    questao_resposta: 0 para extrair as questões e 1 para as respostas.
    """
    
    tipo_dado = verificar_retornar_valor(questao_resposta)
    dados = []
    
    id_img = 0
    for site in sites:
        site_ = BeautifulSoup(site.text, features='html.parser')
        pattern = re.compile(tipo_dado)
        comparate = re.findall(pattern, str(site.text))
        
        if comparate:
            site_ = site_.find_all(attrs = {'class':comparate[0]})
            for tag in site_:
                dado = ''
                imagens = tag.find_all('img')
                paragrafos = tag.find_all('p')
                
                for imagem in imagens:
                    img = requests.get(imagem['src'])
                    img = Image.open(BytesIO(img.content))
                    img.save('{}.png'.format(id_img))
                    id_img += 1
                
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
    options = {'title': 'Salvar as {} em'.format(tipo), 
    'defaultextension':'.txt'}

    with  filedialog.asksaveasfile('w', **options) as file:
            file.write('Prova de {} - {}\n'.format(materia.capitalize(), assunto.capitalize()))
            file.write('\n')
            
            for i in range(len(dados)):
                file.write('{} - {}\n'.format(str(i + 1), dados[i]))
                file.write('\n')