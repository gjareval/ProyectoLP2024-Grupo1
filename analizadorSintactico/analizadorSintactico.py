# Yacc import
import ply.yacc as yacc
# Token map from the lexer
from analizadorLexico.analizadorLexico import tokens
import errorsList as errorsList

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
              | IMPORT LPAREN values_import RPAREN'''
    
def p_values_import(p):
    '''values_import : CHARSTRING
                     | CHARSTRING values_import'''

def p_package(p):
    'package : PACKAGE VARIABLE'  

def p_main(p):
    'main : FUNCTION MAIN LPAREN RPAREN'  

def p_blocks(p):
    '''blocks : block
              | block blocks'''

def p_block(p):
    '''block : print_statement
             | input_statement
             | conditional_structure
             | operation
             | list_structure
             | map_estructure
             | map_assign
             | for_estructure
             | structure
             | function
             | parameters
             | variable_declaration
             | switch_structure
             | slice_structure
             '''
    
def p_variable_declaration(p):
    '''variable_declaration : VAR VARIABLE type
                            | VAR VARIABLE ASSIGN value
                            | VAR VARIABLE ASSIGN list_structure
                            | VARIABLE SHORTASSIGN value
                            | VARIABLE SHORTASSIGN operation'''
    
def p_structure(p):
    'structure : TYPE VARIABLE STRUCT LBRACE statement RBRACE'

# Tipos de funciones
def p_function(p):
    '''function : FUNCTION VARIABLE LPAREN RPAREN LBRACE blocks RBRACE   
                | FUNCTION VARIABLE LPAREN parameters RPAREN LBRACE blocks RBRACE
                | FUNCTION VARIABLE LPAREN RPAREN type LBRACE RETURN value RBRACE
                | FUNCTION VARIABLE LPAREN parameters RPAREN type LBRACE RETURN value RBRACE
                | FUNCTION VARIABLE LPAREN parameters RPAREN type LBRACE blocks RETURN value RBRACE
                '''

def p_values(p):
    '''values : value 
              | value COMMA values'''

def p_string_value(p):
    '''string_value : value
                    | CHARSTRING'''

def p_value(p):
    ''' value : VARIABLE
              | number
              | CHARSTRING'''
    
def p_number(p):
    '''number : INT
              | FLOAT'''

# Impresión con cero, uno o más argumentos  
def p_print_statement(p):
    '''print_statement : PRINT LPAREN values RPAREN
                       | PRINT LPAREN string_value RPAREN
                       | PRINTF LPAREN FORMATSTRING COMMA values RPAREN
                       | PRINT LPAREN string_value COMMA values RPAREN
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
    
# Estructuras de control

# Maria Jose Moyano 
# Estructura condicional (if)
def p_conditional_structure(p):
    '''conditional_structure : IF conditions conditional_body
                             | IF conditions conditional_body ELSE conditional_body
                             | IF conditions conditional_body ELSE IF conditions conditional_body ELSE conditional_body'''
def p_conditional_body(p):
    '''conditional_body : LBRACE statement RBRACE
                        | LBRACE BREAK RBRACE
                        | LBRACE CONTINUE RBRACE'''

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
    'for_iterator : FOR VARIABLE SEMICOLON VARIABLE SHORTASSIGN RANGE VARIABLE LBRACE statement RBRACE'

# Brian Mite
# Estructura switch
def p_switch_structure(p):
    '''switch_structure : SWITCH switch_expression LBRACE case_blocks RBRACE'''
    
def p_switch_expression(p):
    '''switch_expression : value
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

#Maria Jose Moyano 
# Lista
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


# Guillermo Arevalo
# Map
def p_map_estructure(p):
    '''map_estructure : VARIABLE SHORTASSIGN MAP LBRACKET type RBRACKET type LBRACE map_values RBRACE
                      | VARIABLE SHORTASSIGN MAKE LPAREN MAP LBRACKET type RBRACKET type RPAREN'''

def p_map_values(p):
    '''map_values : map_value
                  | map_value COMMA map_values'''
    
def p_map_value(p):
    '''map_value : string_value COLON string_value'''

def p_map_assign(p):
    'map_assign : VARIABLE LBRACKET string_value RBRACKET ASSIGN string_value'

# Brian Mite
# Slice
def p_slice_structure(p):
    '''slice_structure : VARIABLE SHORTASSIGN LBRACKET RBRACKET type LBRACE values RBRACE
                       | VAR VARIABLE LBRACKET RBRACKET type
                       | VARIABLE SHORTASSIGN LBRACKET RBRACKET type
                       | VARIABLE ASSIGN append_statement'''

def p_append_statement(p):
    'append_statement : APPEND LPAREN VARIABLE COMMA values RPAREN'

t_ignore = ' \t'

def p_error(p):
    if p:
        errorsList.errors.append(f"Syntax error at token '{p.value}'")
    else:
        errorsList.errors.append("Syntax error: unexpected end of input")


# Construcción del parser
parser = yacc.yacc()