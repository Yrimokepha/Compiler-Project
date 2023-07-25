########
# TOKENS
# these are simple objects which have a type and optionaly a value
#######

# Define a few constants
TT_INT = 'TT_INT'
TT_FLOAT= 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV='DIV'
# For the left and right parentheses
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
# TT represents Token Type


class Token:
    def __init__(self,type_,value):
        self.type= type_
        self.value= value

# Representation method makes it look nice when printed on to the terminal window
# if the token has a value it will print the type : and the value
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    
########################
# LEXER 
########################
class Lexer:
    def __init__(self,text):
        self.text=text
        self.pos= -1  #(start with -1 cause the advance function will immediately change it to 0)
        self.current_char= None
        self.advance()

# define an advance message that will advance to the next character in the text
def advance(self):
    self.pos += 1
    self.current_char = self.text[pos] if self.pos < len(self.text) else None

# create a make_tokens method
def make_tokens(self):
    tokens=[]

    while self.current_char != None:
        if self.current_char in '\t':
            self.advance()
        elif self.current_char == '+':
            tokens.append(Token(TT_PLUS))
            self.advance()
        elif self.current_char == '-':
            tokens.append(Token(TT_MINUS))
            self.advance()
        elif self.current_char == '*':
            tokens.append(Token(TT_MUL))
            self.advance()
        elif self.current_char == '/':
            tokens.append(Token(TT_DIV))
            self.advance()

