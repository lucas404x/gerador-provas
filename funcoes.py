from googlesearch import search
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from math import ceil

import _locale
import requests
import re
import os

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

def extrair_dados(sites, questao_resposta, diretorio):
    """
    função responsavel por extrair as questões/respostas do site Brasil Escola.
    sites: lista com as urls
    questao_resposta: 0 para extrair as questões e 1 para as respostas.
    diretorio: diretorio onde será salvo os dados
    """

    criar_pastas_prova(diretorio)

    indice_id_questao = 0
    tipo_dado = verificar_retornar_valor(questao_resposta)
    dados = {
                'identificador_questoes':[],
                    'dados':[]        
            }

    for site in sites:
        site_ = BeautifulSoup(site.text, features='html.parser')
        pattern = re.compile(tipo_dado[0])
        comparate = re.findall(pattern, str(site.text))
        
        if comparate:
            id_img, num_questao = 0, 0
            site = site_.find_all(attrs = {'class':comparate[0]})
            id_questoes = site_.find_all(attrs = {'class':tipo_dado[1]})
            for tag in site:
                dado = ''
                imagens = tag.find_all('img')
                paragrafos = tag.find_all('p')
                
                #extração das imagens
                # for imagem in imagens:
                #     img = requests.get(imagem['src'])
                #     img = Image.open(BytesIO(img.content))
                #     save = os.path.join(diretorio, 'imagens', tipo_dado + str(id_img))
                #     img.save('{}.png'.format(save))
                #     id_img += 1
                
                #extração do texto dos dados
                pos_questao = None
                for paragrafo in range(len(paragrafos)):
                    dados['dados'].append(paragrafos[paragrafo].text)
                    if paragrafo == 0:
                        pos_questao = len(dados['dados']) - 1
                
                dados['identificador_questoes'].append(id_questoes[num_questao].text)
                dados['identificador_questoes'] = atualizar_id_dado(dados['identificador_questoes'])
                
                dados['dados'][pos_questao] = dados['identificador_questoes'][indice_id_questao].capitalize() 
                + ' - ' 
                + dados['dados'][pos_questao]
                
                num_questao += 1
                indice_id_questao += 1
                
    return dados

def atualizar_id_dado(dados: list):
    id_atual = dados[-1][-1]
    dados[-1] = dados[-1].replace(id_atual, str(len(dados)))
    return dados

def verificar_retornar_valor(questao_resposta):
    """
    função responsavel por verificar se foi posto um valor valido no
    parametro questao_resposta e retorna o valor valido como uma string
    que vai ser usada no metodo extrair_dados.
    para ser valido, o número tem que ser 0 ou 1.
    """
    
    if questao_resposta == 0:
        return "(questoes-descricao)", "questoes-header"
    elif questao_resposta == 1:
        return "(resposta-descricao)", "resposta-header"
    return

def criar_pastas_prova(diretorio):
    
    try:
        os.mkdir(diretorio)
        os.mkdir(os.path.join(diretorio, 'imagens'))
    except Exception as e:
        print("Ocorreu um erro.",e)

def pega_diretorio():
    return os.path.join(filedialog.askdirectory(), "prova-questoes-respostas")

def trocar_caracter(string: str):

    string = list(string)
    old_caracter = string[-1]
    string[-1] = '-' if old_caracter.isalpha() else old_caracter
    return old_caracter, "".join(string)

def quebrar_linha(texto: str, limite: int):
    texto_divido = []
    loop = ceil(len(texto)/limite)

    for i in range(loop):
        old_texto = texto
        texto = trocar_caracter(texto[:limite]) # faz uma substring do inicio ao limite
        texto_divido.append(texto[1]) # adiciona o novo texto a lista
        if loop == 1:
            texto_divido.append(texto[0] + old_texto[limite:])
        texto = texto[0] + old_texto[limite:]

    return texto_divido
    
def escrever_prova(materia, assunto, dados, diretorio, nome_arquivo):
    """
    metodo que serve para escrever em um documento pdf as questoes ou respostas da atividade/prova.
    """

    TAMANHO_PAGINA = portrait(A4)

    setar_encoding('utf-8')
    nome_arquivo = nome_arquivo + '.pdf' if not 'pdf' in nome_arquivo else nome_arquivo
    pdf = canvas.Canvas(os.path.join(diretorio, nome_arquivo), pagesize = TAMANHO_PAGINA)
    pdf.setFont("Helvetica", 9)
    pdf.drawString((TAMANHO_PAGINA[0]/2) - 100, TAMANHO_PAGINA[1] - 35, "Prova de {} - {}".format(materia, assunto))
    y = TAMANHO_PAGINA[1] - 100 
    #id_questao = 1

    for i in range(len(dados)):
        if y <= (TAMANHO_PAGINA[1] + 10) - TAMANHO_PAGINA[1]:
            pdf.showPage()
            y = TAMANHO_PAGINA[1] - 35
            pdf.setFont("Helvetica", 9)
        
        if not dados[i] == "\n":
            if len(dados[i]) > 135:
                for texto in quebrar_linha(dados[i], 135):
                    pdf.drawString(10, y, "{}".format(texto))
                    y -= 30
                    if y <= (TAMANHO_PAGINA[1] + 10) - TAMANHO_PAGINA[1]:
                        pdf.showPage()
                        y = TAMANHO_PAGINA[1] - 35
                        pdf.setFont("Helvetica", 9)

            else:
                pdf.drawString(10, y, "{}".format(dados[i]))
                y -= 30
    
    pdf.save()
