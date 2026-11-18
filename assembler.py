import sys
import os
from cpu import *


def to_number(text):
    text = text.strip()
    if text.lower().startswith('0x'):
        return int(text, 16)
    return int(text)


def to_register(text):
    text = text.strip().upper()
    if len(text) != 2 or text[0] != 'R' or text[1] not in '01234567':
        raise Exception("bad register: " + text)
    return int(text[1])


def to_value(text, labels):
    # a label or a number from 0 to 255
    text = text.strip()
    if text.upper() in labels:
        return labels[text.upper()]
    return to_number(text) & 0xFF


def assemble(lines):
    labels = {}
    code = []
    data = {}

    # pass 1: remove comments, save labels and DATA values
    address = 0
    for line in lines:
        if ';' in line:
            line = line[:line.index(';')]
        line = line.strip()
        if line == "":
            continue

        if line.upper().startswith("DATA"):
            start, values = line[4:].split(':')
            start = to_number(start)
            for v in values.split(','):
                data[start] = to_number(v)
                start += 1
            continue

        if ':' in line:
            label, line = line.split(':', 1)
            labels[label.strip().upper()] = address
            line = line.strip()
            if line == "":
                continue

        code.append((address, line))
        address += 1

    # pass 2: build the 16-bit word of every instruction
    words = []
    for address, line in code:
        parts = line.split(None, 1)
        op = parts[0].upper()
        args = []
        if len(parts) > 1:
            args = parts[1].split(',')

        if op not in opcodes:
            raise Exception("unknown instruction: " + line)

        word = opcodes[op] << 12
        if op in REG_FORMAT:
            word = word | to_register(args[0]) << 8 | to_register(args[1]) << 4
        elif op in IMM_FORMAT:
            word = word | to_register(args[0]) << 8 | to_value(args[1], labels)
        elif op in JUMP_FORMAT:
            word = word | to_value(args[0], labels)

        words.append((address, word, line))

    return words, data


def save(name, words, data):
    os.makedirs("output", exist_ok=True)

    # machine code file: address and word in hex
    f = open("output/" + name + ".hex", "w")
    for address, word, line in words:
        f.write(format(address, '02X') + " " + format(word, '04X') + "\n")
    for address in sorted(data):
        f.write(format(address, '02X') + " " + format(data[address], '04X') + "\n")
    f.close()

    # listing: address, machine code, source line
    listing = ["Addr  Code  Source"]
    for address, word, line in words:
        listing.append(format(address, '02X') + "    " + format(word, '04X') + "  " + line)
    open("output/" + name + ".lst", "w").write("\n".join(listing) + "\n")
    return listing


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python assembler.py programs/p1_add_sub.asm")
    else:
        name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
        words, data = assemble(open(sys.argv[1]).readlines())
        print("\n".join(save(name, words, data)))
