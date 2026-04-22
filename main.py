import argparse
import sys
from CPU import CPU


def print_report(report):
    print(f"Cycles: {report['cycles']}")
    print("Registers:")
    for register in report["registers"]:
        print(f"  {register['name']:>5} = {register['decimal']} ({register['hex']})")


def main():
    parser = argparse.ArgumentParser(description="MIPS pipelined processor simulator")
    parser.add_argument("file", help="Path to the MIPS assembly (.asm) file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    try:
        cpu = CPU(args.file, args.debug)
        report = cpu.run()
    except FileNotFoundError:
        print(f"Error: could not find assembly file '{args.file}'.", file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print_report(report)


if __name__ == "__main__":
    main()
