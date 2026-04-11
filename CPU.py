from Microarchitecture import *

class CPU:
    
    def __init__(self, fileName, debug=False):
        self.__instructionMemory = instructionMemory(fileName)
        self.__dataMemory = dataMemory()
        self.__registerFile = registerFile()
        self.__ALU = ALU()
        self.__debug = debug
        self.__PC = 0
        self.__cycles = 0
        self.IF_ID =  {"opcode": "", "rs": 0, "rt": 0, "rd": 0, "immediate": 0, "address": 0}
        self.ID_EX =  {"opcode": "", "RegWrite" : 0, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 0, "MemRead" : 0,
                        "PCSrc" : 0, "Jump" : 0, "readData1": 0, "readData2": 0, "immediate": 0, "WriteReg": 0, "address": 0}
        self.EX_MEM = {"opcode": "", "RegWrite" : 0, "MemWrite" : 0, "MemtoReg" : 0, "MemRead" : 0, "ALUResult": 0, "writeData": 0}
        self.MEM_WB = {"opcode": "", "RegWrite" : 0, "MemtoReg" : 0, "ReadData": 0, "ALUResult": 0, "WriteReg" : 0}

    def getControlSignals(self, opCode):
        """
        Returns a dictionary of control signals for a given opcode.
        
        :param self: 
        :param opCode: String of the keyword of the instruction
        """
        control_signals = {
            "ADD"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "PCSrc" : 0, "Jump" : 0},
            "ADDI" : {"RegDst": 0, "RegWrite" : 1, "ALUSrc" : 1, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "PCSrc" : 0, "Jump" : 0},
            "MUL"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "PCSrc" : 0, "Jump" : 0},
            "SUB"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "PCSrc" : 0, "Jump" : 0},
            "AND"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "PCSrc" : 0, "Jump" : 0},
            "OR"   : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "PCSrc" : 0, "Jump" : 0},
            "SLL"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "PCSrc" : 0, "Jump" : 0},
            "SRL"  : {"RegDst": 1, "RegWrite" : 1, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 1, "MemRead" : 0, "PCSrc" : 0, "Jump" : 0},
            "LW"   : {"RegDst": 0, "RegWrite" : 1, "ALUSrc" : 1, "MemWrite" : 0, "MemtoReg" : 0, "MemRead" : 1, "PCSrc" : 0, "Jump" : 0},
            "SW"   : {"RegDst": 0, "RegWrite" : 0, "ALUSrc" : 1, "MemWrite" : 1, "MemtoReg" : 0, "MemRead" : 0, "PCSrc" : 0, "Jump" : 0},
            "BEQ"  : {"RegDst": 0, "RegWrite" : 0, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 0, "MemRead" : 0, "PCSrc" : 1, "Jump" : 0},
            "J"    : {"RegDst": 0, "RegWrite" : 0, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 0, "MemRead" : 0, "PCSrc" : 0, "Jump" : 1}, 
            "NOP"  : {"RegDst": 0, "RegWrite" : 0, "ALUSrc" : 0, "MemWrite" : 0, "MemtoReg" : 0, "MemRead" : 0, "PCSrc" : 0, "Jump" : 0},
        }
        return control_signals.get(opCode)
    
    def run(self):
        """
        Main execution loop of the CPU.
        
        :param self: 
        """

        maxPC = self.__instructionMemory.getInstructionCount() * 4  
        ControlSignals = {}

        while self.__PC < maxPC:

            ControlSignals = self.getControlSignals(self.IF_ID["opcode"])

            # run the first four stages of the pipeline
            self.__instructionMemory.run(self.__PC)

            self.__registerFile.run(self.IF_ID["rs"], self.IF_ID["rt"], 0, 0, 0)
            
            self.__ALU.run(self.ID_EX["opcode"], self.ID_EX["readData1"],
                            self.ID_EX["readData2"] if not ControlSignals["ALUSrc"] else self.ID_EX["immediate"])
            
            self.__dataMemory.run(self.EX_MEM["ALUResult"], self.EX_MEM["writeData"], ControlSignals["MemWrite"], ControlSignals["MemRead"])

            # update the program counter
            if self.ID_EX["jump"]:
                self.__PC = self.ID_EX["address"]
            elif self.ID_EX["PCSrc"] and self.__ALU.zero():
                self.__PC += (self.ID_EX["immediate"] << 2) + 4
            else:
                self.__PC += 4

            # update state registers
            self.IF_ID = {"opcode": self.__instructionMemory.getOpcode(),
                           "rs": self.__instructionMemory.getRs(),
                           "rt": self.__instructionMemory.getRt(),
                           "rd": self.__instructionMemory.getRd(),
                           "immediate": self.__instructionMemory.getImmediate(),
                           "address": self.__instructionMemory.getAddress()}
            
            self.ID_EX = {"opcode": self.IF_ID["opcode"], 
                          "RegWrite" : ControlSignals["RegWrite"], 
                          "ALUSrc" : ControlSignals["ALUSrc"], 
                          "MemWrite" : ControlSignals["MemWrite"], 
                          "MemtoReg" : ControlSignals["MemtoReg"], 
                          "MemRead" : ControlSignals["MemRead"],
                          "PCSrc" : ControlSignals["PCSrc"],
                          "Jump" : ControlSignals["Jump"], 
                          "readData1": self.__registerFile.getReadData1(), 
                          "readData2": self.__registerFile.getReadData2(), 
                          "immediate": self.IF_ID["immediate"], 
                          "WriteReg": self.IF_ID["rd"] if ControlSignals["RegDst"] else self.IF_ID["rt"], 
                          "address": self.IF_ID["address"]}
            
            self.EX_MEM = {"opcode": self.ID_EX["opcode"], 
                           "RegWrite" : self.ID_EX["RegWrite"], 
                           "MemWrite" : self.ID_EX["MemWrite"], 
                           "MemtoReg" : self.ID_EX["MemtoReg"], 
                           "MemRead" : self.ID_EX["MemRead"], 
                           "ALUResult": self.__ALU.getResult(), 
                           "writeData": self.ID_EX["readData2"]}
            
            self.MEM_WB = {"opcode": self.EX_MEM["opcode"], 
                           "RegWrite" : self.EX_MEM["RegWrite"], 
                           "MemtoReg" : self.EX_MEM["MemtoReg"], 
                           "ReadData": self.__dataMemory.getReadData(), 
                           "ALUResult": self.EX_MEM["ALUResult"], 
                           "WriteReg" : self.EX_MEM["WriteReg"]}
            

            # Write back to register file
            self.__registerFile.run(0, 0, self.MEM_WB["WriteReg"], 
                                    self.MEM_WB["ReadData"] if self.MEM_WB["MemtoReg"] else self.MEM_WB["ALUResult"], 
                                    self.MEM_WB["RegWrite"])
            
            self.__cycles += 1
