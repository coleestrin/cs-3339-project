MASK32 = 0xFFFFFFFF

REG_NAMES = (
    "zero", "at", "v0", "v1", "a0", "a1", "a2", "a3",
    "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
    "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
    "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra",
)


def _to_signed32(value):
    value &= MASK32
    if value & 0x80000000:
        return value - (1 << 32)
    return value


class RegisterFile:
    def __init__(self):
        self._reg_array = [0] * 32
        self.readData1 = 0
        self.readData2 = 0

    def reset(self):
        self._reg_array = [0] * 32
        self.readData1 = 0
        self.readData2 = 0

    def read(self, index):
        if index < 0 or index >= 32:
            raise ValueError(f"Register {index} is not a valid register")
        if index == 0:
            return 0
        return self._reg_array[index]

    def write(self, index, value):
        if index < 0 or index >= 32:
            raise ValueError(f"Register {index} is not a valid register")
        if index == 0:
            return
        self._reg_array[index] = _to_signed32(value)

    def dump(self):
        for index, name in enumerate(REG_NAMES):
            print(f"${name} ({index:02d}) = 0x{self.read(index) & MASK32:08X}")

    def run(self, readReg1, readReg2, writeReg, writeData, RegWrite):
        self.readData1 = self.read(readReg1)
        self.readData2 = self.read(readReg2)

        if RegWrite:
            self.write(writeReg, writeData)

    def getReadData1(self):
        return self.readData1

    def getReadData2(self):
        return self.readData2

    def snapshot(self):
        registers = []
        for index, name in enumerate(REG_NAMES):
            value = self.read(index)
            registers.append({
                "index": index,
                "name": f"${name}",
                "decimal": value,
                "hex": f"0x{value & MASK32:08X}",
                "nonZero": value != 0,
            })
        return registers
