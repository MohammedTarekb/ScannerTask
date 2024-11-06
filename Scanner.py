import re

class Token:
    def __init__(self, type: object, value: object) -> object:
        self.type = type
        self.value = value

class LexicalAnalyzer:
    def __init__(self, input):
        self.input = input
        self.current_char = input[0]
        self.position = 0

    def advance(self):
        self.position += 1
        if self.position < len(self.input):
            self.current_char = self.input[self.position]
        else:
            self.current_char = None

    def is_whitespace(self, char):
        return re.match(r'\s', char)

    def is_letter(self, char):
        return re.match(r'[a-zA-Z]', char)

    def is_digit(self, char):
        return re.match(r'\d', char)
    
    def is_operator(self, char):
        operators = ['+','-','=','<','>','==','!=','<=','>=']
        if char in operators:
            return True
        else:
            return False
        

    @property
    def get_next_token(self):
        while self.current_char is not None:
            if self.is_whitespace(self.current_char):
                self.advance()
                continue

            elif self.is_letter(self.current_char):
                keywords = [
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
        'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'False', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'None',
        'not', 'or', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with', 'yield' , 'print']
                letter = ''
                while self.is_letter(self.current_char) or self.is_digit(self.current_char):
                    letter += self.current_char
                    self.advance()
                
                if letter in keywords:
                    return Token('KEYWORD', letter)
                else:
                    return Token('IDENTIFIER', letter)

            elif self.is_digit(self.current_char):
                number = ''
                while self.is_digit(self.current_char):
                    number += self.current_char
                    self.advance()
                return Token('NUMBER', number)
            
            elif self.is_operator(self.current_char):
                operator = ''
                while self.is_operator(self.current_char):
                    operator += self.current_char
                    self.advance()
                return Token('operator', operator)


            elif self.current_char == "'" or self.current_char == '"':
                quote_type = self.current_char  # Remember the type of quote
                char_constant = self.current_char  # Starting quote
                self.advance()

                while self.current_char is not None and self.current_char != quote_type:
                    char_constant += self.current_char
                    self.advance()

                # Close the character constant if there's a matching ending quote
                if self.current_char == quote_type:
                    char_constant += self.current_char
                    self.advance()
                    return Token('CHARACTER_CONSTANT', char_constant)

                # Handle unclosed character constant as an error
                return Token('ERROR', "Unclosed character constant")

                # Special Characters (e.g., parentheses, semicolons)
            else:
                special_char = self.current_char
                self.advance()
                return Token('SPECIAL_CHAR', special_char)

            # Handle other tokens or raise an error for unrecognized characters
            # For simplicity, let's assume keywords are single letters
            current_token = Token(self.current_char, self.current_char)
            self.advance()
            return current_token

        return Token('EOF', None)



input_code = input('please enter the statement\n')
lexer = LexicalAnalyzer(input_code)
print('*'*50)

t_name , t_type = [] , []
token = lexer.get_next_token
while token.type != 'EOF':
    t_name.append(token.value)
    t_type.append(token.type)
    print(f'<Token Type: {token.type} , Value: {token.value}>')
    token = lexer.get_next_token

print('*'*50)
print(t_name,'\n',t_type)
print('*'*50)

    
    

class Parser:
    def __init__(self, t_value, t_type):
        self.t_value = t_value
        self.t_type = t_type
        self.current_value = t_value[0]
        self.current_type = t_type[0]
        self.position = 0
        self.compare_op = ['==', '!=', '>', '<', '>=', '<=']
        self.operations = ['+', '-', '*', '/', '**']
        
    def advance(self):
        self.position += 1
        if self.position < len(self.t_value):
            self.current_value = self.t_value[self.position]
            self.current_type = self.t_type[self.position]
        else:
            self.current_value = None
            self.current_type = None
            
        
    def condition(self, t_value, t_type):
        con = False
        if t_type[self.position] == 'IDENTIFIER' or t_type[self.position] == 'NUMBER':
            self.advance()
            if t_value[self.position] in self.compare_op :
                self.advance()
                if t_type[self.position] == 'IDENTIFIER' or t_type[self.position] == 'NUMBER':
                    con = True
        return con
    
    def assignment(self,t_value,t_type):
        ass= False
        if t_type[self.position] == 'IDENTIFIER':
            self.advance()
            if t_value[self.position]=='++' or t_value[self.position]=='--':
               self.advance()
               if t_value[self.position]==';':
                   return True
            elif t_value[self.position]=='=':
                self.advance()
                if t_type[self.position]=='IDENTIFIER' or t_type[self.position]=='NUMBER':
                    self.advance()
                    if t_value[self.position] ==';':
                        return True
                    while t_value[self.position] !=';':
                       ass= False
                       if t_value[self.position] in self.operations:
                           self.advance() 
                           if t_type[self.position]=='IDENTIFIER' or t_type[self.position]=='NUMBER':
                               self.advance()
                               ass = True
                    return ass
               
        elif t_value[self.position]=='++' or t_value[self.position]=='--':
           self.advance()
           if t_type[self.position] == 'IDENTIFIER':
                self.advance()
                if t_value[self.position]==';':
                    return True
        
        return ass
    
    def statement(self, t_value, t_type):
        if t_value[self.position] == '(':
                self.advance()
                if self.condition(t_value, t_type):
                    self.advance()
                    if t_value[self.position] == ')':
                        self.advance()
                        if t_value[self.position] == '{':
                            self.advance()
                            while self.assignment(t_value, t_type):
                                pass
                                self.advance()
                            if t_value[self.position] == '}':
                                self.advance()
                                return True
                        elif self.assignment(t_value[self.position], t_type[self.position]):
                            self.advance()
                            if t_value[self.position]==';':
                                return True
        return False
                    
    def ifstatement(self, t_value, t_type):
        if t_value[self.position] == 'if':
            self.advance()
            if self.statement(t_value, t_type):
                self.advance()
                return True
                        
        return False
    def whilestatement(self, t_value, t_type):
        if t_value[self.position] == 'while':
            self.advance()
            if self.statement(t_value, t_type):
                self.advance()
                return True
                        
        return False
                

    def get_next_token(self):
        while self.t_value is not None:
            if self.condition(self.current_value, self.current_type):
                print('condition')




pars = Parser(t_name, t_type)
toke = pars.ifstatement(t_name, t_type)
print(toke)


























    
    