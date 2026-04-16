class AddressError(Exception):
    pass

class AlignmentError(Exception):
    pass

class Memory:
    def __init__(self, size, base_addr):
        self.size = size
        self.base_addr = base_addr
        self.byte_arr = bytearray(size)
    
    def __repr__(self):
        return f"Memory(byte_arr = {self.byte_arr}, size = {self.size}, base_addr = {self.base_addr})"
    
    def check_valid_address(self, addr):
        if addr > (self.base_addr + self.size) or addr < self.base_addr: 
            raise AddressError(f"Invalid memory address: 0x{addr:08X}")
    
    def check_address_alignment(self, addr, size):
        if (size == 2 and addr % 2 != 0):
            raise AlignmentError(f"Halfword misaligned address: 0x{addr:08X}")
        if (size == 4 and addr % 4 != 0):
            raise AlignmentError(f"Word misaligned address: 0x{addr:08X}")
    
    def read8(self, addr):
        self.check_valid_address(addr)
        return self.byte_arr[addr]
    
    def write8(self, addr, value):
        self.check_valid_address(addr)
        self.check_valid_address(addr + 3)

        self.byte_arr[addr] = value & 0xFF #puts only lowest 8 bits
    
    def read32(self, addr):
        self.check_valid_address(addr)
        self.check_valid_address(addr + 3)
        self.check_address_alignment(addr, 4)

        b0 = self.byte_arr[addr]
        b1 = self.byte_arr[addr+1] << 8 #sll 8 for printing
        b2 = self.byte_arr[addr+2] << 16
        b3 = self.byte_arr[addr+3] << 24

        #this prints LITTLE ENDIAN
        return b0 | b1 | b2| b3
    
    def write32(self, addr, value):
        self.check_valid_address(addr)
        self.check_valid_address(addr+3)
        self.check_address_alignment(addr, 4)

        #this writes LITTLE ENDIAN
        self.byte_arr[addr] = value & 0xFF
        self.byte_arr[addr+1] =  (value >> 8) & 0xFF #srl 8 for writing next 8 to mem
        self.byte_arr[addr+2] =  (value >> 16) & 0xFF
        self.byte_arr[addr+3] =  (value >> 24) & 0xFF

    def run(self, addr, writeData, MemWrite, MemRead):
        if MemWrite:
            self.write32(addr, writeData)
        elif MemRead:
            self.readData = self.read32(addr)
    
    def getReadData(self):
        return self.readData
