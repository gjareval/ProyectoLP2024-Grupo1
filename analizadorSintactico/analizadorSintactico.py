# Yacc import
import ply.yacc as yacc
# Token map from the lexer
from analizadorLexico.analizadorLexico import tokens

# Definicion de las definiciones  gramaticales
def p_statement(p):
    '''statement : structure
                 | blocks
                 | function
                 | parameters
                 '''
    
def p_blocks(p):
    '''blocks : block
              '''

def p_block(p):
    '''block : print_statement
             | input_statement
             | conditional_structure
             | operation
             | list_structure
             '''
    
def p_structure(p):
    'structure : TYPE VARIABLE STRUCT LBRACE statement RBRACE'

def p_function(p):
    '''function : FUNCTION VARIABLE LPAREN parameters RPAREN type LBRACE blocks RETURN VARIABLE RBRACE
                | FUNCTION VARIABLE LPAREN parameters RPAREN LBRACE blocks RBRACE
                | FUNCTION VARIABLE LPAREN RPAREN type LBRACE blocks RETURN VARIABLE RBRACE
                | FUNCTION VARIABLE LPAREN RPAREN LBRACE blocks RBRACE
                '''

def p_values(p):
    '''values : value 
              | value COMMA values'''


def p_value(p):
    ''' value : VARIABLE
              | number'''
    
def p_number(p):
    '''number : INT
              | FLOAT'''

# Impresión con cero, uno o más argumentos  
def p_print_statement(p):
    '''print_statement : PRINT LPAREN values RPAREN
                       | PRINT LPAREN operation RPAREN
                       | PRINT LPAREN RPAREN'''

# Solicitud de datos por teclado  
def p_input_statement(p):
    '''input_statement : INPUT LPAREN values RPAREN
                       | INPUT LPAREN operation RPAREN
                       | INPUT LPAREN RPAREN'''

# Inicio Expresiones aritméticas con uno o más operadores.
def p_operation(p):
    '''operation : value operator value
                 | value operator operation'''
    
def p_operation_single(p):
    'operation : value double_operator'

def p_operator(p):
    '''operator : PLUS
                | MINUS
                | TIMES
                | DIVIDE
                | ASSIGN'''
    
def p_double_operator(p):
    '''double_operator : INCREMENT
                       | DECREMENT'''
    
# Fin Expresiones aritméticas con uno o más operadores.
    
def p_parameters(p):
    '''parameters : parameter
                  | parameter parameters
                  | parameter COMMA parameters
                  '''

def p_parameter(p):
    'parameter : VARIABLE type'

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
    

# Maria Jose Moyano 
# Estructura condicional (if)
def p_conditional_structure(p):
    '''conditional_structure : IF conditions conditional_body
                             | IF conditions conditional_body ELSE conditional_body
                             | IF conditions conditional_body ELSE IF conditions conditional_body ELSE conditional_body'''
def p_conditional_body(p):
    'conditional_body : LBRACE statement RBRACE'

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

def p_relational_operator(p):
    '''relational_operator : GREATER
                           | LESS
                           | GREATEREQUALS
                           | LESSEQUALS
                           | EQUALS
                           | DIFFERENT
    '''

# Lista como estructura de datos
def p_list_structure(p):
    '''list_structure : empty_list
                      | list_with_data
                      | defined_list
                      '''

def p_empty_list(p):
    'empty_list : LBRACE RBRACE'

def p_list_with_data(p):
    'list_with_data : LBRACE values RBRACE'

def p_defined_list(p):
    'defined_list : TYPE VARIABLE LBRACE values RBRACE'


t_ignore = ' \t'



def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}', line {p.lineno}")
    else:
        print("Syntax error: unexpected end of input")


# Construcción del parser
parser = yacc.yacc()

