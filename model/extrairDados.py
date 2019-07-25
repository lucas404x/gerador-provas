from bs4 import BeautifulSoup
import requests, re

class ExtrairDados:

    def __init__(self, sites):
        """
        sites - vetor com os N sites em forma de requests object.
        """
        self.sites = sites
        
    def extrair_dados(self, questao_resposta):
        """
        metodo que serve para extrair as questões ou respostas do site Brasil escola.
        questao_resposta - 1 se quiser as respostas ou 0 para as questões.
        """

        tipo_dado = self.__verificar_atributo__(questao_resposta)
        dados = []

        for site in self.sites:
            site_ = BeautifulSoup(site.text, features='html.parser')
            pattern = re.compile(tipo_dado)
            comparate = re.findall(pattern, str(site.text))

            if comparate:
                site_ = site_.find_all(attrs={'class':comparate[0]})

                for tipo_de_dado in site_:
                    dado = ''
                    paragrafos = tipo_de_dado.find_all('p')

                    for paragrafo in paragrafos:
                        dado += (paragrafo.text + '\n')
                    
                    dados.append(dado)

        return dados
    
    def __verificar_atributo__(self, questao_resposta):
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
        
        raise ValueError