class ALU:

    def __init__(self):
        self.zero = True
        self.result = 0

    def run(self, opcode, operand1, operand2):
        if opcode == "ADD" or opcode == "ADDI" or opcode == "LW" or opcode == "SW":
            self.result = operand1 + operand2
        elif opcode == "SUB" or opcode == "BEQ":
            self.result = operand1 - operand2
        elif opcode == "MUL":
            self.result = operand1 * operand2
        elif opcode == "AND":
            self.result = operand1 & operand2
        elif opcode == "OR":
            self.result = operand1 | operand2
        elif opcode == "SLL":
            self.result = operand1 << operand2
        elif opcode == "SRL":
            self.result = operand1 >> operand2
        
        self.zero = (self.result == 0)

    def getResult(self):
        return self.result
    
    def zero(self):
        return self.zero
