import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from conexão import *
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para verificar a conexão com a internet
def verificar_conexao():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        logging.error(f"Erro ao verificar a conexão: {e}")
        return False

# Função para atualizar o indicador de conexão
def atualizar_indicador_conexao(canvas_indicador):
    if verificar_conexao():
        cor = 'green'
    else:
        cor = 'red'
    canvas_indicador.delete("all")
    canvas_indicador.create_oval(5, 5, 15, 15, fill=cor, outline=cor)

def resize_panfleto_image(image, screen_width, screen_height, base_width=519, base_height=519):
    base_screen_width = 1920
    base_screen_height = 1080
    width_ratio = screen_width / base_screen_width
    height_ratio = screen_height / base_screen_height
    new_width = int(base_width * width_ratio)
    new_height = int(base_height * height_ratio)
    return image.resize((new_width, new_height), Image.LANCZOS)

def resize_background_image(image, screen_width, screen_height):
    return image.resize((screen_width, screen_height), Image.LANCZOS)

def create_main_window():
    output_folder = 'downloads'
    
    root = tk.Tk()
    root.title("Aplicação Tkinter com TTK")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.attributes("-fullscreen", True)

    canvas = tk.Canvas(root, width=screen_width, height=screen_height, bd=0, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Canvas para o indicador de conexão com fundo na cor desejada
    canvas_indicador = tk.Canvas(root, width=20, height=20, bg='#121cba', bd=0, highlightthickness=0)
    canvas_indicador.place(x=10, y=screen_height - 30, anchor="sw")  # Ajusta a posição no canto inferior esquerdo

    background_path = "background.png"
    if not os.path.exists(background_path):
        logging.error(f"Erro: {background_path} não encontrado.")
        return
    background_image = Image.open(background_path)
    background_image_resized = resize_background_image(background_image, screen_width, screen_height)
    background_photo = ImageTk.PhotoImage(background_image_resized)
    canvas.create_image(0, 0, anchor="nw", image=background_photo, tags="background")

    image_files = []
    current_image_index = 0

    def load_images():
        return [f for f in os.listdir(output_folder) if f.endswith('.jpg')]

    def update_panfleto_image():
        nonlocal current_image_index, image_files
        if not image_files:
            logging.info("Nenhuma imagem disponível para exibir.")
            return

        if current_image_index >= len(image_files):
            current_image_index = 0

        image_path = os.path.join(output_folder, image_files[current_image_index])
        panfleto_image = Image.open(image_path)
        panfleto_image_resized = resize_panfleto_image(panfleto_image, screen_width, screen_height)
        panfleto_photo = ImageTk.PhotoImage(panfleto_image_resized)

        canvas.create_image(947, 332, anchor="nw", image=panfleto_photo, tags="panfleto")
        canvas.image_panfleto = panfleto_photo

        current_image_index = (current_image_index + 1) % len(image_files)
        root.after(5000, update_panfleto_image)

    def check_for_changes():
        nonlocal image_files, current_image_index
        try:
            new_image_files = load_images()
            if sorted(image_files) != sorted(new_image_files):
                image_files = new_image_files
                if image_files:
                    current_image_index = 0
                    update_panfleto_image()
                else:
                    canvas.delete("panfleto")
                    current_image_index = 0
        except Exception as e:
            logging.error(f"Erro ao verificar alterações: {e}")
        root.after(60000, check_for_changes)  # Check every 60 seconds

    image_files = load_images()
    if image_files:
        update_panfleto_image()

    check_for_changes()

    # Atualiza o indicador de conexão
    def atualizar_indicador():
        atualizar_indicador_conexao(canvas_indicador)
        root.after(60000, atualizar_indicador)  # Atualiza a cada 60 segundos

    atualizar_indicador()  # Inicia a atualização do indicador de conexão

    # Campo de entrada invisível na tela principal
    input_var = tk.StringVar()
    input_entry = tk.Entry(root, textvariable=input_var, width=20)
    input_entry.place(x=-100, y=-100)  # Posicionar fora da tela
    input_entry.focus_set()  # Focar automaticamente

    # Label para mostrar o texto digitado
    input_display = ttk.Label(root, text='', font=("Arial", 15), foreground='white', background='#1c22b5')  # Fundo com a cor desejada
    input_display.place(relx=0.5, rely=0.9, anchor="center")  # Centraliza horizontalmente e posiciona no meio da parte inferior

    def mostrar_info_produto(nome_produto, preco):
        info_window = tk.Toplevel(root)
        info_window.attributes("-fullscreen", True)
        info_window.title("Consulta Preço")
        info_window.geometry(f"{screen_width}x{screen_height}")
        info_window.config(background="#1c22b5")

        # Cria um Frame para conter os labels e usar o grid layout
        frame = tk.Frame(info_window, background="#1c22b5")
        frame.pack(expand=True)  # Expande para preencher a tela

        # Nome do produto
        nome_label = ttk.Label(frame, text=nome_produto, font=("Arial", 80, "bold"), foreground='white', background="#1c22b5")
        nome_label.grid(row=0, column=0, padx=20, pady=(0, 50))  # Ajuste o padding aqui se necessário

        if preco is not None:  # Exibe o preço apenas se não for None
            # Preço do produto
            preco_label = ttk.Label(frame, text=f'R$ {preco}', font=("Arial", 80, "bold"), foreground='white', background="#1c22b5")
            preco_label.grid(row=1, column=0, padx=20)  # Ajuste o padding aqui se necessário

        root.after(3000, lambda: [info_window.destroy(), input_entry.focus_set(), input_var.set('')])  # Fecha a janela após 3 segundos, foca no campo de entrada e limpa o campo

    # Verificando o produto no banco de dados
    def verificar_produto(event=None):
        produto = input_var.get()
        banco = Banco()
        try:
            nome = banco.consultar_nome(produto)
            codigo = banco.consultar_cod(produto)
            preco = banco.consultar_prec(codigo)
            try:
                preco_float = float(preco)
                mostrar_info_produto(nome, f'{preco_float:.2f}')
            except (ValueError, TypeError):
                mostrar_info_produto('Produto não encontrado', None)
        except Exception as e:
            logging.error(f"Erro ao verificar produto: {e}")

    def atualizar_display(*args):
        input_display.config(text=input_var.get())  # Atualiza o texto do label com o valor do campo de entrada

    def limitar_caracteres(*args):
        texto = input_var.get()
        # Permite apenas números e limita o comprimento a 13 caracteres
        if texto.isdigit() and len(texto) <= 13:
            input_var.set(texto)
        elif len(texto) > 13:
            input_var.set(texto[:13])
        elif not texto.isdigit():
            input_var.set(''.join(filter(str.isdigit, texto)))


    input_var.trace("w", atualizar_display)  # Atualiza o display sempre que o valor do campo de entrada muda
    input_var.trace_add("write", limitar_caracteres)  # Limita o número de caracteres a 13

    root.bind('<Return>', verificar_produto)  # Verifica produto apenas quando 'Enter' é pressionado

    root.mainloop()

if __name__ == "__main__":
    create_main_window()
