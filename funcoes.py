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

    indice_id_dado = 0
    diretorio_img = os.path.join(diretorio, 'imagens')
    id_img = len(os.listdir(diretorio_img))
    tipo_dado = verificar_retornar_valor(questao_resposta)
    dados = {
                'dados':[],
                'identificador_dados':[],
                'tamanho_imagens':[],
                'inicio_dado':str(id_img) + '.png'
            }

    for site in sites:
        site_ = BeautifulSoup(site.text, features='html.parser')
        pattern = re.compile(tipo_dado[0])
        comparate = re.findall(pattern, str(site.text))
        
        if comparate:
            num_dado = 0
            site = site_.find_all(attrs = {'class':comparate[0]})
            id_dados = site_.find_all(attrs = {'class':tipo_dado[1]})
            for tag in site:
                dado = ''
                imagens = tag.find_all('img')
                paragrafos = tag.find_all('p')
                
                # extração das imagens

                for imagem in imagens:
                    img = requests.get(imagem['src'])
                    img = Image.open(BytesIO(img.content))
                    try:
                        tamanho_imagem = imagem['style']
                    except KeyError:
                        tamanho_imagem = (int(imagem['width']), int(imagem['height']))
                    else:
                        tamanho_imagem = extrair_dimensoes(tamanho_imagem)
                    
                    dados['tamanho_imagens'].append((tamanho_imagem[0], tamanho_imagem[1]))
                    save = os.path.join(diretorio_img, str(id_img))
                    img.save('{}.png'.format(save))
                    id_img += 1

                #extração do texto dos dados
                
                pos_dado = None
                for paragrafo in range(len(paragrafos)):
                    dados['dados'].append(paragrafos[paragrafo].text)
                    if paragrafo == 0:
                        pos_dado = len(dados['dados']) - 1
                
                dados['identificador_dados'].append(id_dados[num_dado].text)
                dados['identificador_dados'] = atualizar_id_dado(dados['identificador_dados'])
                
                dados['dados'][pos_dado] = dados['identificador_dados'][indice_id_dado].capitalize() + ' - ' + dados['dados'][pos_dado]
                
                num_dado += 1
                indice_id_dado += 1
                
    return dados

def extrair_dimensoes(dimensoes: str):
    padrao = r'\d+'
    return converter_tipo_elementos(re.findall(padrao, dimensoes), int)

def converter_tipo_elementos(lista: str, tipo_primitivo):
    return [tipo_primitivo(elemento) for elemento in lista]

def atualizar_id_dado(dados: list):
    ultimo_id = dados[-1][-1]
    dados[-1] = dados[-1].replace(ultimo_id, str(len(dados)))
    return dados

def verificar_retornar_valor(questao_resposta):
    """
    função responsavel por verificar se foi posto um valor valido no
    parametro questao_resposta e retorna o valor valido como uma string
    que vai ser usada no metodo extrair_dados.
    para ser valido, o número tem que ser 0 ou 1.
    """
    
    if questao_resposta == 0:
        return "(questoes-descricao)", "questoes-header", "questao"
    elif questao_resposta == 1:
        return "(resposta-descricao)", "resposta-header", "resposta"
    return

def criar_pastas_prova(diretorio, nome_pasta):
    try:
        os.mkdir(os.path.join(diretorio, nome_pasta))
        os.mkdir(os.path.join(diretorio, nome_pasta, 'imagens'))
    except Exception as e:
        print("Ocorreu um erro.",e)

def pega_diretorio():
    return filedialog.askdirectory()

def extrair_imagens(diretorio):
    return os.listdir(diretorio)

def dividir(path_or_file, caracter):
    indice = path_or_file.rfind(caracter)
    return path_or_file[:indice]

def ordernar_imagens(imagens):
    imagens_ordenadas = [int(dividir(imagem, '.')) for imagem in imagens]
    imagens_ordenadas.sort()
    return [str(imagem) + '.png' for imagem in imagens_ordenadas]

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

def escrever_prova(materia, assunto, dados, diretorio):
    """
    metodo que serve para escrever em um documento pdf as questoes ou respostas da atividade/prova.
    """

    TAMANHO_PAGINA = portrait(A4)
    setar_encoding('utf-8')
    diretorio = diretorio + '.pdf' if not diretorio.rfind('.pdf') else diretorio
    diretorio_imgs = os.path.join(dividir(diretorio, '/'), 'imagens')
    imagens = ordernar_imagens(extrair_imagens(diretorio_imgs))
    primeira_img = imagens.index(dados['inicio_dado'])
    imagens = imagens[primeira_img:]
    pdf = canvas.Canvas(diretorio, pagesize = TAMANHO_PAGINA)
    pdf.setFont("Helvetica", 12)
    pdf.drawString((TAMANHO_PAGINA[0]/2) - 100, TAMANHO_PAGINA[1] - 35, "Prova de {} - {}".format(materia, assunto))
    pdf.setFont("Helvetica", 9)
    y = TAMANHO_PAGINA[1] - 100
    id_img = 0

    for i in range(len(dados['dados'])):
        if y <= (TAMANHO_PAGINA[1] + 10) - TAMANHO_PAGINA[1]:
            pdf.showPage()
            y = TAMANHO_PAGINA[1] - 35
            pdf.setFont("Helvetica", 9)

        if len(dados['dados'][i]) > 135:
            for texto in quebrar_linha(dados['dados'][i], 135):
                if y <= (TAMANHO_PAGINA[1] + 10) - TAMANHO_PAGINA[1]:
                    pdf.showPage()
                    y = TAMANHO_PAGINA[1] - 35
                    pdf.setFont("Helvetica", 9)
                pdf.drawString(10, y, "{}".format(texto)) 
                y -= 25
            
        elif not dados['dados'][i] == '':
            pdf.drawString(10, y, "{}".format(dados['dados'][i]))
            y -= 25
                
        else:
            y -= 100
            pdf.drawImage(os.path.join(diretorio_imgs, imagens[id_img]), 10, y, 
            width = dados['tamanho_imagens'][id_img][0], height = dados['tamanho_imagens'][id_img][1])
            id_img += 1
            y -= 25
    
    pdf.save()
