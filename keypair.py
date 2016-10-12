#-*-coding:utf8;-*-
#qpy:2
#qpy:console

class Parser:
    def __init__(self,f): #f is the file
        self.f = f
        self.collected = {} #2d dict
    def parse(self,type_result=str):
        last_bracket = None
        for index, line in enumerate(self.f):
            line = line.strip() # removing the \n
            if line[0] == "[": # line is start of bracket     
                interior = line[1:len(line)-1]
                self.collected[interior] = {}
                last_bracket = interior
            else:
                if last_bracket == None:
                    raise SyntaxError("No open brackets to store line " + str(index+1))
                pair = line.split("=")
                if len(pair) != 2:
                    raise SyntaxError("Incorrect metadata syntax at line " + str(index+1) + ": '" + line + "'; Expected 2 values, got " + str(len(pair)))
                self.collected[last_bracket][pair[0]] = type_result(pair[1])
        return self.collected
    def get_bracket_dict(self,bracket):
        return self.collected.get(bracket,{})