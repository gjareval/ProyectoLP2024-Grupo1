import datetime
import os
import tkinter as tk
from tkinter import scrolledtext
from analizadorSintactico.analizadorSintactico import parser
import errorsList as errorsList
import subprocess

'''def get_git_user():
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
        parse_result = parser.parse(user_input)
        result += str(parse_result) + "\n"

        if errorsList.errors:
            result += "\nErrores:\n"
            for error in errorsList.errors:
                result += error + "\n"
            errorsList.errors = []

        result_text.insert(tk.END, result)

        logs_dir = os.path.abspath("logs")
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        log_file = os.path.join(logs_dir, f"sintactico-{get_git_user()}-{time}.txt")
        with open(log_file, 'w') as file:
            file.write("Analizador sintactico:\n" + result)

    except Exception as e:
        result_text.insert(tk.END, f"Error en el análisis sintáctico: {str(e)}")

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Analizador Sintactico GO")

input_label = tk.Label(root, text="Ingresa una expresión:")
input_label.pack()

input_text = scrolledtext.ScrolledText(root, width=50, height=5)
input_text.pack()

analyze_button = tk.Button(root, text="Analizar", command=analyze_expression)
analyze_button.pack()

result_label = tk.Label(root, text="Resultado del análisis sintáctico:")
result_label.pack()

result_text = scrolledtext.ScrolledText(root, width=50, height=10)
result_text.pack()

root.mainloop()'''

def multi_line_input(prompt):
    print(prompt)
    lines = []
    print("Ingrese su código (termine con una línea que contenga solo ''' para finalizar):")
    while True:
        try:
            line = input()
            if line.strip() == "'''":  # Use ''' as the termination condition
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)

def get_git_user():
    try:
        result = subprocess.run(['git', 'config', 'user.name'], stdout=subprocess.PIPE)
        username = result.stdout.decode('utf-8').strip()
        return username
    except Exception as e:
        print(f"Error al obtener el usuario de Git: {e}")
        return None

def analyze_and_log(s):
    try:
        result = parser.parse(s)  # Assuming parser is defined somewhere
        print(result)

        errors = []  # Assuming errorsList.errors contains the list of errors
        if errorsList.errors:
            errors.extend(errorsList.errors)

        logs_dir = os.path.abspath("logs")
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        time = datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S')
        log_file = os.path.join(logs_dir, f"sintactico-{get_git_user()}-{time}.txt")
        
        with open(log_file, 'w') as file:
            file.write("Analizador sintactico:\n" + str(result) + "\n")
            if errors:
                file.write("\nErrores:\n")
                for error in errors:
                    file.write(error + "\n")
            errorsList.errors = []

    except Exception as e:
        print(f"Error en el análisis sintáctico: {str(e)}")

while True:
    try:
        s = multi_line_input('lp > ')
    except EOFError:
        break
    if not s:
        continue
    
    analyze_and_log(s)
