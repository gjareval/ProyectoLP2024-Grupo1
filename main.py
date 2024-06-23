import datetime
import os
import subprocess
from analizadorLexico.analizadorLexico import lexer
from analizadorSintactico.analizadorSintactico import parser
import errorsList

def get_git_user():
    try:
        result = subprocess.run(['git', 'config', 'user.name'], stdout=subprocess.PIPE)
        username = result.stdout.decode('utf-8').strip()
        return username
    except Exception as e:
        print(f"Error al obtener el usuario de Git: {e}")
        return None

def create_log(result):
    time = datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S')

    logs_dir = os.path.abspath("logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file = os.path.join(logs_dir, f"sintactico-{get_git_user()}-{time}.txt")
    with open(log_file, 'w') as file:
        file.write("Analizador sintáctico:\n" + str(result))
if __name__ == "__main__":
    while True:
        try:
            s = input('lp > ')
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)
        create_log(result)
