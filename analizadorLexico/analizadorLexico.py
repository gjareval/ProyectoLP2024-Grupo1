import ply.lex as lex

# Reserved words
reserved = {
    'break':'BREAK',
    'case':'CASE',
    'const':'CONTS',
    'continue':'CONTINUE',
    'default':'DEFAULT',
    'if':'IF',            
    'else':'ELSE',
    'for':'FOR',  
    'import':'IMPORT',
    'map':'MAP',
    'package':'PACKAGE',
    'return':'RETURN', 
    'struct':'STRUCT',
    'type':'TYPE',  
    'var':'VAR',
    'switch':'SWITCH'       
}

# List of tokens     names
tokens = (
    #ARITHMETIC
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    #LOGIC
    'MOD',
    'AND',
    'OR',
    'NOT',
    #ASSIGNATION
    'ASSIG',
    'PLUSASSIG',
    'MINUSASSIG',
    'TIMESASSIG',
    'DIVIDEASSIG',
    'MODASSIGN',
    #COMPARATION
    'EQUALS',
    'DIFFERENT',
    'LESS',
    'LESSEQUALS',
    'GREATER',
    'GREATEREQUALS',
    #OTHERS
    'INCREMENT',
    'DECREMENT',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'COLON',
    #COMPLEX
    'VARIABLE',
    'FLOAT',
    'INT'
   

)+tuple(reserved.values())

# Regular expressions for simple tokens

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD = r'\%'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'\!'
t_ASSIG = r'=='
t_PLUSASSIG = r'\+='
t_MINUSASSIG = r'-='
t_TIMESASSIG = r'\*='
t_DIVIDEASSIG = r'/='
t_MODASSIGN = r'\%='
t_EQUALS = r'='

# Regular expressions for complex tokens

def t_VARIABLE(t):
    r'[_a-zA-Z]\w*'
    t.type = reserved.get(t.value,'VARIABLE')
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value=float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_ignore_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir lexer
lexer = lex.lex()