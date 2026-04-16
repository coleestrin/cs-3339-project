import numpy as np
MASK32 = 0xFFFFFFFF

REG_NAMES = (
    "zero", "at", "v0", "v1", "a0", "a1", "a2", "a3",
    "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7",
    "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
    "t8", "t9", "k0", "k1", "gp", "sp", "fp", "ra",
)

class RegisterFile:
    _reg_array = np.zeros(32, dtype=np.int32)
    
    def reset(self):
        for i in self._reg_array:
            self._reg_array[i] = 0

    def read(self, i):
        if i > 32:
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

