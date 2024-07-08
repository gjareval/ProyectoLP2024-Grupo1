# Yacc import
import ply.yacc as yacc
# Token map from the lexer
from analizadorLexico.analizadorLexico import tokens
import errorsList as errorsList

# Variables creadas
variables = {}
constants = {}


# Definicion de las definiciones  gramaticales
def p_statement(p):
    '''statement : blocks
                 | import blocks
                 | package blocks
                 | package import blocks
                 | main LBRACE blocks RBRACE
                 | package main LBRACE blocks RBRACE
                 | import main LBRACE blocks RBRACE
                 | package import main LBRACE blocks RBRACE'''

def p_import(p):
    '''import : 
              | IMPORT CHARSTRING
              | IMPORT LPAREN values_for_import RPAREN'''

def p_values_for_import(p):
    '''values_for_import : CHARSTRING
                         | CHARSTRING values_for_import'''

def p_package(p):
    '''package : PACKAGE VARIABLE
               | PACKAGE MAIN'''  

def p_main(p):
    'main : FUNCTION MAIN LPAREN RPAREN'  

# Reconocimiento de blocks para reglas semánticas (Guillermo Arévalo)
def p_blocks(p):
    '''blocks : block
              | block blocks
              | block SEMICOLON blocks'''
    
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]] + p[3]

def p_block(p):
    '''block : print_statement
             | input_statement
             | operation
             | data_structure
             | control_structure
             | function
             | parameters
             | variable_declaration
             | variable_assignation
             | return
             '''
    p[0] = p [1]

# Reglas semánticas de inicializacion de variables, constantes, y asignacion de variables (Guillermo Arévalo)

def p_variable_declaration(p):
    '''variable_declaration : VAR VARIABLE type
                            | VAR VARIABLE type ASSIGN value'''
    
    # Inicializacion de variables asegurando que no haya una constante con el mismo nombre creada (Guillermo Arévalo)
    if p[2] not in constants:
        if len(p)==4:
            variables[p[2]]=-1
        else :
            variables[p[2]]=p[5]
    else: 
        errorsList.semanticErrors.append(f"Error: Variable '{p[2]}' ya esta definida.")
        print(f"Error: Variable '{p[2]}' ya esta definida.")

    
def p_variable_declaration_short(p):
    '''variable_declaration : VARIABLE SHORTASSIGN value
                            | VARIABLE SHORTASSIGN operation'''
    
    # Inicializacion de variables asegurando que no haya una constante con el mismo nombre creada (Guillermo Arévalo)
    if p[1] not in constants:
        variables[p[1]]=p[3]
    else: 
        errorsList.semanticErrors.append(f"Error: Variable '{p[1]}' ya esta definida.")
        print(f"Error: Variable '{p[1]}' ya esta definida.")
    
def p_variable_declaration_multiple(p):
    '''variable_declaration : VAR variables type
                            | VAR variables type ASSIGN value'''
    
    # Inicializacion de multiples variables en la misma linea (Guillermo Arévalo)
    if len(p) == 4:
        for var in p[2]:
            variables[var] = -1 
    else:
        for var in p[2]:
            variables[var] = p[5]

def p_variable_declaration_constant(p):
    '''variable_declaration : CONST VARIABLE ASSIGN value'''

    # Inicializacion de constante asegurando que no hayan constantes con el mismo nombre ya creadas (Guillermo Arévalo)
    if p[2] in variables or p[2] in constants:
        errorsList.semanticErrors.append(f"Error: Variable '{p[2]}' ya esta definida.")
        print(f"Error: Variable '{p[2]}' ya esta definida.")
    else:
        constants[p[2]] = p[4]
    

    
def p_variable_assignation(p):
    '''variable_assignation : VARIABLE assignation value
                            | VARIABLE assignation operation'''
    
    # Asignacion de variable asegurando que la variable ya haya sido creada (Guillermo Arévalo)
    if p[1] not in variables:
        errorsList.semanticErrors.append(f"Error: Variable '{p[1]}' no inicializada")
        print(f"Error: Variable '{p[1]}' no inicializada")
        
        variables[p[1]]=p[3]


def p_variable_assignation_double(p):
    '''variable_assignation : VARIABLE double_operator'''
    #Asignación doble (Brian Mite)
    if p[1] in variables:
        if p[2] == '++':
            variables[p[1]] += 1
        elif p[2] == '--':
            variables[p[1]] -= 1
    else:
        errorsList.semanticErrors.append(f"Error: Variable '{p[1]}' no inicializada.")
        print(f"Error: Variable '{p[1]}' no inicializada.")
        
 
def p_variable_assignation_multiple(p):
    '''variable_assignation : variables assignation value'''

    # Asignacion de variables multiples asegurando que las variables ya hayan sido creadas (Guillermo Arévalo)
    for var in p[1]:
        if var in variables:
            variables[var] = p[3]
        else:
            errorsList.semanticErrors.append(f"Error: Variable '{var}' no inicializada")
            print(f"Error: Variable '{var}' no inicializada")

def p_variable_assignation_structures(p):
    '''variable_assignation : map_assign
                            | array_assign'''
    
def p_variables(p):
    '''variables : VARIABLE
                 | VARIABLE COMMA variables'''
   
    # Multiples variables en forma de lista (Guillermo Arévalo)
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
    
def p_assignation(p):
    '''assignation : ASSIGN
                   | PLUSASSIGN
                   | MINUSASSIGN
                   | TIMESASSIGN
                   | DIVIDEASSIGN
                   | MODASSIGN
                   '''
    
# Tipos de funciones
def p_function(p):
    '''function : FUNCTION VARIABLE LPAREN RPAREN LBRACE blocks RBRACE   
                | FUNCTION VARIABLE LPAREN RPAREN type LBRACE blocks RBRACE
                | FUNCTION VARIABLE LPAREN parameters RPAREN LBRACE blocks RBRACE
                | FUNCTION VARIABLE LPAREN parameters RPAREN type LBRACE blocks RBRACE
                
                '''
    # Definición de función y verificación de retorno (Maria Jose Moyano)
    function_name = p[2]
    parameters = p[4] if p[4] != ')' else []

    if len(p)==8:
        return_type=None
        body=p[6]
    elif len(p)==9 and p[6] =='{':
        return_type=p[5]
        body=p[7]
    elif len(p)==9 and p[5] =='{':
        return_type=None
        body=p[7]
    elif len(p)==10 and p[7]=='{':
        return_type=p[6]
        body=p[8]

    
    
    print(function_name)
    print(parameters)
    print(return_type)
    print(body)

    if 'return' in body:
        return_value = body['return']
        if isinstance(return_value, return_type):
            # Registro de la función (implementación puede variar)
            function[function_name] = {
                'parameters': parameters,
                'return_type': return_type,
                'body': body
            }
        else:
            errorsList.semanticErrors.append(f"Error: El valor de retorno de la función '{function_name}' no coincide con el tipo '{return_type}'.")
            print(f"Error: El valor de retorno de la función '{function_name}' no coincide con el tipo '{return_type}'.")
    else:
        function[function_name] = {
            'parameters': parameters,
            'return_type': return_type,
            'body': body
        }



def p_return(p):
    '''return : RETURN value
              | RETURN value LBRACKET value RBRACKET
              | RETURN value PERIOD value
              | RETURN TRUE
              | RETURN FALSE'''
    
    if len(p)==2:
        if isinstance(p[2] ,bool):
            p[0]=bool
        else:
            p[0]=type(p[2])

    

#Brian Mite Semantico
def p_values(p):
    '''values : value 
              | value COMMA values'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# Configuracion de values para ser reconocidos por las reglas semanticas (Guillermo Arevalo)   
def p_value(p):
    '''value : VARIABLE
             | VARIABLE LBRACKET RBRACKET
             | VARIABLE LBRACKET value RBRACKET
             | not_variable_value'''
    if isinstance(p[1],str) and p[1] in variables:
        p[0] = variables[p[1]]
    else:
        p[0] =p[1]
    
def p_not_variable_value(p):
    ''' not_variable_value : CHARSTRING
                           | number'''
    p[0] =p[1]
      
def p_number(p):
    '''number : INT
              | FLOAT'''
    p[0] = p[1]

# Impresión con cero, uno o más argumentos  
def p_print_statement(p):
    '''print_statement : PRINT LPAREN values RPAREN
                       | PRINTF LPAREN FORMATSTRING COMMA values RPAREN
                       | PRINT LPAREN operation RPAREN
                       | PRINT LPAREN RPAREN'''

# Solicitud de datos por teclado  
def p_input_statement(p):
    '''input_statement : INPUT LPAREN values RPAREN
                       | INPUT LPAREN operation RPAREN
                       | INPUT LPAREN RPAREN'''

# Inicio Expresiones aritméticas con uno o más operadores.

# Regla semantica para asegurarse que las operaciones sean de tipos numericos compatibles (Guillermo Arevalo)
def p_operation(p):
    '''operation : value operator value'''

    if isinstance(p[1], (int, float)) and isinstance(p[3], (int, float)):
        if p[2] == '+' or p[2] == '-' or p[2] == '*' or p[2] == '/':
            p[0] = p[1] + p[3] if p[2] == '+' else p[1] - p[3] if p[2] == '-' else p[1] * p[3] if p[2] == '*' else p[1] / p[3]
        else:
            errorsList.semanticErrors.append(f"Error semantico: Operador '{p[2]}' no es valido para operaciones aritmeticas.")
            print(f"Error semantico: Operador '{p[2]}' no es valido para operaciones aritmeticas.")
    else:
        if not isinstance(p[1], (int, float)):
            errorsList.semanticErrors.append(f"Error semantico: Operando '{p[1]}' invalido para operaciones aritmeticas.")
            print(f"Error semantico: Operando '{p[1]}' invalido para operaciones aritmeticas.")
        else:
            errorsList.semanticErrors.append(f"Error semantico: Operando '{p[3]}' invalido para operaciones aritmeticas.")
            print(f"Error semantico: Operando '{p[3]}' invalido para operaciones aritmeticas.")



def p_operation_complex(p):
    '''operation : value operator LPAREN value RPAREN
                 | LPAREN value RPAREN operator value
                 | LPAREN value operator value RPAREN
                 | value operator operation
                 | LPAREN value operator operation RPAREN
                 | LPAREN value RPAREN operator operation
                 | value operator LPAREN operation RPAREN'''   
                 
    
def p_operation_single(p):
    'operation : value double_operator'

def p_operator(p):
    '''operator : PLUS
                | MINUS
                | TIMES
                | DIVIDE
                | ASSIGN'''
    p[0]=p[1]
    
def p_double_operator(p):
    '''double_operator : INCREMENT
                       | DECREMENT'''
    p[0] = p[1]    
    
# Fin Expresiones aritméticas con uno o más operadores.
        
def p_parameters(p):
    '''parameters : parameter
                  | parameter COMMA parameters
                  '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_parameter(p):
    'parameter : VARIABLE type'

    p[0] = (p[1],p[2])

def p_type(p):
    '''type : INT
            | INT32
            | INT64
            | STRING
            | FLOAT
            | FLOAT32
            | FLOAT64
            | BOOL
            '''
    p[0]=p[1]
    
# Estructuras de control
def p_control_structure(p):
    '''control_structure : conditional_structure
                         | for_estructure
                         | switch_structure'''

# Maria Jose Moyano 
# Estructura condicional (if)
def p_conditional_structure(p):
    '''conditional_structure : IF conditions conditional_body
                             | IF conditions conditional_body ELSE conditional_body
                             | IF conditions conditional_body ELSE IF conditions conditional_body ELSE conditional_body'''
     # Manejo de estructuras condicionales (Maria Jose Moyano)
    if len(p) == 4:
        # Estructura básica: IF conditions conditional_body
        p[0] = ('if', p[2], p[3])
    elif len(p) == 6:
        # Estructura: IF conditions conditional_body ELSE conditional_body
        p[0] = ('if-else', p[2], p[3], p[5])
    elif len(p) == 10:
        # Estructura: IF conditions conditional_body ELSE IF conditions conditional_body ELSE conditional_body
        p[0] = ('if-else-if-else', p[2], p[3], p[6], p[8], p[9])

    # Verificación semántica de la condición
    if not isinstance(p[2], bool):
        errorsList.semanticErrors.append(f"Error semántico: La condición '{p[2]}' no es una expresión booleana.")
        print(f"Error semántico: La condición '{p[2]}' no es una expresión booleana.")

def p_conditional_body(p):
    '''conditional_body : LBRACE statement RBRACE
                        | LBRACE BREAK RBRACE
                        | LBRACE CONTINUE RBRACE'''
    # Manejo de cuerpos condicionales (Maria Jose Moyano)
    if p[2] == 'break':
        p[0] = ('break',)
    elif p[2] == 'continue':
        p[0] = ('continue',)
    else:
        p[0] = ('statement', p[2])


def p_conditions(p):
    '''conditions : condition
                  | condition logical_operator conditions
                  '''
    


def p_condition(p):
    'condition : value relational_operator value'

    


def p_logical_operator(p):
    '''logical_operator : AND
                        | OR
                        | NOT'''
    p[0] = p[1]

def p_relational_operator(p):
    '''relational_operator : GREATER
                           | LESS
                           | GREATEREQUALS
                           | LESSEQUALS
                           | EQUALS
                           | DIFFERENT
    '''
    p[0]=p[1]

# Guillero Arevalo
# Estructura for

def p_for_estructure(p):
    '''for_estructure : for_initialization
                      | for_infinite_bucle
                      | for_iterator'''

def p_for_initialization(p):
    'for_initialization : FOR VARIABLE SHORTASSIGN value SEMICOLON condition SEMICOLON value double_operator LBRACE statement RBRACE'

def p_for_infinite_bucle(p):
    'for_infinite_bucle : FOR LBRACE statement RBRACE'

def p_for_iterator(p):
    'for_iterator : FOR VARIABLE COMMA VARIABLE SHORTASSIGN RANGE VARIABLE LBRACE statement RBRACE'

# Brian Mite
# Estructura switch
def p_switch_structure(p):
    '''switch_structure : SWITCH switch_expression LBRACE case_blocks RBRACE'''
    
def p_switch_expression(p):
    '''switch_expression : VARIABLE SHORTASSIGN value
                         | empty'''
    
def p_case_blocks(p):
    '''case_blocks : case_block
                   | case_block case_blocks'''
    
def p_case_block(p):
    '''case_block : CASE values COLON statement
                  | DEFAULT COLON statement'''

# Manejar la regla vacía para la expresión opcional
def p_empty(p):
    'empty :'
    pass

# Estructura de datos
#Brian Mite
# Struct
def p_data_structure(p):
    '''data_structure : array_structure
                      | map_structure
                      | slice_structure
                      | struct_structure'''
    
def p_struct_structure(p):
    'struct_structure : TYPE VARIABLE STRUCT LBRACE struct_fields RBRACE'

    struct_name = p[2]
    struct_fields = p[5]

    if struct_name not in variables and struct_name not in constants:
        variables[struct_name] = {
            'type': 'struct',
            'fields': struct_fields
        }
    else:
        errorsList.semanticErrors.append(f"Error: El struct '{struct_name}' ya está definido.")
        print(f"Error: El struct '{struct_name}' ya está definido.")
    

def p_struct_fields(p):
    '''struct_fields : struct_field
                     | struct_field struct_fields'''

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_struct_field(p):
    'struct_field : VARIABLE type'
    
    p[0] = {'name': p[1], 'type': p[2]}

#Maria Jose Moyano 
# Array
def p_array_structure(p):
    '''array_structure : VAR VARIABLE LBRACKET INT RBRACKET type
                       | VAR VARIABLE ASSIGN LBRACKET INT RBRACKET type LBRACE values RBRACE
                       | VAR VARIABLE LBRACKET INT RBRACKET type ASSIGN LBRACKET values RBRACKET'''
    
    # (Maria Jose Moyano)
    if len(p) == 7:
         p[0] = {'type': p[6], 'var': (p[2], p[4])}
    elif len(p) == 10:
         p[0] = {'type': p[7], 'var': (p[2], p[5]), 'values': p[9]}
    elif len(p) == 9:
         p[0] = {'type': p[6], 'var': (p[2], p[4]), 'values': p[8]}



    
def p_array_assign(p):
    'array_assign : VARIABLE LBRACKET INT RBRACKET ASSIGN value'
# (Maria Jose Moyano)
    p[0] = {'var': (p[1], p[3]), 'value': p[6]}
    
    


# Guillermo Arevalo
# Map
def p_map_structure(p):
    '''map_structure : VARIABLE SHORTASSIGN MAP LBRACKET type RBRACKET type LBRACE map_values RBRACE
                      | VARIABLE SHORTASSIGN MAKE LPAREN MAP LBRACKET type RBRACKET type RPAREN'''
    


def p_map_values(p):
    '''map_values : map_value
                  | map_value COMMA map_values'''
    

    
def p_map_value(p):
    '''map_value : value COLON value'''
      

def p_map_assign(p):
    'map_assign : VARIABLE LBRACKET value RBRACKET ASSIGN value'
    
    
        

# Brian Mite
# Slice
def p_slice_structure(p):
    '''slice_structure : VARIABLE SHORTASSIGN LBRACKET RBRACKET type LBRACE values RBRACE
                       | VAR VARIABLE LBRACKET RBRACKET type
                       | VARIABLE SHORTASSIGN LBRACKET RBRACKET type
                       | VARIABLE ASSIGN append_statement'''

    slice_name = p[1]

    if p[2] == ':=':  # Short assignment :=
        if len(p) == 9:  # Variable := []type{values}
            slice_type = p[5]
            slice_values = p[7]
            # Verifica si la slice ya está definida
            if slice_name not in variables and slice_name not in constants:
                variables[slice_name] = {
                    'type': 'slice',
                    'element_type': slice_type,
                    'values': slice_values
                }
            else:
                errorsList.semanticErrors.append(f"Error: La slice '{slice_name}' ya está definida.")
                print(f"Error: La slice '{slice_name}' ya está definida.")
        elif len(p) == 6:  # Variable := []type
            slice_type = p[5]
            # Verifica si la slice ya está definida
            if slice_name not in variables and slice_name not in constants:
                variables[slice_name] = {
                    'type': 'slice',
                    'element_type': slice_type,
                    'values': []
                }
            else:
                errorsList.semanticErrors.append(f"Error: La slice '{slice_name}' ya está definida.")
                print(f"Error: La slice '{slice_name}' ya está definida.")
    elif p[2] == '=':  # Assignment =
        if p[3] == 'append_statement':  # Variable = append_statement
            append_result = p[4]
            # Actualiza la slice con los resultados del append_statement
            if slice_name in variables and variables[slice_name]['type'] == 'slice':
                variables[slice_name]['values'].extend(append_result)
            else:
                errorsList.semanticErrors.append(f"Error: '{slice_name}' no es una slice válida o no está inicializada como una slice.")
                print(f"Error: '{slice_name}' no es una slice válida o no está inicializada como una slice.")
    
    else: # Variable [] type
        slice_name = p[2]
        slice_type = p[5]
        # Verifica si la slice ya está definida
        if slice_name not in variables and slice_name not in constants:
            variables[slice_name] = {
                'type': 'slice',
                'element_type': slice_type,
                'values': []
            }
        else:
            errorsList.semanticErrors.append(f"Error: La slice '{slice_name}' ya está definida.")
            print(f"Error: La slice '{slice_name}' ya está definida.")



def p_append_statement(p):
    '''append_statement : APPEND LPAREN VARIABLE COMMA values RPAREN
                        | APPEND LPAREN VARIABLE COMMA LBRACKET RBRACKET type LBRACE values RBRACE RPAREN'''

    append_result = []

    if len(p) == 7:  # APPEND(VARIABLE, values)
        slice_name = p[3]
        values = p[5]

        if slice_name in variables and variables[slice_name]['type'] == 'slice':
            variables[slice_name]['values'].extend(values)
            append_result = values
        else:
            errorsList.semanticErrors.append(f"Error: '{slice_name}' no es una slice válida o no está inicializada como una slice.")
            print(f"Error: '{slice_name}' no es una slice válida o no está inicializada como una slice.")

    elif len(p) == 11:  # APPEND(VARIABLE, []type{values})
        slice_name = p[3]
        slice_type = p[7]
        values = p[9]

        # Verifica si la slice está definida y es del tipo correcto
        if slice_name in variables and variables[slice_name]['type'] == 'slice' and variables[slice_name]['element_type'] == slice_type:
            variables[slice_name]['values'].extend(values)
            append_result = values
        else:
            errorsList.semanticErrors.append(f"Error: '{slice_name}' no es una slice válida o no está inicializada como una slice del tipo '{slice_type}'.")
            print(f"Error: '{slice_name}' no es una slice válida o no está inicializada como una slice del tipo '{slice_type}'.")

    return append_result

t_ignore = ' \t'

def p_error(p):
    if p:
        errorsList.errors.append(f"Syntax error at token '{p.value}'")
        print(f"Syntax error at token '{p.value}'")
    else:
        errorsList.errors.append(f"Syntax error at token '{p.value}'")
        print(f"Syntax error at token '{p.value}'")

# Construcción del parser
parser = yacc.yacc()