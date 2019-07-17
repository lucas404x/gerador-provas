from googlesearch import search

pesquisa = input()

for resultado in search(f'"questoes de {pesquisa}" google', stop=12):
    print(resultado)