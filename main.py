import argparse
from CPU import CPU


def main():
    parser = argparse.ArgumentParser(description="MIPS pipelined processor simulator")
    parser.add_argument("file", help="Path to the MIPS assembly (.asm) file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    cpu = CPU(args.file, args.debug)
    cpu.run()


if __name__ == "__main__":
    main()
