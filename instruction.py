REGISTERS = {
    "$zero": 0, "$at": 1,
    "$v0": 2, "$v1": 3,
    "$a0": 4, "$a1": 5, "$a2": 6, "$a3": 7,
    "$t0": 8, "$t1": 9, "$t2": 10, "$t3": 11,
    "$t4": 12, "$t5": 13, "$t6": 14, "$t7": 15,
    "$s0": 16, "$s1": 17, "$s2": 18, "$s3": 19,
    "$s4": 20, "$s5": 21, "$s6": 22, "$s7": 23,
    "$t8": 24, "$t9": 25,
    "$k0": 26, "$k1": 27,
    "$gp": 28, "$sp": 29, "$fp": 30, "$ra": 31,
}

INSTRUCTION_TABLE = {
    "ADD": {"type": "R", "opcode": 0, "funct": 32},
    "SUB": {"type": "R", "opcode": 0, "funct": 34},
    "MUL": {"type": "R", "opcode": 28, "funct": 2},
    "AND": {"type": "R", "opcode": 0, "funct": 36},
    "OR": {"type": "R", "opcode": 0, "funct": 37},
    "SLL": {"type": "R", "opcode": 0, "funct": 0},
    "SRL": {"type": "R", "opcode": 0, "funct": 2},
    "ADDI": {"type": "I", "opcode": 8},
    "LW": {"type": "I", "opcode": 35},
    "SW": {"type": "I", "opcode": 43},
    "BEQ": {"type": "I", "opcode": 4},
    "J": {"type": "J", "opcode": 2},
    "NOP": {"type": "R", "opcode": 0, "funct": 0},
}


def _normalize_line(line):
    return line.split("#", 1)[0].strip()


def _read_lines(lines):
    cleaned_lines = []
    labels = {}

    for raw_line in lines:
        line = _normalize_line(raw_line)
        if not line:
            continue

        while ":" in line:
            label, _, rest = line.partition(":")
            labels[label.strip()] = len(cleaned_lines)
            line = rest.strip()
            if not line:
                break

        if line:
            cleaned_lines.append(line)

    return cleaned_lines, labels


def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file_obj:
        return _read_lines(file_obj)


def read_source(source_text):
    return _read_lines(source_text.splitlines())


def _register(register_name):
    try:
        return REGISTERS[register_name.lower()]
    except KeyError as exc:
        raise ValueError(f"Unknown register: {register_name}") from exc


def decode(line, labels, index):
    parts = line.replace(",", " ").split()
    mnemonic = parts[0].upper()

    if mnemonic not in INSTRUCTION_TABLE:
        raise ValueError(f"Unsupported instruction: {mnemonic}")

    info = INSTRUCTION_TABLE[mnemonic]
    instr = {
        "mnemonic": mnemonic,
        "type": info["type"],
        "opcode": info["opcode"],
    }

    if mnemonic == "NOP":
        instr.update({"rs": 0, "rt": 0, "rd": 0, "shamt": 0, "funct": 0})
    elif info["type"] == "R":
        if mnemonic in ("SLL", "SRL"):
            instr["rd"] = _register(parts[1])
            instr["rt"] = _register(parts[2])
            instr["rs"] = 0
            instr["shamt"] = int(parts[3], 0)
            instr["funct"] = info["funct"]
        else:
            instr["rd"] = _register(parts[1])
            instr["rs"] = _register(parts[2])
            instr["rt"] = _register(parts[3])
            instr["shamt"] = 0
            instr["funct"] = info["funct"]
    elif info["type"] == "I":
        if mnemonic in ("LW", "SW"):
            instr["rt"] = _register(parts[1])
            offset, register_name = parts[2].rstrip(")").split("(")
            instr["rs"] = _register(register_name)
            instr["imm"] = int(offset, 0)
        elif mnemonic == "BEQ":
            if parts[3] not in labels:
                raise ValueError(f"Unknown label: {parts[3]}")
            instr["rs"] = _register(parts[1])
            instr["rt"] = _register(parts[2])
            instr["imm"] = labels[parts[3]] - (index + 1)
        else:
            instr["rt"] = _register(parts[1])
            instr["rs"] = _register(parts[2])
            instr["imm"] = int(parts[3], 0)
    else:
        if parts[1] not in labels:
            raise ValueError(f"Unknown label: {parts[1]}")
        instr["address"] = labels[parts[1]]

    return instr


def to_binary(instr):
    if instr["type"] == "R":
        bits = (
            (instr["opcode"] << 26)
            | (instr["rs"] << 21)
            | (instr["rt"] << 16)
            | (instr["rd"] << 11)
            | (instr["shamt"] << 6)
            | instr["funct"]
        )
    elif instr["type"] == "I":
        imm = instr["imm"] & 0xFFFF
        bits = (
            (instr["opcode"] << 26)
            | (instr["rs"] << 21)
            | (instr["rt"] << 16)
            | imm
        )
    else:
        bits = (instr["opcode"] << 26) | instr["address"]

    return f"{bits:032b}"


def _parse_lines(lines, labels):
    instructions = []

    for index, line in enumerate(lines):
        instr = decode(line, labels, index)
        instr["binary"] = to_binary(instr)
        instructions.append(instr)

    return instructions


def parse_file(filepath):
    lines, labels = read_file(filepath)
    return _parse_lines(lines, labels)


def parse_source(source_text):
    lines, labels = read_source(source_text)
    return _parse_lines(lines, labels)
