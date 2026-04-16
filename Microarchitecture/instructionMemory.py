from instruction import parse_file

class InstructionMemory:
    def __init__(self, filepath):
        self.instructions = parse_file(filepath)
        self.current_instruction = None
        self.maxPC = len(self.instructions) * 4 

    def getMaxPC(self):
        return self.maxPC

    def run(self, addr):
        index = addr//4
        if addr < self.maxPC:
            self.current_instruction = self.instructions[index]
        else:
            self.current_instruction = None  # Out of bounds
        
    def getCurrentInstruction(self):
        return self.current_instruction
    
    def getOpcode(self):
        return self.current_instruction["mnemonic"] if "mnemonic" in self.current_instruction else "ERROR"
    
    def getRs(self):
        return self.current_instruction["rs"] if "rs" in self.current_instruction else 0
    
    def getRt(self):
        return self.current_instruction["rt"] if "rt" in self.current_instruction else 0
    
    def getRd(self):
        return self.current_instruction["rd"] if "rd" in self.current_instruction else 0
    
    def getImmediate(self):
        return self.current_instruction["imm"] if "imm" in self.current_instruction else 0
    
    def getAddress(self):
        return self.current_instruction["address"] if "address" in self.current_instruction else 0
    
    