
# attr_list = ["ptr", "name" , "type", "return_type", "value", "scope", \
#             "prev", "next"]      

# for i in attr_list:
#     SymbolTable[i] = {}

# for i in SymbolTable.keys():
#     print(i)


#nested scope aren't universally nested. They are like a path in a tree with only one child per parent.
#scope must be incremented on every '{' and decremented on every '}'
#scope must be incremented on every function definition and decremented on every function end


class Id:
    
    ptr = None
    name = None
    type = None
    return_type = None
    parent_scope = None
    child_scope = None
    

