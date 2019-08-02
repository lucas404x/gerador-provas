from funcoes import *

def acompanha_texto(string):
    
    print("=" * len(string))
    print(string)
    print("=" * len(string))

def main():

    acompanha_texto("Gerador de Provas")
    materia = input("Matéria: ")
    assunto = input("Assunto: ")
    print("----------------------")
    print("Buscando links...")
    links = buscar_links(materia, assunto)
    print("----------------------")
    print("Acessando os links...")
    sites = acessar_links(links)
    print("----------------------")
    print("Extraindo dados...")
    questoes = extrair_dados(sites, 0)
    respostas = extrair_dados(sites, 1)
    print("----------------------")
    print("Escrevendo a prova...")
    escrever_prova(materia, assunto, questoes, pega_diretorio("questões"))
    escrever_prova(materia, assunto, respostas, pega_diretorio("respostas"))
    acompanha_texto("Terminado!")