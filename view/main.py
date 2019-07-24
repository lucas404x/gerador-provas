from tkinter import *
from controller.gerarProva import gerar_prova

class Main:

    def __init__(self):
        self.window = Tk()
        self.window_configure()
        self.create_frame()
        self.create_labels()
        self.create_entrys()
        self.create_buttons()
        self.package()
        self.window.mainloop()
    
    def window_configure(self):
        self.window.title("Janela Principal")
        self.window.geometry("500x300")
        #self.window['bg'] = "white"
        self.window.resizable(False, False)
    
    def create_frame(self):
        self.cabecalho = Frame(self.window)
        self.conteudo = Frame(self.window)
        self.frame_final = Frame(self.window)
    
    def create_entrys(self):
        self.entrada_materia = Entry(self.conteudo, 
        font = ("Arial", 12, "bold"), foreground = "green")
        self.entrada_assunto = Entry(self.conteudo, 
        font = ("Arial", 12, "bold"), foreground = "green")
    
    def create_labels(self):
        self.welcome = Label(self.cabecalho, text = 'Gerador de Provas', 
        bg = 'black', foreground = 'white', font = ('Arial', 14, 'bold'))
        self.label_materia = Label(self.conteudo, text = 'Matéria', 
        foreground = 'black', font = ('Arial', 11))
        self.label_assunto = Label(self.conteudo, text = 'Assunto', 
        foreground = 'black', font = ('Arial', 11))
    
    def create_buttons(self):
        self.clear_button = Button(self.frame_final, 
        text = "Limpar", command = self.clear)
        self.gerar_prova_button = Button(self.frame_final, 
        text = "Gerar Prova", command = gerar_prova)
        self.sair_button = Button(self.frame_final, 
        text = "Sair", command = lambda: self.window.destroy())
   
    def clear(self):
        self.entrada_materia.delete(0, END) 
        self.entrada_assunto.delete(0, END)
    
    def package(self):
        self.cabecalho.pack(pady = 8)
        self.conteudo.pack(pady = 16)
        self.welcome.pack()
        self.label_materia.pack()
        self.entrada_materia.pack()
        self.label_assunto.pack()
        self.entrada_assunto.pack()
        self.frame_final.pack()
        self.clear_button.pack(side = 'right', padx = 4)
        self.gerar_prova_button.pack(side = 'right', padx = 4)
        self.sair_button.pack(side = 'left', padx = 4)