; Program 2: N-th Fibonacci number, N = 6
        LDI R1, 1       ; previous
        LDI R2, 1       ; current
        LDI R3, 6       ; N
        LDI R4, 2
        SUB R3, R4      ; loops = N - 2
        LDI R4, 1
again:  MOV R5, R2
        ADD R2, R1      ; current = current + previous
        MOV R1, R5      ; previous = old current
        SUB R3, R4
        JNZ again
        ST  R2, 250
        HLT
