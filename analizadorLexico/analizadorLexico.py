import ply.lex as lex
import errorsList as errorsList

# Reserved words
reserved = {
    # Guillermo Arevalo
    'break':'BREAK',
    'case':'CASE',
    'const':'CONST',
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

    # Brian Mite   
    'func': 'FUNCTION',
    'main' : 'MAIN',
    'make' : 'MAKE',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'append' : 'APPEND',
    'range'  : 'RANGE',

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
    'PLUS',             # +
    'MINUS',            # -
    'TIMES',            # *
    'DIVIDE',           # /
    'MOD',              # %
    'AND',              # &&
    'OR',               # ||
    'NOT',              # !
    'ASSIGN',           # =
    'PLUSASSIGN',       # +=
    'MINUSASSIGN',      # -=
    'TIMESASSIGN',      # *=
    'DIVIDEASSIGN',     # /=
    'MODASSIGN',        # %=
    'EQUALS',           # ==
    'DIFFERENT',        # !=
    'LESS',             # <
    'LESSEQUALS',       # <=
    'GREATER',          # >   
    'GREATEREQUALS',    # >=
    'INCREMENT',        # ++
    'DECREMENT',        # --
    'CHARSTRING',
    
    #Brian Mite
    'AMPERSAND',        # &
    'COMMA',            # ,
    'COLON',            # :
    'SEMICOLON',        # ;
    'LBRACE',           # {
    'RBRACE',           # }
    'LBRACKET',         # [
    'RBRACKET',         # ]

    # Maria Jose Moyano
    'LPAREN',           # (
    'RPAREN',           # )
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
t_ASSIGN = r'='
t_PLUSASSIGN = r'\+='
t_MINUSASSIGN = r'-='
t_TIMESASSIGN = r'\*='
t_DIVIDEASSIGN = r'/='
t_MODASSIGN = r'\%='
t_EQUALS = r'=='
t_DIFFERENT = r'!='
t_LESS = r'<'
t_LESSEQUALS = r'<='
t_GREATER = r'>'
t_GREATEREQUALS = r'>='
t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_COMMA = r','
t_COLON = r':'
t_SEMICOLON = r';'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_AMPERSAND = r'&'

# Regular expressions for complex tokens

def t_CHARSTRING(t):
    r'\"[^\"]*\"'
    t.type = reserved.get(t.value,'CHARSTRING')
    return t

def t_FLOAT(t):
    r'\-?\d+\.\d+'
    t.value=float(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)    
    return t


def t_PRINT(t):
    r'fmt\.Print(ln)?'
    return t

def t_INPUT(t):
    r'fmt\.Scan(ln)?'
    return t

def t_VARIABLE(t):
    r'[_a-zA-Z]\w*'
    t.type = reserved.get(t.value,'VARIABLE')
    return t

def t_COMMENT(t):
    r'//.*'
    pass 

def t_COMMENT_MULTI(t):
    r'/\*([^*]|\*(?!/))*\*/'
    pass

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    line = t.lineno
    position = t.lexpos - t.lexer.lexdata.rfind("\n", 0, t.lexpos)
    errorsList.errors.append(f"Illegal character ('{t.value[0]}',{line},{position})")
    t.lexer.skip(1)


# Construir lexer
lexer = lex.lex()