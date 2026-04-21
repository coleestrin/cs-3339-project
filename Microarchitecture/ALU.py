class ALU:

    def __init__(self):
        self.zero = True
        self.result = 0

    def run(self, opcode, operand1, operand2, shamt):

        match opcode:
            case "ADD" | "ADDI" | "LW" | "SW":
                self.result = operand1 + operand2
            case "SUB" | "BEQ":
                self.result = operand1 - operand2
            case "MUL":
                self.result = operand1 * operand2
            case "AND":
                self.result = operand1 & operand2
            case "OR":
                self.result = operand1 | operand2
            case "SLL":
                self.result = operand2 << shamt
            case "SRL":
                self.result = operand2 >> shamt
        
        self.zero = (self.result == 0)

    def getResult(self):
        return self.result
    
    def zeroFlag(self):
        return self.zero
