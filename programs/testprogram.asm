@0000         init:  jmp    .jmp_0003
@0002                halt   
@0003     jmp_0003:  out    'h'
@0005                out    'i'
@0007                out    '\n'
set r0 0FAB
call .fcn
out '\n'
               halt   

fcn:
set r1 0
set r2 r0
back:
mod r3 r2 10
add r0 .num r3
rmem r0 r0
out r0
add r5 r1 1
gt r5 r5 4
jz r5 .done
mul r2 r2 10
done: ret





num: db '0'
db '1'
db '2'
db '3'
db '4'
db '5
db '6'
db '7'
db '8'
db '9'
db 'A'
db 'B'
db 'C'
db 'D'
db 'E'
db 'F'
