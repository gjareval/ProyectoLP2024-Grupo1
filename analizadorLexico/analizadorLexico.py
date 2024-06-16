import ply.lex as lex
import errorsList as errorsList

# Reserved words
reserved = {
    # Guillermo Arevalo
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
    'switch':'SWITCH' ,    

    # Maria Jose Moyano
    'bool':'BOOL', 
    'int':'INTSTATE', 
    'int32':'INT32STATE',       
    'int64':'INT64STATE',  
    'float':'FLOATSTATE',   
    'float32':'FLOAT32STATE',    
    'float64':'FLOAT64STATE',   
    'string':'STRINGSTATE',      
}

# List of tokens     names
tokens = (
    # Guillermo Arevalo
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'AND',
    'OR',
    'NOT',
    'ASSIG',
    'PLUSASSIG',
    'MINUSASSIG',
    'TIMESASSIG',
    'DIVIDEASSIG',
    'MODASSIGN',
    'EQUALS',
    'DIFFERENT',
    'LESS',
    'LESSEQUALS',
    'GREATER',
    'GREATEREQUALS',
    'INCREMENT',
    'DECREMENT',
    'CHARSTRING',
    # Maria Jose Moyano
    'LPAREN',
    'RPAREN',
    'COMMA',
    'COLON',
    'PRINT',
    'INPUT',
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
t_DIFFERENT = r'!='
t_LESS = r'<'
t_LESSEQUALS = r'<='
t_GREATER = r'>'
t_GREATEREQUALS = r'>='
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'

# Regular expressions for complex tokens

def t_CHARSTRING(t):
    r'\"[^\"]*\"'
    t.type = reserved.get(t.value,'CHARSTRING')
    return t

def t_VARIABLE(t):
    r'[_a-zA-Z]\w*'
    t.type = reserved.get(t.value,'VARIABLE')
    return t

def t_FLOAT(t):
    r'\-?\d+\.\d+'
    t.value=float(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)    
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    line = t.lineno
    position = t.lexpos - t.lexer.lexdata.rfind("\n", 0, t.lexpos)
    errorsList.errors.append(f"Illegal character ('{t.value[0]}',{line},{position})")
    t.lexer.skip(1)

# To print in console
def t_PRINT(t):
    r'fmt\.Print(ln)?'
    return t

# Enter data via console
def t_INPUT(t):
    r'fmt\.Scan(ln)?'
    return t

# Construir lexer
lexer = lex.lex()