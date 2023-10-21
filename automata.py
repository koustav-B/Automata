import re
import time
import matplotlib.pyplot as plt  # Import matplotlib

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
        self.line = 1
        self.column = 1

    def add_token(self, name, regex):
        token = Token(name, regex)
        self.tokens.append(token)

    def tokenize(self, input):
        result = []
        lines = input.split('\n')
        for line_text in lines:
            self.line += 1
            self.column = 1
            line_input = line_text
            while line_input:
                match = False
                for token in self.tokens:
                    match_obj = token.match(line_input)
                    if match_obj:
                        match = True
                        lexeme = match_obj.group().strip()
                        token.count += 1  # Increment the count

                        # Handle escaped characters in strings and characters
                        if token.name in ["STRING", "CHAR"]:
                            lexeme = lexeme.replace("\\n", "\n")
                            lexeme = lexeme.replace("\\t", "\t")
                            # Handle other escape sequences as needed

                        # Store token position information
                        token_position = (self.line, self.column)

                        result.append(f'{token.name}: {lexeme} at Line {token_position[0]}, Column {token_position[1]}')
                        
                        if token.name != "NEWLINE":
                            self.column += len(lexeme)
                        line_input = line_input[len(lexeme):].strip()
                        break
                if not match:
                    # Handle lexer errors or unknown tokens and attempt error recovery
                    error_column = self.column
                    error_char = line_input[0]
                    print(f'Lexer Error: Unable to tokenize input at Line {self.line}, Column {error_column} - Unexpected character: {error_char}')
                    self.column += 1
                    line_input = line_input[1:]
                if not line_input:
                    break
        return result

def input_from_file():
    file_path = input("Enter the input file name: ")
    try:
        with open(file_path, 'r') as file:
            input_text = file.read()
            return input_text
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    return None

def input_directly():
    code = input("Enter code directly. Type 'exit' on a new line to finish:\n")
    input_text = ""
    while code.strip() != "exit":
        input_text += code + '\n'
        code = input()
    return input_text

def main():
    lexer = Lexer()

    # Define your tokens with regular expressions
    lexer.add_token("NUMBER", r'0x[0-9A-Fa-f]+|0[0-7]*|\d+')
    lexer.add_token("FLOAT", r'\d+\.\d+')
    lexer.add_token("ID", r'[a-zA-Z_]\w*')
    lexer.add_token("STRING", r'"(?:\\.|[^"])*"')
    lexer.add_token("CHAR", r"'(?:\\.|[^\\'])*'")
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
    lexer.add_token("COMMENT_MULTI", r'/\*(.|\n)*?\*/')
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

    while True:
        print("Choose an option:")
        print("1. Enter a file name")
        print("2. Enter code directly")
        print("3. Exit")
        choice = input("Enter the option number: ")

        if choice == "1":
            input_text = input_from_file()
            if input_text is not None:
                process_input(input_text, lexer)
        elif choice == "2":
            input_text = input_directly()
            process_input(input_text, lexer)
        elif choice == "3":
            break
        else:
            print("Invalid option. Please select a valid option.")

def process_input(input_text, lexer):
    start_time = time.time()  # Measure start time
    tokens = lexer.tokenize(input_text)
    end_time = time.time()  # Measure end time

    print("\nTokenized output:")
    for token in tokens:
        print(token)

    elapsed_time = end_time - start_time
    print(f"\nTime taken: {elapsed_time:.6f} seconds")

    print("\nToken Counts:")
    for token in lexer.tokens:
        print(f'{token.name}: {token.count} occurrences')

    # Visualize token counts as a bar chart
    visualize_token_counts(lexer)

def visualize_token_counts(lexer):
    token_names = [token.name for token in lexer.tokens]
    token_counts = [token.count for token in lexer.tokens]

    plt.figure(figsize=(12, 6))
    plt.bar(token_names, token_counts)
    plt.title('Token Counts')
    plt.xlabel('Tokens')
    plt.ylabel('Counts')

    for i, count in enumerate(token_counts):
        plt.text(i, count, str(count), ha='center', va='bottom')

    plt.xticks(rotation=90)
    plt.show()

if __name__ == "__main__":
    main()
