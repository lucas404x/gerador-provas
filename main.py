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
    diretorio = pega_diretorio()
    questoes = extrair_dados(sites, 0, diretorio)
    respostas = extrair_dados(sites, 1, diretorio)
    print("----------------------")
    print("Escrevendo a prova...")
    
    escrever_prova(materia, assunto, questoes['dados'], diretorio, 
    "questoes_{}_{}".format(materia, assunto))

    escrever_prova(materia, assunto, respostas['dados'], diretorio, 
    "respostas_{}_{}".format(materia, assunto))
    
    acompanha_texto("Terminado!")