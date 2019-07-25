import requests

class AcessarLinks:

    def __init__(self, urls):
        self.urls = urls
    
    def acessar_links(self):
        
        """
        metodo responsavel por acessar os links do site da Brasil Escola.
        """
        
        sites = []
        
        for url in self.urls:
            try:
                site = requests.get(url)
            except Exception as e:
                raise e
            else:
                sites.append(site)
                    
        return sites
            