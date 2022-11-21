from Env import *
from sym_table import *


#semantic actions for the parser
class SemanticAction:
    def __init__(self):
        self.env = Env()
    
    def put(self, id):
        self.env.put(id)

    def get(self, id):
        self.env.get(id)

    def print(self, id):
        self.env.print(id)

    def delete(self, id):
        self.env.delete(id)

    def assign(self, id):
        self.env.assign(id)

    def printAll(self):
        self.env.printAll()

    def check(self, id):
        self.env.check(id)
    
    def declaration(self, id):
        if False == self.env.check(id):
            self.env.put(id)
        else:
            print ("ERROR: variable already declared")
    def checkType(self, id):
        if False == self.env.check(id):
            print ("ERROR: variable not declared")
        else:
            self.env.get(id)
            

    