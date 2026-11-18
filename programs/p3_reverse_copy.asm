; Program 3: copy the array to 160-167 in reverse order
DATA 128: 7, 61, 25, 6, 68, 60, 25, 7

        LDI R1, 128     ; first element
        LDI R2, 167     ; last place of the copy
        LDI R3, 8       ; elements left
        LDI R4, 1
copy:   LDX R5, R1
        STX R5, R2
        ADD R1, R4
        SUB R2, R4
        SUB R3, R4
        JNZ copy
        LDI R6, 8
        ST  R6, 251     ; answer = elements copied
        HLT
