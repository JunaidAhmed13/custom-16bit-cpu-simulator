; Program 1: a + b and a - b
DATA 128: 7, 61

        LD  R1, 128     ; R1 = a
        LD  R2, 129     ; R2 = b
        MOV R3, R1
        ADD R3, R2      ; R3 = a + b
        ST  R3, 200
        MOV R4, R1
        SUB R4, R2      ; R4 = a - b
        ST  R4, 201
        HLT
