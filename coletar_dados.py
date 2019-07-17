from googlesearch import BeautifulSoup, search
import requests, re

def buscar_links(materia, assunto):
    urls = []

    for resultado in search(f'"Brasil escola {materia} - {assunto} exercicios" stop = 5'):
        if "brasilescola.uol.com.br" in resultado and "exercicios" in resultado:
            urls.append(resultado)
    
    return urls

def extrair_questoes(urls):
    
    for url in urls:
        site = requests.get(url)
        site = BeautifulSoup(site.text, features='html.parser')
        pattern = re.compile("(questoes-descricao)")
        comparate = re.findall(pattern, str(site))

        if comparate:
            site = site.find(attrs={'class':comparate[0]})
            var = site.find_all('p')
            print(len(var))
            print(var[0].text)
        
        print("....")

def armazenar_questoes(questao):
    pass

def escrever_questoes(materia, assunto, questoes):

    with open(f'prova_{materia}.txt', 'w') as file:
        file.write(f'PROVA DE {materia.capitalize()} - {assunto.capitalize()}')

        for i in range(len(questoes)):
            file.write(f'{str(i + 1)} - {questoes[i]}\n')
            file.write('\n')

if __name__ == "__main__":
    urls = buscar_links(input("Materia: "), input("Assunto: "))
    print(urls)
    extrair_questoes(urls)
    #questoes = extrair_questoes(urls)
    #escrever_questoes('geografia', 'geopolitica', questoes)