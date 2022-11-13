def read_lex_output(lex_output):
    tokens = []
    for token in lex_output.split(">"):
        if token:
            tokens.append(token.split(","))
    return tokens

#remove < from string
def remove_brackets(tokens):
    for i in range(len(tokens)):
        tokens[i][0] = tokens[i][0][1:]
    return tokens

lex_output = "<dt,int><id, 1><(><void><)><{><dt,int><id, 2><[><]><;><dt,int><id, 3><=><num, 4><;><while><(><id, 3><rel_op, >><num, 5><)><{><id, 2><[><id, 3><]><=><(><><id, 3><)><+><num, 6><><num, 7><;><id, 3><=><id, 3><-><num, 8><;><}><return><num, 9><;><}>"

# print(read_lex_output(lex_output))
# print(remove_brackets(read_lex_output(lex_output)))

x = "1"

match x:
    case "h":
        print("hello")
    case _:
        print("no")
