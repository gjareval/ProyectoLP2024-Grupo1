from analizadorLexico import lexer

while True:
    user_input = input("Ingresa una expresion ('salir' para cerrar el analizador): ")

    if user_input.lower() in ['salir']:
        print("Saliendo...")
        break

    lexer.input(user_input)

    for token in lexer:
        print(token)



