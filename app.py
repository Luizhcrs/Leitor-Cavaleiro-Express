import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import base64
from conexão import *



conexao= Banco()
def limpar_consulta():
    descricao.config(text='')
    resultado.config(text='') 
def consultar_preco(*args):
    produto = pesquisa.get()
    descricaos = conexao.consultar_nome(produto)
    codigo_interno = conexao.consultar_cod(produto)
    preco = conexao.consultar_prec(codigo_interno)
    if preco:
        descricao['text'] = f'{descricaos}'
        resultado['text'] = f'R$ {preco}'
        #pesquisa.delete(0, tk.END)
        resultado.pack()
        pesquisa.delete(0, tk.END)
        janela.after(8000, limpar_consulta)
    else:
        descricao['text'] = ''
        resultado['text'] = 'Produto não encontrado'
        pesquisa.delete(0, tk.END)
        janela.after(8000, limpar_consulta)
        

      
      
    
janela = tk.Tk()
janela.attributes("-fullscreen", True)
janela.title("Consulta de Preços")
janela.geometry("1920x1080")
janela.config(background="#f7ae40")

fundo = tk.Label(janela, background='#4074f7')
fundo.pack(side="top", fill="both", expand="True")


# Adicionando título da aplicação
titulo = ttk.Label(janela, text='CONSULTA PREÇO', font=("Arial", 80, "bold"),foreground='white',background="#f7ae40" )
titulo.pack(pady=100)




# Adicionando uma caixa de pesquisa
pesquisa = ttk.Entry(janela, width=20,font=("TkDefaultFont",10),background="#f7ae40" )
pesquisa.pack(pady=30)

# Adicionando a descrição do produto
descricao = ttk.Label(janela, text='', font=("TkDefaultFont", 30),background="#f7ae40")
descricao.pack(pady=10)

# Adicionando a exibição do preço
resultado = ttk.Label(janela, text='', font=("Arial", 80, "bold"),background="#f7ae40")
resultado.pack(pady=30)



# Colocando o foco na caixa de pesquisa
pesquisa.focus_set()

# Evento de pesquisa ao pressionar a tecla Enter
janela.bind('<Return>', consultar_preco)


img = Image.open("C:/Users/luizg/OneDrive/Documentos/BuscaPreço/fundo.png")
resize_image = img.resize((450, 150))
# img = img.resize((janela.winfo_screenwidth(), janela.winfo_screenheight()), Image.ANTIALIAS)
img = ImageTk.PhotoImage(resize_image)

imagem = tk.Label(janela, image=img,background='#f7ae40')
imagem.pack(side="bottom", fill="both", expand="yes")


janela.mainloop()
