
class GerarProva:
    
    def __init__(self, materia, assunto):
        self.materia = materia
        self.assunto = assunto

    def escrever_prova(self, dados, tipo):
        """
        metodo que serve para escrever em um documento .txt as questoes ou respostas da atividade/prova.
        
        dados - vetor com as N questões ou respostas;
        tipo - string com a palavra "questões" ou "respostas", para diferenciar o texto.
        """

        with open(f'prova_{self.materia.lower()}_{self.assunto.lower()}_{tipo.lower()}.txt', 'w'
            , encoding="utf-8") as file:

            file.write(f'Prova de {self.materia.capitalize()} - {self.assunto.capitalize()}\n')
            file.write('\n')
                
            for i in range(len(dados)):
                file.write(f'{str(i + 1)} - {dados[i]}\n')
                file.write('\n')