class CPU:
    
    def __init__(self, fileName, debug=False):
        self.__instructionMemory = __instructionMemory(fileName)
        self.__dataMemory = dataMemory()
        self.__registerFile = registerFile()
        self.__ALU = ALU()
        self.__debug = debug