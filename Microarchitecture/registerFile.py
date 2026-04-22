MASK32 = 0xFFFFFFFF

REG_NAMES = (
    "zero", "at", "v0", "v1", "a0", "a1", "a2", "a3",
    "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
    "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
    "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra",
)

class RegisterFile:
    def __init__(self):
        self._reg_array = [0] * 32
        self.readData1 = 0
        self.readData2 = 0
    
    def reset(self):
        self._reg_array = [0] * 32
        self.readData1 = 0
        self.readData2 = 0

    def read(self, i):
        if i < 0 or i >= 32:
            raise ValueError(f"Register {i} is not a valid register")
        if i == 0:
            return 0        
        return self._reg_array[i]

    def write(self, i, value):
        if i == 0:
            return 
        self._reg_array[i] = value & MASK32 #manually limiting to 32 bits
    
    def dump(self):
        for i in range(32):
            print(f"${REG_NAMES[i]} ({i:02d}) = 0x{self.read(i):08X}")

    def snapshot(self):
        registers = []
        for i in range(32):
            value = self.read(i)
            registers.append({
                "index": i,
                "name": REG_NAMES[i],
                "decimal": value,
                "hex": f"0x{value & MASK32:08X}",
            })
        return registers

    def run(self, readReg1, readReg2, writeReg, writeData, RegWrite):
        if RegWrite:
            self.write(writeReg, writeData)
            return
        
        self.readData1 = self.read(readReg1)
        self.readData2 = self.read(readReg2)

    def getReadData1(self):
        return self.readData1
    
    def getReadData2(self):
        return self.readData2
