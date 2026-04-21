# MIPS Pipeline Simulator

CS3339 course project for simulating a 5 stage pipelined MIPS processor.

## Requirements

- Python 3
- NumPy

Install NumPy with:

```bash
pip install numpy
```

There is no separate build step.

## Run

Run the simulator with:

```bash
python3 main.py <file.asm>
```

Example:

```bash
python3 main.py testfile.asm
```

## Command Line Arguments

- `file`: required path to the input MIPS assembly file
- `-d`, `--debug`: optional debug flag

## Input

The input must be a valid MIPS assembly file using only the instructions supported by this project.

Sample input files included in this repo:

- `testfile.asm`
- `basicMips.asm`

## Supported Instructions

`ADD`, `ADDI`, `SUB`, `MUL`, `AND`, `OR`, `SLL`, `SRL`, `LW`, `SW`, `BEQ`, `J`, `NOP`

## Main Files

- `main.py` starts the simulator
- `CPU.py` contains the pipeline logic and state registers
- `instruction.py` parses assembly and generates binary output
- `script.py` is a small parser test script
- `Microarchitecture/` contains the ALU, register file, instruction memory, and data memory

## Output

After execution, the simulator prints the final register state. The project code also includes the pipeline state registers used by the simulator.
