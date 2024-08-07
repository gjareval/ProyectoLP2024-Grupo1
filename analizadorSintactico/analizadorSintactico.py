import ply.yacc as yacc
from analizadorLexico.analizadorLexico import tokens
import errorsList as errorsList

# Variables creadas
variables = {}
constants = {}
functions = {}

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
             | variable_declaration
             | variable_assignation
             '''
    p[0] = p [1]

def p_variables(p):
    '''variables : VARIABLE
                 | VARIABLE COMMA variables'''
   
    # Multiples variables en forma de lista (Guillermo Arévalo)
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


# Configuracion de values para ser reconocidos por las reglas semanticas (Guillermo Arevalo)   
def p_value(p):
    '''value : not_variable_value
             | VARIABLE LBRACKET RBRACKET    
             | VARIABLE LBRACKET value RBRACKET
             | VARIABLE'''
    if isinstance(p[1], str) and not(p[1].startswith('"') and p[1].endswith('"')) and not p[1]=="True" and not p[1]=="False"  :
        if p[1] in variables:
            p[0] = variables[p[1]]
        else:
           errorsList.semanticErrors.append(f"Error: Variable '{p[1]}' no esta definida.")
    else:
        p[0] =p[1]
    
def p_not_variable_value(p):
    ''' not_variable_value : CHARSTRING
                           | INT
                           | FLOAT
                           | BOOL'''
    p[0] = p[1]
        
def p_values(p):
    '''values : value 
              | value COMMA values'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
      
# Reglas semánticas de inicializacion de variables, constantes, y asignacion de variables (Guillermo Arévalo)
def p_variable_declaration(p):
    '''variable_declaration : VAR variables type
                            | VAR variables type ASSIGN value
                            | VAR variables type ASSIGN operation
                            | VARIABLE SHORTASSIGN value
                            | VARIABLE SHORTASSIGN operation
                            | CONST VARIABLE ASSIGN value'''

    if len(p) == 4:
        if p[1] == 'var':
            for var in p[2]:
                if(var in constants):
                    errorsList.semanticErrors.append(f"Error: Variable '{var}' ya esta definida como constante.")
                else:
                    variables[var] = None 
        else:
            if(p[1] in constants):
                errorsList.semanticErrors.append(f"Error: Variable '{p[1]}' ya esta definida como constante.")
            else:
                variables[p[1]] = p[3]
    else:
        if p[1] == 'const':
            if(p[2] in constants):
                errorsList.semanticErrors.append(f"Error: Variable '{p[2]}' ya esta definida.")
            else:
                constants[p[2]] = p[4]
        else:
            for var in p[2]:
                if(var in constants):
                    errorsList.semanticErrors.append(f"Error: Variable '{var}' ya esta definida como constante.")
                else:
                    variables[var] = p[5] 
    
def p_variable_assignation(p):
    '''variable_assignation : VARIABLE assignation value
                            | VARIABLE assignation operation
                            | VARIABLE double_operator'''
    
    # Asignacion de variable asegurando que la variable ya haya sido creada (Guillermo Arévalo)
    if len(p)==3:
        try:
            if p[2] == '++':
                variables[p[1]] += 1
            elif p[2] == '--': 
                variables[p[1]] -= 1
        except Exception as e:
            if variables[p[1]] == None: 
                errorsList.semanticErrors.append(f"La variable '{p[1]}' no ha sido inicializada")
            else:
                errorsList.semanticErrors.append(f"No es posible realizar esa operacion para '{p[1]}'")

    else:
        if p[1] not in variables:
            errorsList.semanticErrors.append(f"Error: Variable '{p[1]}' no inicializada")
        else:
            if p[2] == '=' :
                variables[p[1]]=p[3]
            elif p[2] == '+=':
                variables[p[1]] += p[3]
            elif p[2] == '-=':
                variables[p[1]] -= p[3]
            elif p[2] == '*=':
                variables[p[1]] -= p[3]
            elif p[2] == '/=':
                variables[p[1]] /= p[3]
            elif p[2] == '%=':
                variables[p[1]] %= p[3]

def p_variable_assignation_structures(p):
    '''variable_assignation : map_assign
                            | array_assign'''
    
def p_assignation(p):
    '''assignation : ASSIGN
                   | PLUSASSIGN
                   | MINUSASSIGN
                   | TIMESASSIGN
                   | DIVIDEASSIGN
                   | MODASSIGN
                   '''

def p_parameters(p):
    '''parameters : VARIABLE type
                  | VARIABLE COMMA parameters
                  '''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

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



#Definicion de funcion, devuelve nombre
def p_definir_function(p):
    '''definir_function : FUNCTION VARIABLE LPAREN RPAREN
                        | FUNCTION VARIABLE LPAREN RPAREN type
                        | FUNCTION VARIABLE LPAREN parameters RPAREN
                        | FUNCTION VARIABLE LPAREN parameters RPAREN type
                        '''
    if p[2] in functions:
        errorsList.semanticErrors.append(f"Error: La funcion ya esta definida.")
    else:
        parameters = p[4] if p[4]!=')' else []
        return_type = None
        if len(p) == 6 and p[5]!=')':
            return_type = p[5]
        elif len(p)== 7:
            return_type = p[6]
        functions[p[2]]={
            'parameters':parameters,
            'return_type': return_type
        }

    p[0] = p[2]

    
# Tipos de funciones
def p_function(p):
    '''function : definir_function LBRACE RBRACE
                | definir_function LBRACE blocks RBRACE
                | definir_function LBRACE return RBRACE  
                | definir_function LBRACE blocks return RBRACE
                '''
    function_name = p[1]
    parameters = functions[function_name]['parameters']
    return_type = functions[function_name]['return_type']
    return_value = None

    if len(p)==6:
        return_value = type(p[4]).__name__
    elif len(p)==5:
        return_value = type(p[3]).__name__ if type(p[3]).__name__!='list' else None
        if return_value =='str':
            return_value = 'string'
    if return_type==None and return_value==None:
        functions[function_name]['return_value'] = return_value
    elif return_value != return_type:
        errorsList.semanticErrors.append(f"Error: El valor de retorno de la función '{function_name}' no coincide con el tipo '{return_type}'.")
    else:
        functions[function_name]['return_value'] = return_value

def p_return(p):
    '''return : RETURN value
              | RETURN value LBRACKET value RBRACKET
              | RETURN value PERIOD value'''
    
    if p[2]=="True":
        p[0]=True
    elif p[2]=="False":
        p[0]=False
    else:
        p[0]=p[2]

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

def p_operator(p):
    '''operator : PLUS
                | MINUS
                | TIMES
                | DIVIDE
                | AND
                | OR
                | NOT
                | LESS
                | LESSEQUALS
                | GREATER
                | GREATEREQUALS
                | EQUALS
                | DIFFERENT'''
    p[0]=p[1]

def p_operation(p):
    '''operation : value operator value'''
    if (type(p[1]).__name__=='int' or type(p[1]).__name__=='float') and (type(p[3]).__name__=='int' or type(p[3]).__name__=='float'):
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3] if p[3] != 0 else errorsList.semanticErrors.append("Error semantico: Division por cero.")
        elif p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '<=':
            p[0] = p[1] <= p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        elif p[2] == '>=':
            p[0] = p[1] >= p[3]
        elif p[2] == '==':
            p[0] = p[1] == p[3]
        elif p[2] == '!=':
            p[0] = p[1] != p[3]        
        else:
            errorsList.semanticErrors.append(f"Error semantico: Operador '{p[2]}' no es valido para operaciones aritmeticas.")
    elif type(p[1]).__name__=='bool' and type(p[1]).__name__=='bool':
        if p[2] == '&&':
            p[0] = p[1] and p[3]
        elif p[2] == '||':
            p[0] = p[1] or p[3]
        elif p[2] == '==':
            p[0] = p[1] == p[3]
        else:
            errorsList.semanticErrors.append(f"Error semantico: Operador '{p[2]}' no es valido para operaciones logicas.")
    else:
        if not isinstance(p[1], (int, float, bool)):
            errorsList.semanticErrors.append(f"Error semantico: Operando '{p[1]}' invalido. Asegurate de usar un numero, variable inicializada o booleano.")
        if not isinstance(p[3], (int, float, bool)):
            errorsList.semanticErrors.append(f"Error semantico: Operando '{p[3]}' invalido. Asegurate de usar un numero, variable inicializada o booleano.")
        else:
            errorsList.semanticErrors.append(f"No es posible realizar esta operacion entre estoss tipos de datos.")

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
    
def p_double_operator(p):
    '''double_operator : INCREMENT
                       | DECREMENT'''
    p[0] = p[1]    
    
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
                             | IF conditions conditional_body ELSE IF conditions conditional_body
                             | IF conditions conditional_body ELSE IF conditions conditional_body ELSE conditional_body'''

def p_conditional_body(p):
    '''conditional_body : LBRACE blocks RBRACE
                        | LBRACE blocks return RBRACE
                        | LBRACE return RBRACE
                        | LBRACE BREAK RBRACE
                        | LBRACE CONTINUE RBRACE'''

def p_conditions(p):
    '''conditions : condition
                  | condition logical_operator conditions
                  '''

def p_condition(p):
    '''condition : BOOL
                  | value relational_operator values
                  '''

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

# Guillermo Arevalo
# Estructura for

def p_for_estructure(p):
    '''for_estructure : for_initialization
                      | for_infinite_bucle
                      | for_iterator'''

def p_for_initialization(p):
    'for_initialization : FOR VARIABLE SHORTASSIGN value SEMICOLON condition SEMICOLON value double_operator LBRACE blocks RBRACE'

def p_for_infinite_bucle(p):
    'for_infinite_bucle : FOR LBRACE blocks RBRACE'

def p_for_iterator(p):
    'for_iterator : FOR VARIABLE COMMA VARIABLE SHORTASSIGN RANGE VARIABLE LBRACE blocks RBRACE'

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
    
    if p[10]=='}':
        if p[1] not in variables:
            variables[p[1]]=f'[{p[9]}]'
    else:
        if p[1] not in variables:
            variables[p[1]]='map'
    
def p_map_values(p):
    '''map_values : map_value
                  | map_value COMMA map_values'''
      
def p_map_value(p):
    '''map_value : value COLON value'''
      
def p_map_assign(p):
    'map_assign : VARIABLE LBRACKET value RBRACKET ASSIGN value'
    if p[1] not in variables:
        errorsList.semanticErrors.append(f"Error: Variable '{p[1]}' no inicializada")
        
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
    elif p[2] == '=':  # Assignment =
        if p[3] == 'append_statement':  # Variable = append_statement
            append_result = p[4]
            # Actualiza la slice con los resultados del append_statement
            if slice_name in variables and variables[slice_name]['type'] == 'slice':
                variables[slice_name]['values'].extend(append_result)
            else:
                errorsList.semanticErrors.append(f"Error: '{slice_name}' no es una slice válida o no está inicializada como una slice.")
    
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
    return append_result

t_ignore = ' \t'

def p_error(p):
    if p:
        errorsList.syntaxErrors.append(f"Error sintactico en el token '{p.value}'")
    else:
        errorsList.syntaxErrors.append(f"Error sintactico en el token '{p.value}'")

def clear_variables():
    global variables, constants, functions
    variables = {}
    constants = {}
    functions = {}

# Construcción del parser
parser = yacc.yacc()

def parse_input(input_data):
    clear_variables()
    result = parser.parse(input_data)
    return result