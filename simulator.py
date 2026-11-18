import sys
from cpu import *

registers = [0] * 8
memory = [0] * 256
flags = {'Z': 0, 'N': 0}
pc = 0

cycles = 0
instruction_count = 0
memory_accesses = 0
mix = {}


def reset():
    global pc, cycles, instruction_count, memory_accesses, mix
    for i in range(8):
        registers[i] = 0
    for i in range(256):
        memory[i] = 0
    flags['Z'] = 0
    flags['N'] = 0
    pc = 0
    cycles = 0
    instruction_count = 0
    memory_accesses = 0
    mix = {}


def load(hex_file):
    # each line is: address word
    for line in open(hex_file):
        parts = line.split()
        if len(parts) == 2:
            memory[int(parts[0], 16)] = int(parts[1], 16)


def signed(value):
    if value & 0x8000:
        return value - 65536
    return value


def set_flags(value):
    if value == 0:
        flags['Z'] = 1
    else:
        flags['Z'] = 0
    flags['N'] = (value >> 15) & 1


def disassemble(ir):
    op = names[ir >> 12]
    rd = (ir >> 8) & 0xF
    rs = (ir >> 4) & 0xF
    value = ir & 0xFF
    if op == 'HLT':
        return 'HLT'
    if op in REG_FORMAT:
        return op + " R" + str(rd) + ", R" + str(rs)
    if op == 'LOOP':
        return op + " R" + str(rd) + ", " + format(value, '02X')
    if op in IMM_FORMAT:
        return op + " R" + str(rd) + ", " + str(value)
    return op + " " + format(value, '02X')


def step(mem_cost):
    global pc, cycles, instruction_count, memory_accesses

    # fetch
    ir = memory[pc]
    pc = pc + 1

    # decode
    op = names[ir >> 12]
    rd = (ir >> 8) & 0xF
    rs = (ir >> 4) & 0xF
    value = ir & 0xFF

    # execute
    cost = 1
    if op == 'HLT':
        pass
    elif op == 'LDI':
        registers[rd] = value
    elif op == 'LD':
        registers[rd] = memory[value]
        cost = mem_cost
        memory_accesses += 1
    elif op == 'ST':
        memory[value] = registers[rd]
        cost = mem_cost
        memory_accesses += 1
    elif op == 'LDX':
        registers[rd] = memory[registers[rs] & 0xFF]
        cost = mem_cost
        memory_accesses += 1
    elif op == 'STX':
        memory[registers[rs] & 0xFF] = registers[rd]
        cost = mem_cost
        memory_accesses += 1
    elif op == 'MOV':
        registers[rd] = registers[rs]
    elif op == 'ADD':
        registers[rd] = (registers[rd] + registers[rs]) & 0xFFFF
        set_flags(registers[rd])
    elif op == 'SUB':
        registers[rd] = (registers[rd] - registers[rs]) & 0xFFFF
        set_flags(registers[rd])
    elif op == 'CMP':
        set_flags((registers[rd] - registers[rs]) & 0xFFFF)
    elif op == 'XOR':
        registers[rd] = registers[rd] ^ registers[rs]
        set_flags(registers[rd])
    elif op == 'JMP':
        pc = value
        cost = 2
    elif op == 'JZ':
        if flags['Z'] == 1:
            pc = value
            cost = 2
    elif op == 'JNZ':
        if flags['Z'] == 0:
            pc = value
            cost = 2
    elif op == 'JN':
        if flags['N'] == 1:
            pc = value
            cost = 2
    elif op == 'LOOP':
        # our own instruction: count down and jump back
        registers[rd] = (registers[rd] - 1) & 0xFFFF
        if registers[rd] != 0:
            pc = value
            cost = 2

    # counters
    cycles += cost
    instruction_count += 1
    mix[op] = mix.get(op, 0) + 1

    return ir, op


def run(hex_file, mem_cost=M, show=True):
    reset()
    load(hex_file)
    out = []

    out.append("Group " + str(GROUP) + "   " + MEMBER_1 + " " + ENROLL_1 + "   " + MEMBER_2 + " " + ENROLL_2)
    out.append("Opcode key K = " + format(K, 'X') + "   memory cost M = " + str(mem_cost))
    out.append("")
    header = "Step  PC  IR    Instruction    "
    for i in range(8):
        header += ("R" + str(i)).rjust(6)
    header += "  Z N  Cycles"
    out.append(header)

    step_no = 0
    while step_no < 10000:
        old_pc = pc
        ir, op = step(mem_cost)
        step_no += 1
        row = str(step_no).rjust(4) + "  " + format(old_pc, '02X') + "  " + format(ir, '04X') + "  " + disassemble(ir).ljust(15)
        for r in registers:
            row += str(signed(r)).rjust(6)
        row += "  " + str(flags['Z']) + " " + str(flags['N']) + "  " + str(cycles).rjust(6)
        out.append(row)
        if op == 'HLT':
            break

    cpi = cycles / instruction_count
    out.append("")
    out.append("Instructions executed: " + str(instruction_count))
    out.append("Total cycles:          " + str(cycles))
    out.append("CPI:                   " + str(round(cpi, 2)))
    out.append("Memory accesses:       " + str(memory_accesses))
    out.append("Instruction mix:       " + ", ".join(k + "=" + str(mix[k]) for k in mix))
    out.append("")
    out.append("Data memory (non zero):")
    for address in range(128, 256):
        if memory[address] != 0:
            out.append("  mem[" + str(address) + "] = " + format(memory[address], '04X') + "  (" + str(signed(memory[address])) + ")")

    if show:
        print("\n".join(out))

    return {
        'instructions': instruction_count,
        'cycles': cycles,
        'cpi': cpi,
        'memory_accesses': memory_accesses,
        'mix': dict(mix),
        'memory': list(memory),
        'trace': out,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python simulator.py output/p1_add_sub.hex [M]")
    else:
        cost = M
        if len(sys.argv) > 2:
            cost = int(sys.argv[2])
        run(sys.argv[1], cost)
