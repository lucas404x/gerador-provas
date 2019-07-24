
class BuscarLinks:

    def __init__(self, materia, assunto):
        self.materia = materia
        self.assunto = assunto
        
    def buscar_links(self, materia, assunto):
        from googlesearch import search
    
        """
        metodo responsavel por buscar links no site da Brasil Escola.
        materia - materia a ser buscada.
        assunto - assunto a ser buscado.
        """

        urls = []
        
        try:
            for resultado in search(f"Brasil escola {materia} - {assunto} exercicios", stop = 5):
                if "brasilescola.uol.com.br" in resultado and "exercicios" in resultado:
                    urls.append(resultado)
        except Exception as e:
            print("Não conseguimos acessar o site.", e)
        finally:
            return urls