import csv  
import re

def lexer(input_string):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),   
        ('ID',       r'[a-zA-Z_]\w*'),  
        ('PLUS',     r'\+'),            
        ('TIMES',    r'\*'),            
        ('LPAREN',   r'\('),            
        ('RPAREN',   r'\)'),            
        ('SKIP',     r'[ \t]+'),        
        ('MISMATCH', r'.'),             
    ]
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    get_token = re.compile(token_regex).match
    line = input_string.strip()
    pos = 0
    tokens = []
    match = get_token(line)
    
    while match is not None:
        type = match.lastgroup
        if type == 'NUMBER':
            tokens.append('id')  
        elif type == 'ID':
            tokens.append('id')
        elif type == 'PLUS':
            tokens.append('+')
        elif type == 'TIMES':
            tokens.append('*')
        elif type == 'LPAREN':
            tokens.append('(')
        elif type == 'RPAREN':
            tokens.append(')')
        elif type == 'SKIP':
            pass
        elif type == 'MISMATCH':
            raise RuntimeError(f'Caractere inválido {match.group()} na posição {pos}')
        pos = match.end()
        match = get_token(line, pos)
    
    if pos != len(line):
        raise RuntimeError(f'Erro inesperado na posição {pos}')
    
    return tokens

def load_input(file_path):
    with open(file_path, 'r') as file:
        input_string = file.read()
    return lexer(input_string)

def load_parsing_table(file_path):
    table = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)[1:]  
        for row in reader:
            row_non_terminal = row[0].strip()  
            table[row_non_terminal] = {}
            for index, cell in enumerate(row[1:]):  
                if index < len(header):  
                    table[row_non_terminal][header[index].strip()] = cell.strip()  
    return table

def parse_input(parsing_table, input_tokens):
    stack = ['$', 'E']  
    input_tokens.append('$')  

    previous_token = None  

    if input_tokens[0] in ['+', '*', ')']:
        return f"Erro: Produção não encontrada para 'E' com símbolo '{input_tokens[0]}'."

    while stack:
        top = stack.pop()
        current_token = input_tokens[0]

        if previous_token in ['+', '*'] and current_token in ['+', '*']:
            return "Erro: Operadores consecutivos sem identificador ou expressão."

        if top == current_token:  
            previous_token = input_tokens.pop(0)
        elif top in parsing_table:  
            if current_token in parsing_table[top]:
                rule = parsing_table[top][current_token]
                if rule not in ['ε', 'Îµ', '']:  
                    symbols_to_push = rule.split()  
                    stack.extend(reversed(symbols_to_push))  
                elif current_token == '$' and previous_token in ['+', '*']:
                    return "Erro: A entrada termina de forma incorreta."
                previous_token = top  
            else:
                return f"Erro: Produção não encontrada para '{top}' com símbolo '{current_token}'."
        else:
            return f"Erro: Símbolo inesperado '{top}' na pilha."

    if previous_token in ['+', '*']:  
        return "Erro: A entrada termina de forma incorreta."

    return "Entrada aceita com sucesso."

def main():
    parsing_table = load_parsing_table('parsing_table.csv')
    input_tokens = load_input('input.txt')
    result = parse_input(parsing_table, input_tokens)
    print(result)

if __name__ == "__main__":
    main()
