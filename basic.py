###################
# CONSTANTS
###################
DIGITS = '0123456789'

###################
# ERRORS
##################

class Error:
    def __init__(self, pos_start, pos_end, error_name,details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    def as_string(self):
        result =f'{self.error_name}: {self.details}'
        result += f'File {self.pos_start.file_name}, line {self.pos_start.line + 1}'
        return result
    
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character',details)

###################
#POSITION- keeps track of the line number column number and index
###################
class Position:
    def __init__(self, index, line, col, file_name, file_text):
        self.index= index
        self.line= line
        self.col= col
        self.file_name = file_name
        self.file_text = file_text

    def advance(self, current_char):
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.line += 1
            self.col = 0
        return self
    
# Create a copy of the current position
    
    def copy(self):
        return Position(self.index, self.line, self.col, self.file_name, self.file_text)

########
# TOKENS
# these are simple objects which have a type and optionaly a value
#######

# Define a few constants
TT_INT = 'INT'
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
    def __init__(self,type_,value=None):
        self.type= type_
        self.value= value

# Representation method makes it look nice when printed on to the terminal window
# if the token has a value it will print the type : and the value
    def __repr__(self):
        if self.value: 
            return f'{self.type}:{self.value}'
        return f'{self.type}'
    
########################
# LEXER 
########################
class Lexer:
    def __init__(self, file_name, text):
        self.file_name= file_name
        self.text=text
        self.pos= Position(-1, 0, -1, file_name, text) #start with -1 cause the advance function will immediately change it to 0
        self.current_char= None
        self.advance()

# define an advance message that will advance to the next character in the text
    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index] 
        else:
            self.current_char = None

# create a make_tokens method
    def make_tokens(self):
        tokens= []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
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
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return[], IllegalCharError(pos_start, self.pos, "'" + char + "'")
    
            
        return tokens, None
    
    def make_number(self):
        num_str= ''
        dot_count= 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count +=1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
            

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
        
#######################
# NODES
#######################
class NumberNode:
    def __init__ (self,tok):
        self.tok=tok  

    def __repr__ (self):
        return f'{self.tok}'    

class BinOpNode:
    def __init__ (self,left_node, op_tok, right_node):
        self.left_node= left_node
        self.op_tok= op_tok
        self.right_node= right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'  
    
###################
# PARSER
##################

class Parser:
    def __init__ (self,tokens):
        self.tokens=tokens
        self.tok_index=1
        self.advance()

    def advance(self):
        self.tok_index += 1
        if self.tok_index < len(self.tokens):
            self.current_tok = self.tokens[self.tok_index]
        return self.current_tok 
#################################
    def parse(self):
        res= self.expression()
        return res  
          
    def factor(self):
        tok= self.current_tok
        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)


    def term(self):
        return self.bin_op(self.factor,(TT_MUL, TT_DIV))
       
    def expression(self):
        return self.bin_op(self.factor,(TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
         left = func()

         while self.current_tok.type in ops:
             op_tok=self.current_tok
             self.advance()
             right=func
             left=BinOpNode(left, op_tok, right)

         return left

        

######################
# RUN
######################
def run(file_name, text):
    # Generate tokens
    lexer = Lexer(file_name,text)
    tokens,error=lexer.make_tokens()
    if error: return None, error

    #Generate AST
    parser = Parser(tokens)
    ast=parser.parse()

    return ast, None
