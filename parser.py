#match characters
from analyser import main
from symTable import *


global glob_table

glob_table = dict()

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

test,id_info = main("test1.txt")
# print(id_info)
# print(test)
# input_string = "<dt,int><id, 1><(><void><)><{><dt,int><id, 2><[><]><;><dt,int><id, 3><=><num, 4><;><while><(><id, 3><rel_op, >><num, 5><)><{><id, 2><[><id, 3><]><=><(><><id, 3><)><+><num, 6><><num, 7><;><id, 3><=><id, 3><-><num, 8><;><}><return><num, 9><;><}>"
# test = "<dt><id><(><dt><id><)><{><}><;>"
# <dt,int> <id,main> <(> <dt, int> <id,a> <)> <{> <}> <;>
global token_list
token_list = remove_brackets(read_lex_output(test))

print(token_list)


# #string for writing error messages

global error_string
error_string = ""

global index
index = 0

def match(char):
    print(char)
    global index
    global token_list

    var = None
    if token_list[index][0] == char:
        # print(char)
        if char == 'dt' and len(token_list[index]) == 2:
            # print(token_list[index],"hello")
            var = token_list[index][1]  
            print(var)
            # return True, var

        elif char == 'id' and len(token_list[index]) == 3:
            var = token_list[index][2]
            print(var)
            # return True, var
        index += 1
        return True, var
    return False, var 



def Program(): #function definition & will have synthesised attribute


    glob_table[scope_count] = {}
    
    entry = Id()
    entry.scope = scope_count

    # print("here")
    if match('dt'):
        entry.return_type = token_list[index-1][1]
        # id_type = token_list[index-1][1]
        # print(dt_type)
        if match('id'):
            entry.name = token_list[index-1][1]
            if match('('):
                arg_list = []
                if ParamList(arg_list, scope_count):
                    # for i in arg_list:
                    #     print(i)
                    if match(')'):
                        if match('{'):
                            if S_prime():
                                if match('}'):
                                    return True
                                else:
                                    return "punctuator '}' expected but wasn't provided"
                            else:
                                return "statements expected but weren't provided"
                        else:
                            return "punctuator '{' expected but wasn't provided"
                    else:
                        return "punctuator ')' expected but wasn't provided"
                else:
                    return "parameter(s) expected but wasn't provided"
            else:
                return "punctuator '(' expected but wasn't provided"
        else:
            return "missing/unrecognized identifier"                
    else:
        return False


def ParamList(arg_list, scope_count):

    var_entry = Id()
    var_entry.in_scope = scope_count
    if match('dt'):
        var_entry.type = token_list[index-1][1]
        if match('id'):
            var_entry.name = token_list[index-1][1]
            arg_list.append(var_entry)
            # if token_list[index][0] == ',':
            #     Plist(arg_list, scope_count)
            if PList(arg_list, scope_count):
                return True, arg_list
            else:
                return True
        else:
            return False, "missing/unrecognized identifier"
    else:
        return False, "missing/incorrect datatype"


def PList(arg_list,scope_count):
    var_entry = Id()
    var_entry.in_scope = scope_count

    if match(','):
        if match('dt'):
            var_entry.type = token_list[index-1][1]
            print('hello')
            if match('id'):
                var_entry.name = token_list[index-1][2]
                print(token_list[index-1][2])
                arg_list.append(var_entry)
                if token_list[index][0] == ',':
                    PList(arg_list, scope_count)
                
                else:
                    return
    else:
        print('pls')
        if match(')'):
            return True
        return False, "punctuator ',' or ')' expected but wasn't provided"

# def Plist():
#     if (match(',')):
#         if (E()):
#             if (Plist()):
#                 return True
#         else:
#             return False, "expression expected but wasn't provided"
#     else:
#         return True

def F():
    if (match('(')):
        if (E()):
            if (match(')')):
                return True
            else:
                return False, "punctuator ')' expected but wasn't provided"
        else:
            return False,"expression expected but wasn't provided"
            
    elif (match('id')):
        return True
    else:
        return False, "punctuator '(' or identifier expected but wasn't provided"

def T_prime():
    if (match('*')):
        if (F()):
            if (T_prime()):
                return True
        else:
            return False, "factor expected but wasn't provided"
    
    else:
        return True
    
def T():
    if (F()):
        if (T_prime()):
            return True
    else:
        return False, "factor expected but wasn't provided"

def E_prime():
    if (match('+')):
        if (T()):
            if (E_prime()):
                return True
    else:
        return True

def E():
    if (T()):
        if (E_prime()):
            return True

    else:
        return False, "term expected but wasn't provided"

def AssignStmt():
    if (match('id')):
        if (match('=')):
            if (E()):
                if match(';'):
                    return True

                else:
                    return False,"punctuator ';' expected but wasn't provided"
            else:
                return False,"expression expected but wasn't provided"
        else:
            return False,"punctuator '=' expected but wasn't provided"
    else:
        error_string = "identifier expected but wasn't provided"
        return False

def OptionalAssign():
    if (match('=')):
            if (E()):
                if match(';'):
                    return True            
    else:
        return True

def List():
    if match(','):
        if match('dt'):
            if OptionalAssign():
                if List():
                    return True
    else:
        return True

def DecStmts():
    if match('dt'):
        if match('id'):
            if OptionalAssign():
                if List():
                    return True
                    
        else:
            return False,"missing/unrecognized identifier"
    else:
        error_string = "missing/incorrect datatype"
        return False


def ForStmt():
    if match('for'):
        if match('('):
            if Type():
                if match('id'):
                    if E():
                        if match(';'):
                            if E():
                                if match('relop'):
                                    if E():
                                        if match(';'):
                                            if match('id'):
                                                if match('+'):
                                                    if match('+'):
                                                        if match(')'):
                                                            if match('{'):
                                                                if Stmts():
                                                                    if match('}'):
                                                                        return True
                                                                    else:
                                                                        error_string = "punctuator '}' expected but wasn't provided"
                                                                        return False
                                                            else:
                                                                error_string = "punctuator '{' expected but wasn't provided"
                                                                return False
                                                        else:
                                                            error_string = "punctuator ')' expected but wasn't provided"
                                                            return False
                                                    else:
                                                        error_string = "punctuator '+' expected but wasn't provided"
                                                        return False
                                                else:
                                                    error_string = "punctuator '+' expected but wasn't provided"
                                                    return False
                                            else:
                                                error_string = "identifier expected but wasn't provided"
                                                return False
                                        else:
                                            error_string = "punctuator ';' expected but wasn't provided"
                                            return False
                                else:
                                    error_string = "relational operator expected but wasn't provided"
                                    return False
                        else:
                            error_string = "punctuator ';' expected but wasn't provided"
                            return False
                else:
                    error_string = "identifier expected but wasn't provided"
                    return False

   
        else:
            error_string = "punctuator '(' expected but wasn't provided"
            return False
    else:
        error_string = "keyword 'for' expected but wasn't provided"
        return False

def Type():
    if match('dt'):
        return True
    else:
        return True

def IfStmt():
    if match('if'):
        if match('('):
            if E():
                if match('relop'):
                    if E():
                        if match(')'):
                            if match('{'):
                                if Stmts():
                                    if match('}'):
                                        if OptionalElse():
                                            return True
                            
                                    else:
                                        error_string = "punctuator '}' expected but wasn't provided"
                                        return False
                            else:
                                error_string = "punctuator '{' expected but wasn't provided"
                                return False
                        else:
                            error_string = "punctuator ')' expected but wasn't provided"
                            return False
                else:
                    error_string = "relational operator expected but wasn't provided"
                    return False
        else:
            print('here')
            error_string = "punctuator '(' expected but wasn't provided"
            return False
    else:
        error_string = "keyword 'if' expected but wasn't provided"
        return False



def OptionalElse():
    if match('else'):
        if match('{'):
            if Stmts():
                if match('}'):
                    return True
    
    else:
        return True


def ReturnStmt():
    if match('return'):
        if E():
            if match(';'):
                return True
            else:
                error_string = "punctuator ';' expected but wasn't provided"
                return False
        else:
            error_string = "expression expected but wasn't provided"
            return False
    else:
        error_string = "keyword 'return' expected but wasn't provided"
        return False

def S_prime():
    if Stmts():
        return True

def Stmts():
    if DecStmts():
        if Stmts():
            return True
        else:
            return False
    elif AssignStmt():
        if Stmts():
            return True
        else:
            return False
    elif ForStmt():
        if Stmts():
            return True
        else:
            return False
    elif IfStmt():
        if Stmts():
            return True
        else:
            return False
    elif ReturnStmt():
        if Stmts():
            return True
        else:
            return False
    else:
        return True

def test():
    global error_string
    test = Program()
    if test:
        print("string is accepted")
    else:
        print("string is not accepted")
        print(error_string)


test()