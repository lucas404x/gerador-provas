from googlesearch import search
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import _locale
import requests
import re

def setar_encoding(encoding):
    _locale._getdefaultlocale = (lambda *args: ['en_US', encoding])

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
                
                #extração das imagens
                for imagem in imagens:
                    img = requests.get(imagem['src'])
                    img = Image.open(BytesIO(img.content))
                    img.save('{}.png'.format(tipo_dado + str(id_img)))
                    id_img += 1
                
                #extração do texto dos dados
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

def pega_diretorio(tipo = ""):

    options = {'title': 'Salvar as {} em'.format(tipo) if tipo != "" else 'Salvar em', 
    'defaultextension':'.pdf'}

    with filedialog.asksaveasfile('w', **options) as file:
        diretorio = file.name
    
    return diretorio

def escrever_prova(materia, assunto, dados, diretorio):
    """
    metodo que serve para escrever em um documento pdf as questoes ou respostas da atividade/prova.
    dados - vetor com as N questões ou respostas;
    tipo - string com a palavra "questões" ou "respostas", para diferenciar o texto.
    """

    setar_encoding('utf-8')
    pdf = canvas.Canvas(diretorio, pagesize = letter)
    #pdf.setFont("Arial", 12)
    pdf.drawString((letter[0]/2) - 100, letter[1] - 35, "Prova de {} - {}".format(materia, assunto))
    y = letter[1] - 50

    for i in range(len(dados)):
        pdf.drawString(20, y, "{} - {}".format(i + 1, dados[i]))
        y -= 20
    
    pdf.save()
