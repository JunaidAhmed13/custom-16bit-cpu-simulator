; XOR demo: XOR result, swap with XOR, clear with XOR
        LDI R1, 12
        LDI R2, 10
        XOR R1, R2      ; 12 xor 10 = 6
        ST  R1, 210
        XOR R2, R1      ; R2 = 12
        XOR R1, R2      ; R1 = 10, so R1 and R2 swapped
        ST  R1, 211
        ST  R2, 212
        XOR R3, R3      ; R3 = 0 and Z = 1
        HLT
