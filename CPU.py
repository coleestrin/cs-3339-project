class CPU:
    
    def __init__(self, fileName, debug=False):
        self.__instructionMemory = __instructionMemory(fileName)
        self.__dataMemory = dataMemory()
        self.__registerFile = registerFile()
        self.__ALU = ALU()
        self.__debug = debug

        def getControlSignals(self, opCode):
            control_signals = {
                "ADD"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "Branch" : 0, "Jump" : 0},
                "ADDI" : {"RegDst": 0, "RegWrite" : 1, "ALUSrc" : 1, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "Branch" : 0, "Jump" : 0},
                "MUL"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "Branch" : 0, "Jump" : 0},
                "SUB"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "Branch" : 0, "Jump" : 0},
                "AND"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "Branch" : 0, "Jump" : 0},
                "OR"   : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "Branch" : 0, "Jump" : 0},
                "SLL"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "Branch" : 0, "Jump" : 0},
                "SRL"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "Branch" : 0, "Jump" : 0},
                "LW"   : {"RegDst": 0, "RegWrite" : 1, "ALUSrc" : 1, "MemWrite" : 0, "MemtoReg" : 0, "MemRead" : 1, "Branch" : 0, "Jump" : 0},
                "SW"   : {"RegDst": 0, "RegWrite" : 0, "ALUSrc" : 1, "MemWrite" : 1, "MemtoReg" : 0, "MemRead" : 0, "Branch" : 0, "Jump" : 0},
                "BEQ"  : {"RegDst": 0, "RegWrite" : 0, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 0, "MemRead" : 0, "Branch" : 1, "Jump" : 0},
                "J"    : {"RegDst": 0, "RegWrite" : 0, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 0, "MemRead" : 0, "Branch" : 0, "Jump" : 1}, 
                "NOP"  : {"RegDst": 0, "RegWrite" : 0, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 0, "MemRead" : 0, "Branch" : 0, "Jump" : 0},
            }
            return control_signals.get(opCode)