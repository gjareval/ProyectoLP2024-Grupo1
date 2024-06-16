import datetime
import os
import tkinter as tk
from tkinter import scrolledtext
from analizadorLexico import lexer
import subprocess
import errorsList as errorsList

def get_git_user():
    try:
        result = subprocess.run(['git', 'config', 'user.name'], stdout=subprocess.PIPE)
        username = result.stdout.decode('utf-8').strip()
        return username
    except Exception as e:
        print(f"Error al obtener el usuario de Git: {e}")
        return None

def analyze_expression():
    user_input = input_text.get('1.0', tk.END) 
    result_text.delete('1.0', tk.END)

    result = ""
    time = datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S')

    lexer.input(user_input)
    for token in lexer:
        result += f"{token}\n"

    if len(errorsList.errors)>0:
        result += "\nErrores:"
        for error in errorsList.errors:
            result += "\n"+error  
        errorsList.errors=[]

    result_text.insert(tk.END, result)

    logs_dir = os.path.abspath("logs")

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    log_file = os.path.join(logs_dir,"lexico-"+get_git_user()+"-"+time+".txt")
    with open(log_file, 'w') as file:
        file.write("Analizador lexico:\n" + result)

    lexer.lineno = 1 

root = tk.Tk()
root.title("Analizador Léxico GO")
    
input_label = tk.Label(root, text="Ingresa una expresión:")
input_label.pack()

# Reemplazar Entry por Text para permitir múltiples líneas
input_text = scrolledtext.ScrolledText(root, width=50, height=5)
input_text.pack()

analyze_button = tk.Button(root, text="Analizar", command=analyze_expression)
analyze_button.pack()

result_label = tk.Label(root, text="Resultado del análisis léxico:")
result_label.pack()

result_text = scrolledtext.ScrolledText(root, width=50, height=10)
result_text.pack()

root.mainloop()
