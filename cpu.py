# group details
GROUP = 16
MEMBER_1 = "Abdul Wali"
ENROLL_1 = "01-134242-007"
MEMBER_2 = "Malik Junaid Ahmed"
ENROLL_2 = "01-134242-061"

# group parameters from the brief
a = 7
b = 61
S = 5
T = a + b + S
K = T % 16
EXTRA_ROW = T % 7
P2_OPTION = T % 5
P3_OPTION = (T + b) % 5
N = 5 + (a % 6)
M = 2 + (b % 3)

# opcode table: start at K and wrap after F
MANDATORY = ['HLT', 'LDI', 'LD', 'ST', 'LDX', 'STX', 'MOV',
             'ADD', 'SUB', 'CMP', 'JMP', 'JZ', 'JNZ', 'JN']
ALL = MANDATORY + ['XOR', 'LOOP']

opcodes = {}
for i in range(len(ALL)):
    opcodes[ALL[i]] = (K + i) % 16

names = {}
for name in opcodes:
    names[opcodes[name]] = name

# which format each instruction uses
REG_FORMAT = ['LDX', 'STX', 'MOV', 'ADD', 'SUB', 'CMP', 'XOR']
IMM_FORMAT = ['LDI', 'LD', 'ST', 'LOOP']
JUMP_FORMAT = ['JMP', 'JZ', 'JNZ', 'JN']


if __name__ == "__main__":
    print("T =", T, " K =", K, " extra row =", EXTRA_ROW, " P2 option =", P2_OPTION,
          " P3 option =", P3_OPTION, " N =", N, " M =", M)
    for name in ALL:
        print(name.ljust(5), format(opcodes[name], 'X'))
