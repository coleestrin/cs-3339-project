import argparse
from CPU import CPU


def main():
    parser = argparse.ArgumentParser(description="MIPS pipelined processor simulator")
    parser.add_argument("file", help="Path to the MIPS assembly (.asm) file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    cpu = CPU(args.file, args.debug)
    result = cpu.run()
    print_report(result)
    

def print_report(report):
    print(f"Program execution completed after {report['cycles']} cycles.")
    print_register_file(report['registers'])
    print_memory(report['memory'])
def print_register_file(registers):
    for i in range(8):
        output = ""
        for j in range(4):
            part = f"${registers[i + j*8]['name']:4} ({registers[i + j*8]['index']:02d}) = {registers[i + j*8]['hex']} ({registers[i + j*8]['decimal']})"
            part = part.ljust(30)
            output += part
        print(output)

def print_memory(data_memory):
    print("\nData Memory (non-zero values):")
    for word in data_memory:
        if word['decimal'] != 0:
            print(f"Address: {word['hexAddress']} = {word['hex']} ({word['decimal']})")
    

if __name__ == "__main__":
    main()
