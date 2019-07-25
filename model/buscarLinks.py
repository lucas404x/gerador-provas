from googlesearch import search

class BuscarLinks:

    def __init__(self, materia, assunto):
        self.materia = materia
        self.assunto = assunto
        
    def buscar_links(self):
        """
        metodo responsavel por buscar links no site da Brasil Escola.
        """

        urls = []
        
        try:
            for resultado in search(f"Brasil escola {self.materia} - {self.assunto} exercicios", stop = 5):
                if "brasilescola.uol.com.br" in resultado and "exercicios" in resultado:
                    urls.append(resultado)
        except Exception as e:
            raise e
        else:
            return urls