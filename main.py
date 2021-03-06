from funcoes import *

def acompanha_texto(string: str):
    
    print("=" * len(string))
    print(string)
    print("=" * len(string))

def main():

    acompanha_texto("Gerador de Provas")
    materia = input("Matéria: ").lower()
    assunto = input("Assunto: ").lower()
    print("----------------------")
    print("Buscando links...")
    links = buscar_links(materia, assunto)
    print("----------------------")
    print("Acessando os links...")
    sites = acessar_links(links)
    print("----------------------")
    print("Extraindo dados...")
    diretorio = pega_diretorio()
    nome_pasta =  "prova-de-{}-{}".format(materia, assunto)
    criar_pastas_prova(diretorio, nome_pasta)
    questoes = extrair_dados(sites, 0, os.path.join(diretorio, nome_pasta))
    respostas = extrair_dados(sites, 1, os.path.join(diretorio, nome_pasta))
    print("----------------------")
    print("Escrevendo a prova...")
    
    escrever_prova(materia, assunto, questoes, os.path.join(diretorio, nome_pasta, 'questões-{}-{}.pdf'.format(materia, assunto)))
    escrever_prova(materia, assunto, respostas, os.path.join(diretorio, nome_pasta, 'respostas-{}-{}.pdf'.format(materia, assunto)))
    
    acompanha_texto("Terminado!")