0000h         init:  jmp    init.jmp_0003
20 ;blankish line
40                halt   
						db 0234h 20 55
						db '2'
						db '321314' 
100h     .jmp_0003:  out    'bad\n'
out '\n'
out 'a'
200h                out    ';'     ;helloasd asdasd 
300h                out    r0    ; tricky comments have 'this stuff' in them
			set r0 123
			add r0 r1 (@f+1)

0x400 		jmp .jmp_0003
jmp init
1000h     @@:   nop
jmp @b
jmp @r ;go back
jmp @f
@@: nop