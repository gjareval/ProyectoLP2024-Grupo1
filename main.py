import datetime
import os
import tkinter as tk
from tkinter import scrolledtext
from analizadorSintactico.analizadorSintactico import parser
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

    except Exception as e:
        print(f"Error en el análisis sintáctico: {str(e)}")

def on_resize(event):
    # Adjust the size of the text widgets when the window is resized
    input_text.config(width=event.width // 10, height=event.height // 20)
    result_text.config(width=event.width // 10, height=event.height // 20)

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Analizador de GO")
root.geometry("500x400")  # Set initial window size

input_label = tk.Label(root, text="Ingresa una expresión:",font=("TkDefaultFont",12,"bold"))
input_label.pack()

input_text = scrolledtext.ScrolledText(root, width=80, height=10)
input_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

analyze_button = tk.Button(root, text="Analizar", command=analyze_expression,font=("TkDefaultFont",10,"normal"))
analyze_button.pack()

result_label = tk.Label(root, text="Resultado del análisis sintáctico:",font=("TkDefaultFont",12,"bold"))
result_label.pack()

result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.pack(fill=tk.BOTH, expand=True,padx=10, pady=10)

root.bind('<Configure>', on_resize)

root.mainloop()
