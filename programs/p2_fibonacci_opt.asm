; Program 2 optimized with LOOP
        LDI R1, 1       ; previous
        LDI R2, 1       ; current
        LDI R3, 6       ; N
        LDI R4, 2
        SUB R3, R4      ; loops = N - 2
again:  MOV R5, R2
        ADD R2, R1
        MOV R1, R5
        LOOP R3, again  ; R3 = R3 - 1, jump if not zero
        ST  R2, 250
        HLT
