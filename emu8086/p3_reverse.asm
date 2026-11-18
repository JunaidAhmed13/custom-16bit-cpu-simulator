; Program 3: reverse copy
org 100h

    lea si, arr          ; first element
    lea di, rev + 14     ; last place of the copy
    mov cx, 8            ; elements left
copy:
    mov ax, [si]
    mov [di], ax
    add si, 2
    sub di, 2
    loop copy
    mov count, 8         ; answer
    ret

arr   dw 7, 61, 25, 6, 68, 60, 25, 7
rev   dw 8 dup(0)
count dw 0
