#match characters
from xml.etree.ElementTree import TreeBuilder
from analyser import main
from symTable import *


global glob_table
global scope
scope = 0

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

test,id_info = main("test3.txt")

global token_list
token_list = remove_brackets(read_lex_output(test))
token_list.append(["EOF"])
print(token_list)


# #string for writing error messages



global index
global token_string

index = 0

def match(char):
    global index
    # print(index, len(token_list)-1)
    if token_list[index] == "EOF":
        # print('sup')
        return

    else:
        str = token_list[index][0]

        # print("str:",str,"  char:", char)

        if str == char:
            index +=1
            return True

        else:

            return False



def Program(): #function definition & will have synthesised attribute

    global scope

    glob_table[scope] = {}
    
    entry = Id()
    entry.in_scope = scope

    # entry.scope = scope

    # print("here")
    if match('dt'):
        entry.return_type = token_list[index-1][1]
        # id_type = token_list[index-1][1]
        # print(dt_type)
        if match('id'):
            entry.name = token_list[index-1][1]
            if match('('):
                # print('sup2')
                entry.next = dict()
                scope += 1
                entry.next[scope] = {}

                arg_list = []


                if ParamList(arg_list, scope):
                    s = ""
                    #cocatenates parameter types and inserts into function type
                    for i in arg_list:
                        s = s + i.type

                    entry.next[scope] = s
                    if match(')'):
                        arg_list = []
                        scope -= 1
                        # print('broter')
                        if match('{'):
                            scope += 1
                            if Stmts():
                                if match('}'):
                                    scope -= 1
                                    return True, 'lesgoo'
                                else:
                                    return False, "punctuator '}' expected but wasn't provided"
                            else:
                                return False, "statements expected but weren't provided"
                        else:
                            return False, "punctuator '{' expected but wasn't provided"
                    else:
                        return False, "punctuator ')' expected but wasn't provided"
                else:
                    return False, "parameter(s) expected but wasn't provided"
            else:
                return False, "punctuator '(' expected but wasn't provided"
        else:
            return False, "missing/unrecognized identifier"                
    else:
        return False, "missing incorrect datatype"


def ParamList(arg_list, scope_count):
    
    var_entry = Id()
    var_entry.in_scope = scope_count

    if match('dt'):
        # print('alpha')
        var_entry.type = token_list[index-1][1]
        arg_list.append(var_entry)

        if match('id'):
            # print('beta')
            var_entry.name = token_list[index-1][1]

            if PList(arg_list, scope_count):
                return True, arg_list
            else:
                return True, arg_list, 
        else:
            return False, "missing/unrecognized identifier"
    else:
        return False, "missing/incorrect datatype"


def PList(arg_list,scope_count):
    var_entry = Id()
    var_entry.in_scope = scope_count
    
    if match('?'):
        if match('dt'):
            var_entry.type = token_list[index-1][1]
            # print('hello')
            if match('id'):
                var_entry.name = token_list[index-1][2]
                # print(token_list[index-1][2])
                arg_list.append(var_entry)
                # if token_list[index][0] == ',':
                #     PList(arg_list, scope_count)
                
                # else:
                #     return 
                if PList():
                    return True
    else:
        # print('pls')
        # if match(')'):
        #     return True
        return False, "punctuator '?' or ')' expected but wasn't provided"


def F():
    # print(token_list[index])
    if match('id'):
        return True

    elif match('('):
        # print('here')
        if (E()):
            # print('over')
            if (match(')')):
                return True
            else:
                return False, "punctuator ')' expected but wasn't provided"
        else:
            return False,"expression expected but wasn't provided"
            
    else:
        return False, "punctuator '(' or identifier expected but wasn't provided"

def T_prime():
    # print('hello2')
    if (match('*')):
        # print('ello3')
        if (F()):
            if (T_prime()):
                # print('nub')
                return True
        else:
            return False, "factor expected but wasn't provided"
    else:
        # print('hello')
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
        return False, "identifier expected but wasn't provided"



def DecStmts():
    # print("in dec")
    if match('dt'):
        # print('here')
        if match('id'):
            if OptionalAssign():
                print('bhaijaan')
                return True
            else:
                if List():
                    return True
        else:
            return False,"missing/unrecognized identifier"
    else:
        return False, "missing/incorrect datatype"


def OptionalAssign():
    if (match('=')):
        if (E()):
            if match(';'):
                # print('mayn')
                return True
            else:
                return False
                         
    else:
        return True

def List():
    if match('?'):
        if match('dt'):
            if OptionalAssign():
                return True
            else:
                if List():
                    return True
        else:
            return False, "no dt given"
    else:
        return False, "error"


def ForStmt():
    # print('pls')
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
                                                                    # print('heehee')
                                                                    if match('}'):
                                                                        return True
                                                                    else:
                                                                        return False, "punctuator '}' expected but wasn't provided"
                                                            else:
                                                                return False, "punctuator '{' expected but wasn't provided"
                                                        else:
                                                            return False, "punctuator ')' expected but wasn't provided"
                                                    else:
                                                        return False, "punctuator + expected but wasn't provided"
                                                else:
                                                    return False, "punctuator + expected but wasn't provided"
                                            else:
                                                return False, "identifier expected but wasn't provided"
                                        else:
                                            return False, "punctuator ';' expected but wasn't provided"
                                else:
                                    return False, "relational operator expected but wasn't provided"
                        else:
                            return False, "punctuator ';' expected but wasn't provided"
                else:
                    return False, "identifier expected but wasn't provided"

   
        else:
            return False, "punctuator '(' expected but wasn't provided"
    else:
        return False, "keyword 'for' expected but wasn't provided"

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
                                        return False, "punctuator '}' expected but wasn't provided"
                            else:
                                return False, "punctuator '{' expected but wasn't provided"
                        else:
                            return False, "punctuator ')' expected but wasn't provided"
                else:
                    return False, "relational operator expected but wasn't provided"
        else:
            return False, "punctuator '(' expected but wasn't provided"
    else:
        return False, "keyword 'if' expected but wasn't provided"


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
                return False, "punctuator ';' expected but wasn't provided"
        else:
            return False, "expression expected but wasn't provided"
    else:
        return False, "keyword 'return' expected but wasn't provided"

def Stmts():
    if S_prime():
        return True

def S_prime():
    if token_list[index] == '}':
        pass
    elif DecStmts():
        return True

    elif AssignStmt():
        return True
    elif ForStmt():
        return True
    
    elif IfStmt():
        return True

    elif ReturnStmt():
        return True

    else:
        return False
        # if S_prime():
        #     return True
        # else:
        #     return False, 'something wrong with statements'

def test():

    test = Program()
    # print(test)
    if test[0]:
        print(test[1])
        # print("string is accepted")
    else:
        print("string is not accepted")
        print("Error:",test[1])
        


test()