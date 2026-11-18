# Custom 16-bit processor, assembler and simulator

CSL-327 Computer Architecture Lab project, Bahria University, Fall 2026.
Group 16: Abdul Wali (01-134242-007) and Malik Junaid Ahmed (01-134242-061).

A 16-bit processor with eight registers, 256 words of memory and sixteen instructions.
Our opcode key is K = 9, the assigned instruction is XOR and our own instruction is LOOP.
The assembler turns `.asm` files into 16-bit machine code and the simulator runs that
machine code with a fetch, decode and execute loop while counting instructions, cycles,
CPI and memory accesses.

## Files

| File | What it does |
|---|---|
| `cpu.py` | Group parameters and the opcode table |
| `assembler.py` | Two-pass assembler, writes `output/*.hex` and `output/*.lst` |
| `simulator.py` | Runs a `.hex` file and prints the trace and counters |
| `run_all.py` | Runs every program and draws the graphs in `graphs/` |
| `programs/` | Program 1, Program 2 (Fibonacci) and its LOOP version, Program 3 (reverse copy), XOR demo |
| `emu8086/` | Programs 2 and 3 in 8086 assembly with EMU8086 screenshots |
| `docs/` | Report and design document |

## Running

Needs Python 3 and Matplotlib.

```
python assembler.py programs/p1_add_sub.asm
python simulator.py output/p1_add_sub.hex
python simulator.py output/p3_reverse_copy.hex 5
python run_all.py
```

The number after the `.hex` file is the memory cost M (default 3).

## Results (M = 3)

| Program | Answer | Instructions | Cycles | CPI |
|---|---|---|---|---|
| 1: a + b, a - b | 68 at 200, -54 at 201 | 9 | 17 | 1.89 |
| 2: Fibonacci, N = 6 | 8 at 250 | 28 | 33 | 1.18 |
| 2 with LOOP | 8 at 250 | 23 | 28 | 1.22 |
| 3: reverse copy | 160-167 reversed, 8 at 251 | 55 | 96 | 1.75 |
