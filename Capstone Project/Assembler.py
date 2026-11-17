import sys
import os

# Roll No: 2501010072 -> K = 72 (K mod 3 == 0: Export symbols.txt)
COMP_TABLE = {
    "0":   "0101010", "1":   "0111111", "-1":  "0111010",
    "D":   "0001100", "A":   "0110000", "!D":  "0001101",
    "!A":  "0110001", "-D":  "0001111", "-A":  "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M":   "1110000", "!M":  "1110001", "-M":  "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101"
}

DEST_TABLE = {
    "":   "000", "M":  "001", "D":  "010", "MD":  "011",
    "A":  "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_TABLE = {
    "":    "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def get_predefined_symbols():
    symbols = {f"R{i}": i for i in range(16)}
    symbols.update({
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    })
    return symbols

def assemble(input_path):
    symbols = get_predefined_symbols()
    user_symbols = {}  # Stores labels and variables for symbols.txt

    with open(input_path, "r") as f:
        raw_lines = f.readlines()

    # Pass 1: Remove comments/blank lines and record (LABELS)
    instructions = []
    rom_address = 0

    for line in raw_lines:
        clean = line.split("//")[0].strip()
        if not clean:
            continue
        if clean.startswith("(") and clean.endswith(")"):
            label = clean[1:-1].strip()
            symbols[label] = rom_address
            user_symbols[label] = rom_address
        else:
            instructions.append(clean)
            rom_address += 1

    # Pass 2: Translate instructions and allocate variables starting at RAM[16]
    next_ram_address = 16
    output_lines = []

    for inst in instructions:
        if inst.startswith("@"):
            symbol = inst[1:].strip()
            if symbol.isdigit():
                val = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_ram_address
                    user_symbols[symbol] = next_ram_address
                    next_ram_address += 1
                val = symbols[symbol]
            output_lines.append(f"{val:016b}")
        else:
            dest, comp, jump = "", inst, ""
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)

            binary = (
                "111"
                + COMP_TABLE[comp.strip()]
                + DEST_TABLE[dest.strip()]
                + JUMP_TABLE[jump.strip()]
            )
            output_lines.append(binary)

    # Save .hack file
    output_path = os.path.splitext(input_path)[0] + ".hack"
    with open(output_path, "w") as f:
        f.write("\n".join(output_lines) + "\n")

    # K mod 3 == 0 feature: Save labels and variables to symbols.txt
    sym_path = os.path.join(os.path.dirname(os.path.abspath(input_path)), "symbols.txt")
    with open(sym_path, "w") as sf:
        sf.write("// Labels and Variables (K = 72, K mod 3 = 0)\n")
        for sym, addr in user_symbols.items():
            sf.write(f"{sym}: {addr}\n")

    print(f"Assembled {output_path} and saved symbol table to {sym_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <Program.asm>")
        sys.exit(1)
    assemble(sys.argv[1])