import sys

# global constants
COMM_START = "/$"
COMM_END = '$/'
KEYWORD = 'KEYWORD'
KEYWORDS = {'and', 'break', 'continue', 'else', 'false', 'for', 'if', 'mod',\
    'not', 'or', 'then', 'true', 'void', 'while', 'return'}
DATA_TYPES = {'bool', 'char', 'int', 'float'}
REL_OPS = {'<', '<=', '>', '>=', '==', '!='}
ARITH_OPS = {"+","-","*","/","^"}
PUNCTUATION = {'=', '{', '}', '(', ')', ';', '[', ']', "'" ,'”' , ','}

# global vars
token_stream = ""
found_comment = False
table_ptr = 1
id_info = dict()

def check_sym_type(sym: str, peek_ahead:str = "") -> str:
    global found_comment
    global id_info
    
    if sym == COMM_END:
        found_comment = False
        return
    
    if found_comment:
        return

    if sym == COMM_START:
        found_comment = True
        return

    if sym in KEYWORDS:
        handle_keyword(sym)
        return
    elif sym in DATA_TYPES:
        handle_data_type(sym)
        return
    elif sym in REL_OPS or sym+peek_ahead in REL_OPS:
        handle_rel_ops(sym, peek_ahead)
        return
    elif sym in ARITH_OPS or sym+peek_ahead in ARITH_OPS:
        handle_arith_ops(sym, peek_ahead)
        return
    elif sym in PUNCTUATION:
        handle_punctuation(sym)
        return
    elif handle_num(sym):
        return

    # HANDLE IDENTIFIERS HERE
    else:
        handle_identifier(sym)

    return

def handle_keyword(sym: str):
    global token_stream
    
    token_stream += f'<{sym}>'
    return

def handle_data_type(sym: str):
    global token_stream
    
    token_stream += f'<dt,{sym}>'
    return


def handle_num(sym: str):
    global token_stream
    global id_info
    global table_ptr
    try:
        _ = float(sym)
        # add to symbol table
        id_info[table_ptr] = sym
        token_stream += f'<num, {table_ptr}>'
        table_ptr += 1
        return True
    except (TypeError, ValueError):
        return False

def handle_rel_ops(sym: str, peek_ahead: str):
    global token_stream
    if sym in REL_OPS:
        token_stream += f'<rel_op, {sym}>'
    else:
        token_stream += f'<rel_op, {sym+peek_ahead}>'
    return

def handle_arith_ops(sym: str, peek_ahead: str):
    global token_stream
    if sym+peek_ahead in ARITH_OPS:
        token_stream += f'<{sym+peek_ahead}>'
    else:
        token_stream += f'<{sym}>'
    
    return

def handle_punctuation(sym: str):
    global token_stream
    token_stream += f'<{sym}>'
    return

def handle_identifier(sym: str):
    global token_stream
    global id_info
    global table_ptr


    #if not sym[0].isalpha():
    #    print("unrecognized symbol")
    #    return


    # check if punctuation mark is in sym string
    if any(punc in sym for punc in PUNCTUATION):
        # split sym into a list of groups of chars and punctuation
        sym_list = []
        temp = ""
        for char in sym:
            if char in PUNCTUATION:
                if temp:
                    sym_list.append(temp)
                sym_list.append(char)
                temp = ""
            else:
                temp += char
                
        if temp:
            sym_list.append(temp)

        for sym in sym_list:
            check_sym_type(sym)
    else:
        # check if sym is in symbol table
        if sym in id_info.values():
            # get the key
            key = list(id_info.keys())[list(id_info.values()).index(sym)]
            token_stream += f'<id,{key}>'
        else:
            # add to symbol table
            id_info[table_ptr] = sym
            token_stream += f'<id,{table_ptr},{sym}>'
            table_ptr += 1

    return

def main(filename):
    global token_stream
    global found_comment
    global id_info

    # !! To take arg from cmdline 
    if len(sys.argv) < 2:
        print(" Please provide a valid file to analyse!")
        print(" Usage: python3 analyser.py <file_name>")
        exit(1)
    
    with open(filename, 'r') as src:
        src_lines = src.readlines()
        
        # read one line to tokenize
        for line in src_lines:
            symbols = line.split()
            for i, symbol in enumerate(symbols):
                peek_ahead = symbols[i+1] if i+1 < len(symbols) else ""
                check_sym_type(symbol, peek_ahead)
                

    # write symbol table and token stream
    file_prefix = sys.argv[1].split('.')
    if file_prefix[1] == 'tpl':
        file_prefix = file_prefix[0]
    else:
        file_prefix = file_prefix[1][1:] # win32 file naming support

    with open(f'{file_prefix}.out', 'w') as out_file:
        out_file.write(token_stream)
    
    with open(f'{file_prefix}.sym', 'w') as sym_file:
        # write a dict to file
        for key, value in id_info.items():
            sym_file.write(f'{key}\t{value}\n')
    
    
    # # print(id_info.keys)

    # for i in id_info.keys():
    #     print(i, id_info[i])

    # exit(0)

    return token_stream, id_info


main("test2.txt")
