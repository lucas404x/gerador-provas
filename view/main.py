from tkinter import *

class Main:

    def __init__(self):
        self.window = Tk()
        self.window_configure()
        self.create_frame()
        self.create_buttons_labels_entry()
        self.package()
        self.window.mainloop()
    
    def window_configure(self):
        self.window.title("Janela Principal")
        self.window.geometry("600x400")
        self.window.resizable(False, False)
    
    def create_frame(self):
        self.cabecalho = Frame(self.window)
        self.conteudo = Frame(self.window)
        self.botoes = Frame(self.window)
    
    def create_buttons_labels_entry(self):
        self.welcome = Label(self.cabecalho, text = 'Gerador de Provas', 
        bg = 'black', foreground = 'white', font = ('Arial', 14, 'bold'))
        self.entrada_label = Label(self.conteudo, text = 'Número de provas', 
        foreground = 'black', font = ('Arial', 11))
        self.entrada_provas = Entry(self.conteudo, justify = 'center', 
        font = ('Arial', 12, 'bold'), foreground = 'green')
    
    def package(self):
        self.cabecalho.pack(pady = 12)
        self.conteudo.pack(pady = 32)
        self.welcome.pack()
        self.entrada_label.pack()
        self.entrada_provas.pack()

        self.botoes.pack()