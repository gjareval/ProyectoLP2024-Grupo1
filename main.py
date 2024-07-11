import datetime
import os
import tkinter as tk
from tkinter import scrolledtext
import traceback
from analizadorSintactico.analizadorSintactico import parse_input
from analizadorLexico.analizadorLexico import lexer
import errorsList as errorsList
import subprocess

def get_git_user():
    try:
        result = subprocess.run(['git', 'config', 'user.name'], stdout=subprocess.PIPE)
        username = result.stdout.decode('utf-8').strip()
        return username
    except Exception as e:
        print(f"Error al obtener el usuario de Git: {e}")
        return None

def analyze_expression():

    errorsList.lexicalErrors = []
    errorsList.syntaxErrors = []
    errorsList.semanticErrors = []

    user_input = input_text.get('1.0', tk.END).strip()
    result_text.delete('1.0', tk.END)
    token_text.delete('1.0', tk.END)

    result = ""
    time = datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S')

    if not user_input:
        result_text.insert(tk.END, "No se ingresó ninguna expresión.")
        return

    logs_dirs = {
            "sintacticos": os.path.abspath("logsSintacticos"),
            "semanticos": os.path.abspath("logsSemanticos"),
            "lexicos": os.path.abspath("logsLexicos")
    }

    for dir_path in logs_dirs.values():
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    try:

        # Lexical analysis
        tokens = ""
        lexer.input(user_input)
        for token in lexer:
            tokens += f"{token}\n"

        token_text.insert(tk.END, "Tokens reconocidos: \n")
        token_text.insert(tk.END, tokens)

        lexicos_log_file = os.path.join(logs_dirs["lexicos"], f"lexico-{get_git_user()}-{time}.txt")
        with open(lexicos_log_file, 'w') as file:
            file.write("Analizador lexico:\n" + tokens)
            if errorsList.lexicalErrors:
                token_text.insert(tk.END, "\nErrores:\n")
                file.write("\nErrores:\n")
                for error in errorsList.lexicalErrors:
                    token_text.insert(tk.END, error + "\n")
                    file.write(error + "\n")
    except Exception as e:
        result_text.insert(tk.END, f"Error en el análisis léxico: {str(e)}")
        file.write(f"Error en el análisis léxico: {str(e)}")

    try:
        # Syntax analysis
        result = parse_input(user_input)
        sintactico_log_file = os.path.join(logs_dirs["sintacticos"], f"sintactico-{get_git_user()}-{time}.txt")
        with open(sintactico_log_file, 'w') as file:
            result_text.insert(tk.END, "Analizador sintáctico:\n" + str(result) + "\n")
            file.write("Analizador sintactico:\n" + str(result) + "\n")
            if errorsList.syntaxErrors:
                result_text.insert(tk.END, "\nErrores:\n")
                file.write("\nErrores:\n")
                for error in errorsList.syntaxErrors:
                    result_text.insert(tk.END, error + "\n")
                    file.write(error + "\n")

    except Exception as e:
        result_text.insert(tk.END, f"Error en el análisis sintáctico: {str(e)}")
        file.write(f"Error en el análisis sintáctico: {str(e)}")
    
    try:
        # Semantic analysis
        semantico_log_file = os.path.join(logs_dirs["semanticos"], f"semantico-{get_git_user()}-{time}.txt")
        with open(semantico_log_file, 'w') as file:
            result_text.insert(tk.END, "\nAnalizador semántico:\n" + str(result) + "\n")
            file.write("Analizador semantico:\n" + str(result) + "\n")
            if errorsList.semanticErrors:
                result_text.insert(tk.END, "\nErrores:\n")
                file.write("\nErrores:\n")
                for error in errorsList.semanticErrors:
                    result_text.insert(tk.END, error + "\n")
                    file.write(error + "\n")

    except Exception as e:
        result_text.insert(tk.END, f"Error en el análisis semántico: {str(e)}")
        file.write(f"Error en el análisis semántico: {str(e)}")
    
    finally:
        errorsList.lexicalErrors = []
        errorsList.syntaxErrors = []
        errorsList.semanticErrors = []


# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Analizador de GO")
root.configure(bg="#424141")
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()
root.geometry(f"{ancho_pantalla-30}x{alto_pantalla-50}")

analyze_button = tk.Button(root, text="Analizar", command=analyze_expression, font=("TkDefaultFont",10,"normal"))
analyze_button.grid(row=0, column=0, pady=2)

seccion1 = tk.Frame(root, bg="#424141", width=200, height=200)
seccion1.grid(row=1, column=0, pady=0, sticky="nsew")

contenedor_secciones = tk.Frame(root, bg="#424141")
contenedor_secciones.grid(row=2, column=0, sticky="ew")

root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

contenedor_secciones.grid_columnconfigure(0, weight=1)  # Hacer que la columna 0 del contenedor se expanda
contenedor_secciones.grid_columnconfigure(1, weight=1)

seccion2 = tk.Frame(contenedor_secciones, bg="#424141", width=200, height=100)
seccion2.grid(row=0, column=0, padx=2, pady=0, sticky="nsew")
seccion3 = tk.Frame(contenedor_secciones, bg="#424141", width=200, height=100)
seccion3.grid(row=0, column=1, padx=2, pady=0, sticky="nsew")

input_label = tk.Label(seccion1, text="Ingresa una expresión:", font=("TkDefaultFont",12,"bold"), bg="#424141", fg="#FFFFFF")
input_label.pack()

input_text = scrolledtext.ScrolledText(seccion1, width=80, height=18, borderwidth=0, font=("Consolas",10,"normal"), bg="#4F5155", fg="#FFFFFF")
input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

result_label = tk.Label(seccion2, text="Resultado del análisis:", font=("TkDefaultFont",12,"bold"), bg="#424141", fg="#FFFFFF")
result_label.pack()

result_text = scrolledtext.ScrolledText(seccion2, width=80, height=13, borderwidth=0, font=("Consolas",10,"normal"), bg="#4F5155", fg="#FFFFFF")
result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

token_label = tk.Label(seccion3, text="Tokens:", font=("TkDefaultFont",12,"bold"), bg="#424141", fg="#FFFFFF")
token_label.pack()

token_text = scrolledtext.ScrolledText(seccion3, width=80, height=13, borderwidth=0, font=("Consolas",10,"normal"), bg="#4F5155", fg="#FFFFFF")
token_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

root.mainloop()
