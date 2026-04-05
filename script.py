from instruction import parse_file

#THIS SCRIPT DISPLAYS THE PARSING AND DECODING CONTENTS OF ASM TEST FILES USED FOR THIS PROJECT
#USE instruction.py FOR TESTING THIS SCRIPT AND IMPLEMENTING INTO PROJECT

def test_parser(filepath):
    print("=" * 70)
    print(f"Parsing: {filepath}")
    print("=" * 70)

    instructions = parse_file(filepath)

    print(f"\n{'IDX':<5} {'MNEM':<6} {'TYPE':<6} {'BINARY':>32}   FIELDS")
    print("=" * 70)

    for i, instr in enumerate(instructions):
        
        if instr['type'] == 'R':
            fields = (f"rd={instr.get('rd','?')} "
                      f"rs={instr.get('rs','?')} "
                      f"rt={instr.get('rt','?')} "
                      f"shamt={instr.get('shamt','?')} "
                      f"funct={instr.get('funct','?')}")
        elif instr['type'] == 'I':
            fields = (f"rs={instr.get('rs','?')} "
                      f"rt={instr.get('rt','?')} "
                      f"imm={instr.get('imm','?')}")
        else:  # J
            fields = f"addr={instr.get('address','?')}"

        print(f"{i:<5} {instr['mnemonic']:<6} {instr['type']:<6} "
              f"{instr['binary']:>32}   {fields}")

    print(f"\nTotal instructions parsed: {len(instructions)}")

if __name__ == "__main__":
    test_parser("testfile.asm")# NAME WHICHEVER ASM FILE IS BEING TESTED HERE