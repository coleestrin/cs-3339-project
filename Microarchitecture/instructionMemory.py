from instruction import parse_file, parse_source

class InstructionMemory:
    def __init__(self, filepath=None, source_text=None):
        if source_text is not None:
            self.instructions = parse_source(source_text)
        elif filepath is not None:
            self.instructions = parse_file(filepath)
        else:
            raise ValueError("Instruction memory requires a filepath or source_text")
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
        return self.current_instruction["name"] if self.current_instruction and "mnemonic" in self.current_instruction else None
    
    def getRs(self):
        return self.current_instruction["rs"] if self.current_instruction and "rs" in self.current_instruction else 0
    
    def getRt(self):
        return self.current_instruction["rt"] if self.current_instruction and "rt" in self.current_instruction else 0
    
    def getRd(self):
        return self.current_instruction["rd"] if self.current_instruction and "rd" in self.current_instruction else 0
    
    def getImmediate(self):
        return self.current_instruction["imm"] if self.current_instruction and "imm" in self.current_instruction else 0
    
    def getAddress(self):
        return self.current_instruction["address"] if self.current_instruction and "address" in self.current_instruction else 0
    
    def getShamt(self):
        return self.current_instruction["shamt"] if self.current_instruction and "shamt" in self.current_instruction else 0
    
    
