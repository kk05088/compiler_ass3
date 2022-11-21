#match characters
from lib2to3.pgen2 import token
from xml.etree.ElementTree import TreeBuilder
from analyser import main
from sym_table import *


global glob_table
global scope
global arg_list

arg_list = []
scope = 0

glob_table = {}

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

test,id_info = main("test2.txt")

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
        # if token_list[index-1][0] == 'dt':
        #     str = token_list[index][1]
        
        # elif token_list[index-1][0] == 'id':
        #     str = token_list[index[2]]
        

        str = token_list[index][0]

        # print("str:",str,"  char:", char)

        if str == char:
            index +=1
            return True

        else:

            return False



def Program(): #function definition & will have synthesised attribute

    global scope

    glob_table[scope] = []
    
    entry = Id()
    entry.parent_scope = 'global'
    glob_table[scope].append(entry)
    # print(glob_table)

    # entry.scope = scope

    # print("here")
    if match('dt'):
        entry.return_type = token_list[index-1][1]
        # id_type = token_list[index-1][1]
        # print(dt_type)
        if match('id'):
            entry.name = token_list[index-1][2]
            if match('('):
                # print('sup2')
                entry.child_scope = {}
                scope += 1
                entry.child_scope[scope] = []

                arg_list = []

                if ParamList(arg_list, scope, entry):
                    s = ""
                    #concatenates parameter types and inserts into function type
                    for i in arg_list:
                        s = s + i.type
                    entry.type = s

                    if match(')'):
                        arg_list = []
                        scope -= 1
                        # print('broter')
                        if match('{'):
                            scope += 1
                            #this is also in functions scope
                            if Stmts(scope,entry):
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

def ParamList(arg_list, scope,entry):

    var_entry = Id()
    var_entry.parent_scope = entry.name

    if match('dt'):
        # print('alpha')
        var_entry.type = token_list[index-1][1]
        arg_list.append(var_entry)

        if match('id'):
            # print('beta')
            var_entry.name = token_list[index-1][2]
            entry.child_scope.append(var_entry)
            # glob_table[scope]
            if PList(arg_list, scope, entry):
                return True, arg_list
            else:
                return True, arg_list, 
        else:
            return False, "missing/unrecognized identifier"
    else:
        return False, "missing/incorrect datatype"

def PList(arg_list, scope, entry):


    var_entry = Id()
    var_entry.parent_scope = scope

    
    if match('?'):
        if match('dt'):
            var_entry.type = token_list[index-1][1]
            # print('hello')
            if match('id'):
                var_entry.name = token_list[index-1][2]
                # print(var_entry.name)
                # if var_entry.name == 4:
                #     print('sister')
                # print(token_list[index-1][2])
                arg_list.append(var_entry)

                if PList():
                    return True
    else:
        # print('pls')
        return False, "punctuator '?' or ')' expected but wasn't provided"

def F(scope, entry):
    # print(token_list[index])
    var_entry = Id()
    var_entry.parent_scope = scope

    if match('id'):
        var_entry.name = token_list[index-1][2]
        entry.child_scope[scope].append(var_entry)
        print(var_entry)
        return True
    
    elif match('('):
        # print('here')
        if (E(scope,entry)):
            # print('over')
            if (match(')')):
                return True
            else:
                return False, "punctuator ')' expected but wasn't provided"
        else:
            return False,"expression expected but wasn't provided"
            
    else:
        return False, "punctuator '(' or identifier expected but wasn't provided"

def T_prime(scope, entry):
    # print('hello2')
    if (match('*')):
        # print('ello3')
        if (F(scope, entry)):
            if (T_prime(scope, entry)):
                # print('nub')
                return True
        else:
            return False, "factor expected but wasn't provided"
    else:
        # print('hello')
        return True
    
def T(scope, entry):
    if (F(scope, entry)):
        if (T_prime(scope, entry)):
            return True
    else:
        return False, "factor expected but wasn't provided"

def E_prime(scope, entry):
    if (match('+')):
        if (T(scope, entry)):
            if (E_prime(scope, entry)):
                return True
    else:
        return True

def E(scope, entry):
    if (T(scope, entry)):
        if (E_prime(scope, entry)):
            return True

    else:
        return False, "term expected but wasn't provided"

def AssignStmt():
    if (match('id')):
        print('abey')
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

def DecStmts(scope, entry):

    var = Id()
    var.parent_scope = scope
    # var.par = entry.child_scope

    # print("in dec")

    if match('dt'):
        var.type = token_list[index-1][1]
        # print('here')
        
        if match('id'):
            var.name = token_list[index-1][2]
            entry.child_scope[scope].append(var)

            if OptionalAssign(scope, entry):
                # print('bhaijaan')
                return True
            else:
                if List(scope, entry):
                    return True
        else:
            return False,"missing/unrecognized identifier"
    else:
        return False, "missing/incorrect datatype"

def OptionalAssign(scope, entry):

    if (match('=')):
        if (E(scope, entry)):
            if match(';'):
                # print('mayn')
                return True
            else:
                return False
                         
    else:
        return True

def List(scope, entry):
    if match('?'):
        if match('dt'):
            if OptionalAssign(scope, entry):
                return True
            else:
                if List(scope, entry):
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

def Stmts(arg_list, scope):
    if S_prime(arg_list, scope):
        return True

def S_prime(arg_list, scope):
    if token_list[index] == '}':
        pass

    elif DecStmts(arg_list, scope):
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


def sym_table_traverse(sym_table):

    #child_scopeable is a dict
    # print(sym_table.child_scope,'oops')

    if sym_table.child_scope != None:
        
        print('lmfao')
        
        # print(sym_table.child_scope[1].ptr)
        # print(sym_table.child_scope[1].name)
        # print(sym_table.child_scope[1].type)
        # print(sym_table.child_scope[1].return_type)
        # print(sym_table.child_scope[1].parent_scope)
        # print(sym_table.child_scope[1].child_scope)
        # print(sym_table.type)
        # print(sym_table.return_type)
        # print(sym_table.parent_scope)
        # print(sym_table.child_scope)
        

    
def iterdict(d):
    for key,value in d.items():
        # print(type(value))
        # return
        for x in value:
            print(x.ptr, x.name, x.type, x.return_type, x.parent_scope, x.child_scope)
        # if isinstance(value,list):
        #     print(value[0].name)
        # print(value.ptr)
        # print (k,":",v.child_scope)
        
        
            # print(type(value.child_scope))
            if isinstance(x.child_scope, dict):
            # print('idk')
                iterdict(x.child_scope)

            else:            
                print (key,":",x.name)



def test():

    test = Program()

    # print(glob_table[scope],'bwois')
    iterdict(glob_table)
    # for i in glob_table:
        # print(glob_table[i].ptr)
        # print(glob_table[i].name)
        # print(glob_table[i].type)
        # print(glob_table[i].return_type)
        # print(glob_table[i].parent_scope)
        # print(glob_table[i].child_scope)

        # print(sym_table_traverse(glob_table[i]),'ayo')
        # print(glob_table[i].child_scope)
    # print(test)

    if test[0]:
        # print(test[1])
        print("string is accepted")
    else:
        print("string is not accepted")
        print("Error:",test[1])
        

test()