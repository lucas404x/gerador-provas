import requests

class ExtrairDados:

    def __init__(self, site, questao_resposta):
        self.site = site
        self.questao_resposta = self.__verificar_atributo__(questao_resposta)
        
    def extrair_dados(self):
        """
        metodo que serve para extrair as questões ou respostas do site Brasil escola.
        """

        tipo_dado = self.questao_resposta
        dados = []

        site = BeautifulSoup(self.site.text, features='html.parser')
        pattern = re.compile(tipo_dado)
        comparate = re.findall(pattern, str(self.site))

        if comparate:
            site = site.find_all(attrs={'class':comparate[0]})

            for tipo_de_dado in site:
                dado = ''
                paragrafos = tipo_de_dado.find_all('p')

                for paragrafo in paragrafos:
                    dado += (paragrafo.text + '\n')
                
                dados.append(dado)

        return dados
    
    def __verificar_atributo__(self, questao_resposta):
        """
        metodo responsavel por verificar se foi posto um valor valido na
        metodo extrair_dados e retorna o valor valido como uma string
        que vai ser usada no metodo extrair_dados.
        """

        if questao_resposta == 0:
            return "(questoes-descricao)"
        
        elif questao_resposta == 1:
            return "(resposta-descricao)"
        
        raise "Atributo invalido."