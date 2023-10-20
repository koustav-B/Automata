import re
import time

class Token:
    def __init__(self, name, regex):
        self.name = name
        self.pattern = re.compile(regex)
        self.count = 0  # Initialize the count to 0

    def match(self, input):
        return self.pattern.match(input)

class Lexer:
    def __init__(self):
        self.tokens = []

    def add_token(self, name, regex):
        token = Token(name, regex)
        self.tokens.append(token)

    def tokenize(self, input):
        result = []
        line = 1
        column = 1
        lines = input.split('\n')
        for line_text in lines:
            line_input = line_text
            while line_input:
                match = False
                for token in self.tokens:
                    match_obj = token.match(line_input)
                    if match_obj:
                        match = True
                        lexeme = match_obj.group().strip()
                        token.count += 1  # Increment the count
                        if token.name != "NEWLINE":
                            result.append(f'{token.name}: {lexeme} at Line {line}, Column {column}')
                            if token.name != "WHITESPACE":
                                column += len(lexeme)
                        line_input = line_input[len(lexeme):].strip()
                        break
                if not match:
                    # Handle lexer errors or unknown tokens
                    print(f'Lexer Error: Unable to tokenize input at Line {line}, Column {column} - Unexpected character: {line_input[0]}')
                    break
                if not line_input:
                    break
            line += 1
            column = 1
        return result

lexer = Lexer()

# Define your tokens with regular expressions
lexer.add_token("NUMBER", r'0x[0-9A-Fa-f]+|0[0-7]*|\d+')
lexer.add_token("FLOAT", r'\d+\.\d+')
lexer.add_token("ID", r'[a-zA-Z_]\w*')
lexer.add_token("STRING", r'"[^"]*"')
lexer.add_token("CHAR", r"'(\\.|[^\\'])'")
lexer.add_token("PLUS", r'\+')
lexer.add_token("MINUS", r'-')
lexer.add_token("MULTIPLY", r'\*')
lexer.add_token("DIVIDE", r'/')
lexer.add_token("MODULUS", r'%')
lexer.add_token("BITWISE_AND", r'&')
lexer.add_token("BITWISE_OR", r'\|')
lexer.add_token("BITWISE_XOR", r'\^')
lexer.add_token("BITWISE_NOT", r'~')
lexer.add_token("ASSIGNMENT_OP", r'[-+*/%&|^\w]+=')
lexer.add_token("LEFT_SHIFT", r'<<')
lexer.add_token("RIGHT_SHIFT", r'>>')
lexer.add_token("NEWLINE", r'\n')
lexer.add_token("WHITESPACE", r'\s+')
lexer.add_token("COMMENT_SINGLE", r'//.*')
lexer.add_token("COMMENT_MULTI", r'/\*(.*?)(?=\*/)\*/')
lexer.add_token("KEYWORD", r'(if|else|while|for|int|float|void|true|false)')
lexer.add_token("COMPARISON_OP", r'==|!=|<|>|<=|>=')
lexer.add_token("LOGICAL_OP", r'&&|\|\||!')
lexer.add_token("LEFT_PAREN", r'\(')
lexer.add_token("RIGHT_PAREN", r'\)')
lexer.add_token("LEFT_BRACE", r'{')
lexer.add_token("RIGHT_BRACE", r'}')
lexer.add_token("SEMICOLON", r';')
lexer.add_token("EQUALS", r'=')
lexer.add_token("HASH", r'#')

file_path = input("Enter the input file name: ")

try:
    with open(file_path, 'r') as file:
        input_text = file.read()

        start_time = time.time()  # Measure start time

        tokens = lexer.tokenize(input_text)

        end_time = time.time()  # Measure end time

        print("Token Counts:")
        for token in lexer.tokens:
            print(f'{token.name}: {token.count} occurrences')

        print("\nTokenized output:")
        for token in tokens:
            print(token)

        elapsed_time = end_time - start_time
        print(f"\nTime taken: {elapsed_time:.6f} seconds")

except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
