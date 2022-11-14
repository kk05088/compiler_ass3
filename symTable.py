
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

    # def __init__(self, ptr, name, type, return_type, in_scope, value=None, prev=None, next=None):

    #     self.ptr = ptr
    #     self.name = name
    #     self.type = type
    #     self.return_type = return_type 
    #     self.value = value
    #     self.in_scope = in_scope
    #     self.prev = prev    #ptr to show which scope it was made in
    #     self.next = next    #ptr to a new scope if this creates one (in the case of a new function declaration)
    
    ptr = None
    name = None
    type = None
    return_type = None
    in_scope = None
    prev = None
    sym_t = None
    


    
# int a = 4;
# int sum(int y, int x):   
# char* sum(int y, int x):
#     pass
# sum(4, 5)

