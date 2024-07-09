import datetime
import os
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from analizadorSintactico.analizadorSintactico import parser
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
    user_input = input_text.get('1.0', tk.END).strip()
    result_text.delete('1.0', tk.END)

    result = ""
    time = datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S')

    if not user_input:
        result_text.insert(tk.END, "No se ingresó ninguna expresión.")
        return

    try:
        result = parser.parse(user_input)  # Assuming parser is defined somewhere
        print(result)

        errors = []  # Assuming errorsList.errors contains the list of errors
        if errorsList.errors:
            errors.extend(errorsList.errors)

        logs_dir = os.path.abspath("logsSintacticos")
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        time = datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S')
        log_file = os.path.join(logs_dir, f"sintactico-{get_git_user()}-{time}.txt")
        
        with open(log_file, 'w') as file:
            result_text.insert(tk.END, "Analizador sintactico:\n" + str(result) + "\n")
            file.write("Analizador sintactico:\n" + str(result) + "\n")
            if errors:
                result_text.insert(tk.END, "\nErrores:\n")
                file.write("\nErrores:\n")
                for error in errors:
                    result_text.insert(tk.END, error + "\n")
                    file.write(error + "\n")
            errorsList.errors = []

        errorsSemantic = []  
        if errorsList.semanticErrors:
            errorsSemantic.extend(errorsList.semanticErrors)

        logs_dir = os.path.abspath("logsSemanticos")
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        log_file = os.path.join(logs_dir, f"semantico-{get_git_user()}-{time}.txt")
        
        with open(log_file, 'w') as file:
            result_text.insert(tk.END, "Analizador semantico:\n" + str(result) + "\n")
            file.write("Analizador semantico:\n" + str(result) + "\n")
            if errorsSemantic:
                result_text.insert(tk.END, "\nErrores:\n")
                file.write("\nErrores:\n")
                for error in errorsSemantic:
                    result_text.insert(tk.END, error + "\n")
                    file.write(error + "\n")
            errorsList.semanticErrors = []

        tokens =""
        lexer.input(user_input)
        for token in lexer:
            tokens += f"{token}\n"

        token_text.insert(tk.END, tokens)

    except Exception as e:
        print(f"Error en el análisis sintáctico: {str(e)}")


# Configurar la interfaz gráfica

root = tk.Tk()
root.title("Analizador de GO")
root.configure(bg="#4F5155",)
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()
root.geometry(f"{ancho_pantalla-30}x{alto_pantalla-50}")

analyze_button = tk.Button(root, text="Analizar", command=analyze_expression,font=("TkDefaultFont",10,"normal"))
analyze_button.grid(row=0, column=0, pady=2)

seccion1 = tk.Frame(root,bg="#4F5155",width=200, height=200)
seccion1.grid(row=1, column=0, pady=0, sticky="nsew")

contenedor_secciones = tk.Frame(root,bg="#4F5155")
contenedor_secciones.grid(row=2, column=0, sticky="ew")

root.grid_rowconfigure(2, weight=1) 
root.grid_columnconfigure(0, weight=1)

contenedor_secciones.grid_columnconfigure(0, weight=1)  # Hacer que la columna 0 del contenedor se expanda
contenedor_secciones.grid_columnconfigure(1, weight=1) 

seccion2 = tk.Frame(contenedor_secciones,bg="#4F5155", width=200, height=100)
seccion2.grid(row=0, column=0, padx=2, pady=0, sticky="nsew")
seccion3 = tk.Frame(contenedor_secciones, bg="#4F5155",width=200, height=100)
seccion3.grid(row=0, column=1, padx=2, pady=0, sticky="nsew")

input_label = tk.Label(seccion1, text="Ingresa una expresión:",font=("TkDefaultFont",12,"bold"), bg="#4F5155", fg="#FFFFFF")
input_label.pack()

input_text = scrolledtext.ScrolledText(seccion1, width=80, height=18,borderwidth=0, font=("Consolas",10,"normal"), bg="#424141", fg="#FFFFFF")
input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

result_label = tk.Label(seccion2, text="Resultado del análisis sintáctico:",font=("TkDefaultFont",12,"bold"), bg="#4F5155", fg="#FFFFFF")
result_label.pack()

result_text = scrolledtext.ScrolledText(seccion2, width=80, height=13,borderwidth=0, font=("Consolas",10,"normal"), bg="#424141", fg="#FFFFFF")
result_text.pack(fill=tk.BOTH, expand=True,padx=5, pady=5)

token_label = tk.Label(seccion3, text="Tokens:",font=("TkDefaultFont",12,"bold"), bg="#4F5155", fg="#FFFFFF")
token_label.pack()

token_text = scrolledtext.ScrolledText(seccion3, width=80, height=13,borderwidth=0, font=("Consolas",10,"normal"),  bg="#424141", fg="#FFFFFF")
token_text.pack(fill=tk.BOTH, expand=True,padx=5, pady=5)


root.mainloop()
