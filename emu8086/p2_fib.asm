; Program 2: Fibonacci, N = 6
org 100h

    mov ax, 1        ; previous
    mov bx, 1        ; current
    mov cx, 6        ; N
    sub cx, 2        ; loops = N - 2
again:
    mov dx, bx
    add bx, ax       ; current = current + previous
    mov ax, dx       ; previous = old current
    loop again
    mov result, bx   ; answer
    ret

result dw 0
