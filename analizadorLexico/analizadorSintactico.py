# Yacc import
import ply.yacc as yacc
# Token map from the lexer
from .analizadorLexico import tokens


# Reduccion de las definiciones  gramaticales
def t_statement(p):
    '''statement : structure
                 | function
                 | blocks
                 '''

def t_blocks(p):
    '''blocks : block
              | block NEWLINE blocks
              '''

def t_block(p):
    '''block : print_statement
             | input_statement
             | conditional_structure
             | operations
             | list_structure
             '''



def t_structure(p):
    'structure : TYPE IDENTIFIER STRUCT LBRACE statement RBRACE'

def t_function(p):
    '''function : FUNC IDENTIFIER LPAREN parameters RPAREN type LBRACE blocks RETURN IDENTIFIER RBRACE
                | FUNC IDENTIFIER LPAREN parameters RPAREN LBRACE blocks RBRACE
                | FUNC IDENTIFIER LPAREN RPAREN type LBRACE blocks RETURN IDENTIFIER RBRACE
                | FUNC IDENTIFIER LPAREN RPAREN LBRACE blocks RBRACE
                '''


def t_values(p):
    '''values : value
              | value COMMA values
              '''

def t_value(p):
    '''value : NUMBER
             | TEXT
             | BOOLEAN
             | IDENTIFIER
             '''

def p_number(p):
    '''number : integer
              | float
              '''

# Impresión con cero, uno o más argumentos
def t_print_statement(p):
    '''print_statement : PRINT LPAREN RPAREN
                       | PRINT LPAREN values RPAREN
                       '''

# Solicitud de datos por teclado
def t_input_statement(p):
    '''input_statement : INPUT LPAREN RPAREN
                       | INPUT LPAREN values RPAREN
                       '''

# Inicio Expresiones aritméticas con uno o más operadores.
def t_operations(p):
    '''operations : sum
                  | subtract
                  | product
                  | division
                  | increment
                  | decrement
                  '''


def t_sum(p):
    '''sum : NUMBER PLUS NUMBER
           | IDENTIFIER PLUS IDENTIFIER
           | IDENTIFIER PLUS NUMBER
           '''

def t_subtract(p):
    '''subtract : NUMBER MINUS NUMBER
                | IDENTIFIER MINUS IDENTIFIER
                | IDENTIFIER MINUS NUMBER
                '''

def t_product(p):
    '''product : NUMBER TIMES NUMBER
               | IDENTIFIER TIMES IDENTIFIER
               | IDENTIFIER TIMES NUMBER
               '''

def t_division(p):
    '''division : NUMBER DIVIDE NUMBER
                | IDENTIFIER DIVIDE IDENTIFIER
                | IDENTIFIER DIVIDE NUMBER
                '''

def t_increment(p):
    '''increment : IDENTIFIER INCREMENT
                 '''

def t_decrement(p):
    '''decrement : IDENTIFIER DECREMENT
                 '''

# Fin Expresiones aritméticas con uno o más operadores.


def t_parameters(p):
    '''parameters : parameter
                  | parameter COMMA parameters
                  '''

def t_parameter(p):
    'parameter : IDENTIFIER type'

def t_type(p):
    '''type : INT32
            | INT64
            | STRING
            | FLOAT32
            | FLOAT64
            | BOOL
            '''


# Maria Jose Moyano 
# Lista como estructura de datos
def t_list_structure(p):
    '''list_structure : list
                      | list_empty
                      | list_with_data
                      | defined_list
                      '''

def t_list(p):
    '''list : empty_list
            | list_with_data
            | defined_list
            '''

def t_empty_list(p):
    'empty_list : LBRACKET RBRACKET'

def t_list_with_data(p):
    'list_with_data : LBRACKET values RBRACKET'

def t_defined_list(p):
    'defined_list : TYPE IDENTIFIER LBRACKET values RBRACKET'


# Estructura condicional (if)
def t_conditional_structure(p):
    '''conditional_structure : IF conditions LBRACE statement RBRACE'''

def t_conditions(p):
    '''conditions : condition
                  | condition logical_operator conditions
                  '''

def t_condition(p):
    'condition : IDENTIFIER relational_operator NUMBER'

def t_logical_operator(p):
    '''logical_operator : AND
                        | OR
                        | NOT'''

def t_relational_operator(p):
    '''relational_operator : GREATER
                           | LESS
                           | GREATEREQUALS
                           | LESSEQUALS
                           | EQUALS
                           | DIFFERENT
    '''

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'



# Función de error
class SyntaxError(Exception):
    pass

def t_error(p):
    print("Error de sintaxis")
    raise SyntaxError("Error de sintaxis en la entrada")


# Construcción del parser
parser = yacc.yacc()

# Test del parser
#data = '''
#FUNC my_function() {
#    PRINT("Hello world")
#}
#'''
#Parser.parse(data)
