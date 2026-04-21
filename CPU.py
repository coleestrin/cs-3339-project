from Microarchitecture.instructionMemory import InstructionMemory
from Microarchitecture.dataMemory import Memory
from Microarchitecture.registerFile import RegisterFile
from Microarchitecture.ALU import ALU

MEMORY_SIZE = 1024
BASE_ADDRESS = 0x0


class CPU:
    def __init__(self, fileName=None, debug=False, program_text=None):
        self.__instructionMemory = InstructionMemory(fileName, source_text=program_text)
        self.__dataMemory = Memory(MEMORY_SIZE, BASE_ADDRESS)
        self.__registerFile = RegisterFile()
        self.__ALU = ALU()
        self.__debug = debug
        self.__PC = 0
        self.__cycles = 0
        self._last_control_signals = self.getControlSignals(None)
        self.IF_ID = {"opcode": None, "rs": 0, "rt": 0, "rd": 0, "immediate": 0, "address": 0, "shamt": 0}
        self.ID_EX = {"opcode": None, "RegWrite": 0, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 0, "MemRead": 0,
                      "PCSrc": 0, "Jump": 0, "readData1": 0, "readData2": 0, "immediate": 0, "WriteReg": 0,
                      "address": 0, "shamt": 0}
        self.EX_MEM = {"opcode": None, "RegWrite": 0, "MemWrite": 0, "MemtoReg": 0, "MemRead": 0,
                       "WriteReg": 0, "ALUResult": 0, "writeData": 0}
        self.MEM_WB = {"opcode": None, "RegWrite": 0, "MemtoReg": 0, "ReadData": 0, "ALUResult": 0, "WriteReg": 0}

    def getControlSignals(self, opCode):
        control_signals = {
            "ADD":  {"RegDst": 1, "RegWrite": 1, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 1, "MemRead": 0, "PCSrc": 0, "Jump": 0},
            "ADDI": {"RegDst": 0, "RegWrite": 1, "ALUSrc": 1, "MemWrite": 0, "MemtoReg": 1, "MemRead": 0, "PCSrc": 0, "Jump": 0},
            "MUL":  {"RegDst": 1, "RegWrite": 1, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 1, "MemRead": 0, "PCSrc": 0, "Jump": 0},
            "SUB":  {"RegDst": 1, "RegWrite": 1, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 1, "MemRead": 0, "PCSrc": 0, "Jump": 0},
            "AND":  {"RegDst": 1, "RegWrite": 1, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 1, "MemRead": 0, "PCSrc": 0, "Jump": 0},
            "OR":   {"RegDst": 1, "RegWrite": 1, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 1, "MemRead": 0, "PCSrc": 0, "Jump": 0},
            "SLL":  {"RegDst": 1, "RegWrite": 1, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 1, "MemRead": 0, "PCSrc": 0, "Jump": 0},
            "SRL":  {"RegDst": 1, "RegWrite": 1, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 1, "MemRead": 0, "PCSrc": 0, "Jump": 0},
            "LW":   {"RegDst": 0, "RegWrite": 1, "ALUSrc": 1, "MemWrite": 0, "MemtoReg": 0, "MemRead": 1, "PCSrc": 0, "Jump": 0},
            "SW":   {"RegDst": 0, "RegWrite": 0, "ALUSrc": 1, "MemWrite": 1, "MemtoReg": 0, "MemRead": 0, "PCSrc": 0, "Jump": 0},
            "BEQ":  {"RegDst": 0, "RegWrite": 0, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 0, "MemRead": 0, "PCSrc": 1, "Jump": 0},
            "J":    {"RegDst": 0, "RegWrite": 0, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 0, "MemRead": 0, "PCSrc": 0, "Jump": 1},
            "NOP":  {"RegDst": 0, "RegWrite": 0, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 0, "MemRead": 0, "PCSrc": 0, "Jump": 0},
            None:   {"RegDst": 0, "RegWrite": 0, "ALUSrc": 0, "MemWrite": 0, "MemtoReg": 0, "MemRead": 0, "PCSrc": 0, "Jump": 0},
        }
        return control_signals.get(opCode, control_signals[None]).copy()

    def _snapshot_pipeline(self):
        return {
            "IF_ID": dict(self.IF_ID),
            "ID_EX": dict(self.ID_EX),
            "EX_MEM": dict(self.EX_MEM),
            "MEM_WB": dict(self.MEM_WB),
        }

    def _snapshot_state(self, instruction_before_step):
        return {
            "cycle": self.__cycles,
            "pc": self.__PC,
            "instruction": instruction_before_step,
            "controlSignals": dict(self._last_control_signals),
            "stateRegisters": self._snapshot_pipeline(),
            "registerFile": self.__registerFile.snapshot(),
            "memory": self.__dataMemory.snapshot_words(),
        }

    def _final_report(self, debug_trace):
        return {
            "cycles": self.__cycles,
            "registers": self.__registerFile.snapshot(),
            "memory": self.__dataMemory.snapshot_words(),
            "debugTrace": debug_trace,
        }

    def run(self):
        maxPC = self.__instructionMemory.getMaxPC()
        debug_trace = []

        while self.__PC < maxPC + 16:
            current_pc = self.__PC
            self.__instructionMemory.run(self.__PC)
            instruction_before_step = self.__instructionMemory.getCurrentInstruction()

            self.IF_ID = {
                "opcode": self.__instructionMemory.getOpcode(),
                "rs": self.__instructionMemory.getRs(),
                "rt": self.__instructionMemory.getRt(),
                "rd": self.__instructionMemory.getRd(),
                "immediate": self.__instructionMemory.getImmediate(),
                "address": self.__instructionMemory.getAddress(),
                "shamt": self.__instructionMemory.getShamt(),
            }
            control_signals = self.getControlSignals(self.IF_ID["opcode"])

            self.__registerFile.run(self.IF_ID["rs"], self.IF_ID["rt"], 0, 0, 0)
            write_reg = self.IF_ID["rd"] if control_signals["RegDst"] else self.IF_ID["rt"]
            self.ID_EX = {
                "opcode": self.IF_ID["opcode"],
                "RegWrite": control_signals["RegWrite"],
                "ALUSrc": control_signals["ALUSrc"],
                "MemWrite": control_signals["MemWrite"],
                "MemtoReg": control_signals["MemtoReg"],
                "MemRead": control_signals["MemRead"],
                "PCSrc": control_signals["PCSrc"],
                "Jump": control_signals["Jump"],
                "readData1": self.__registerFile.getReadData1(),
                "readData2": self.__registerFile.getReadData2(),
                "immediate": self.IF_ID["immediate"],
                "WriteReg": write_reg,
                "address": self.IF_ID["address"],
                "shamt": self.IF_ID["shamt"],
            }

            self.__ALU.run(
                self.ID_EX["opcode"],
                self.ID_EX["readData1"],
                self.ID_EX["readData2"] if not self.ID_EX["ALUSrc"] else self.ID_EX["immediate"],
                self.ID_EX["shamt"],
            )

            self.EX_MEM = {
                "opcode": self.ID_EX["opcode"],
                "RegWrite": self.ID_EX["RegWrite"],
                "MemWrite": self.ID_EX["MemWrite"],
                "MemtoReg": self.ID_EX["MemtoReg"],
                "MemRead": self.ID_EX["MemRead"],
                "ALUResult": self.__ALU.getResult(),
                "writeData": self.ID_EX["readData2"],
                "WriteReg": self.ID_EX["WriteReg"],
            }

            self.__dataMemory.run(
                self.EX_MEM["ALUResult"],
                self.EX_MEM["writeData"],
                self.EX_MEM["MemWrite"],
                self.EX_MEM["MemRead"],
            )

            self.MEM_WB = {
                "opcode": self.EX_MEM["opcode"],
                "RegWrite": self.EX_MEM["RegWrite"],
                "MemtoReg": self.EX_MEM["MemtoReg"],
                "ReadData": self.__dataMemory.getReadData(),
                "ALUResult": self.EX_MEM["ALUResult"],
                "WriteReg": self.EX_MEM["WriteReg"],
            }

            write_back_value = self.MEM_WB["ALUResult"] if self.MEM_WB["MemtoReg"] else self.MEM_WB["ReadData"]
            self.__registerFile.run(0, 0, self.MEM_WB["WriteReg"], write_back_value, self.MEM_WB["RegWrite"])

            self._last_control_signals = control_signals
            self.__cycles += 1

            if self.ID_EX["Jump"]:
                self.__PC = self.ID_EX["address"] * 4
            elif self.ID_EX["PCSrc"] and self.__ALU.zeroFlag():
                self.__PC = current_pc + (self.ID_EX["immediate"] << 2) + 4
            else:
                self.__PC = current_pc + 4

            if self.__debug:
                debug_trace.append(self._snapshot_state(instruction_before_step))

        return self._final_report(debug_trace)
