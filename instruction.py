REGISTERS = {
    '$zero': 0, '$at': 1,
    '$v0': 2,  '$v1': 3,
    '$a0': 4,  '$a1': 5,  '$a2': 6,  '$a3': 7,
    '$t0': 8,  '$t1': 9,  '$t2': 10, '$t3': 11,
    '$t4': 12, '$t5': 13, '$t6': 14, '$t7': 15,
    '$s0': 16, '$s1': 17, '$s2': 18, '$s3': 19,
    '$s4': 20, '$s5': 21, '$s6': 22, '$s7': 23,
    '$t8': 24, '$t9': 25,
    '$k0': 26, '$k1': 27,
    '$gp': 28, '$sp': 29, '$fp': 30, '$ra': 31,
}

INSTRUCTION_TABLE = {
    'ADD':  {'type': 'R', 'opcode': 0,  'funct': 32},
    'SUB':  {'type': 'R', 'opcode': 0,  'funct': 34},
    'MUL':  {'type': 'R', 'opcode': 28, 'funct': 2},
    'AND':  {'type': 'R', 'opcode': 0,  'funct': 36},
    'OR':   {'type': 'R', 'opcode': 0,  'funct': 37},
    'SLL':  {'type': 'R', 'opcode': 0,  'funct': 0},
    'SRL':  {'type': 'R', 'opcode': 0,  'funct': 2},
    'ADDI': {'type': 'I', 'opcode': 8},
    'LW':   {'type': 'I', 'opcode': 35},
    'SW':   {'type': 'I', 'opcode': 43},
    'BEQ':  {'type': 'I', 'opcode': 4},
    'J':    {'type': 'J', 'opcode': 2},
    'NOP':  {'type': 'R', 'opcode': 0,  'funct': 0},  # ALL ZERO
}


def _clean_source_lines(source_text):
    lines = []
    labels = {}

    for raw_line in source_text.splitlines():
        line = raw_line.split('#')[0].strip()
        if not line:
            continue

        if ':' in line:
            label, _, rest = line.partition(':')
            labels[label.strip()] = len(lines)
            line = rest.strip()
            if not line:
                continue

        lines.append(line)

    return lines, labels


#PARSER
def read_file(filepath):
    with open(filepath, 'r') as f:
        return _clean_source_lines(f.read())


#DECODER
def decode(line, labels, current_index=0):
    parts = line.replace(',', ' ').split()
    name = parts[0].upper()
    info = INSTRUCTION_TABLE[name]

    instr = {
        'name': name,
        'type': info['type'],
        'opcode': info['opcode'],
    }

    if mnemonic == 'NOP':
        instr.update({'rs': 0, 'rt': 0, 'rd': 0, 'shamt': 0, 'funct': 0})

    elif info['type'] == 'R':
        if name in ('SLL', 'SRL'):
            # SLL $rd, $rt, shamt
            instr['rd']    = REGISTERS[parts[1]]
            instr['rt']    = REGISTERS[parts[2]]
            instr['rs']    = 0
            instr['shamt'] = int(parts[3])
            instr['funct'] = info['funct']
        else:
            # ADD $rd, $rs, $rt
            instr['rd']    = REGISTERS[parts[1]]
            instr['rs']    = REGISTERS[parts[2]]
            instr['rt']    = REGISTERS[parts[3]]
            instr['shamt'] = 0
            instr['funct'] = info['funct']

    elif info['type'] == 'I':
        if name in ('LW', 'SW'):
            # LW $rt, offset($rs)
            instr['rt']  = REGISTERS[parts[1]]
            offset_reg   = parts[2]
            offset, reg  = offset_reg.rstrip(')').split('(')
            instr['rs']  = REGISTERS[reg]
            instr['imm'] = int(offset)
        elif name == 'BEQ':
            # BEQ $rs, $rt, label
            instr['rs']  = REGISTERS[parts[1]]
            instr['rt']  = REGISTERS[parts[2]]
            instr['imm'] = labels[parts[3]] - (current_index + 1)
        else:
            # ADDI $rt, $rs, imm
            instr['rt']  = REGISTERS[parts[1]]
            instr['rs']  = REGISTERS[parts[2]]
            instr['imm'] = int(parts[3])

    elif info['type'] == 'J':
        instr['address'] = labels[parts[1]]

    return instr

#BINARY REPRESENTATION
def to_binary(instr):
    if instr['type'] == 'R':
        bits = (instr['opcode'] << 26 | instr['rs'] << 21 |
                instr['rt'] << 16 | instr['rd'] << 11 |
                instr['shamt'] << 6 | instr['funct'])
    elif instr['type'] == 'I':
        imm = instr['imm'] & 0xFFFF  # HANDLES NEGATIVES
        bits = (instr['opcode'] << 26 | instr['rs'] << 21 |
                instr['rt'] << 16 | imm)
    else:  # J-type
        bits = (instr['opcode'] << 26 | instr['address'])

    return f"{bits:032b}"  # RETURNS 32-BIT BINARY


#PUTTING IT ALL TOGETHER
def parse_lines(lines, labels, emit_listing=False):
    instructions = []

    for i, line in enumerate(lines):
        instr = decode(line, labels, current_index=i)
        instr['binary'] = to_binary(instr)
        instructions.append(instr)

    if emit_listing:
        for i, instr in enumerate(instructions):
            print(f"{i:3}: {instr['binary']}  ({instr['name']})")

    return instructions


def parse_file(filepath, emit_listing=False):
    lines, labels = read_file(filepath)
    return parse_lines(lines, labels, emit_listing=emit_listing)

    
def parse_source(source_text, emit_listing=False):
    lines, labels = _clean_source_lines(source_text)
    return parse_lines(lines, labels, emit_listing=emit_listing)
