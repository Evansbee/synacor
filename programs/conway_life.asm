

set r0 0
init: 	
		call .update
		call .print
		add r0 r0 1
		eq r1 r0 0100
		jz r1 .init
		halt



update: push r0
		push r1
		push r2
		push r3
		push r4
		push r5
		push r6
		push r7
		set r0 0
upd_loop:	
		
		
		
		
		
		add r0 r0 1
		eq r1 r0 000F
		jz r1 .upd_loop
		
    	pop r7
		pop r6
		pop r5
		pop r4
		pop r3
		pop r2
		pop r1
		pop r0
		ret

		
cls:   push r0
		set r0 001B
		out r0
		out '['
		out '2'
		out 'J'
		pop r0
		ret
		
		

print: push r0
		push r1
		push r2
		push r3
		push r4
		push r5
		push r6
		push r7
		call .cls
		out 'b'
		out 'o'
		out 'a'
		out 'r'
		out 'd'
		out '\n'
		set r0 0
p_ol:	add r3 r0 .row1
		rmem r4 r3 ;has the row in r4 
		set r1 1
p_il:		
		and r5 r1 r4
		eq r5 r5 0
		jz r5 .p_0
		out '*'
		jmp .printed
p_0:    out '0'		
printed:
		mul r1 r1 2
		eq r2 r1 8000
		jz r2 .p_il
		out '\n'
		add r0 r0 1
		eq r1 r0 000F
		jz r1 .p_ol
		out '\n'
		out '\n'
p_done:	pop r7
		pop r6
		pop r5
		pop r4
		pop r3
		pop r2
		pop r1
		pop r0
		ret




row1: db 0001
row2: db 0010
row3: db 0100
row4: db 1000
row5: db 0001
row6: db 0002
row7: db 0003
row8: db 0004
row9: db 0000
row10: db 0000
row11: db 0000
row12: db 0000
row13: db 0000
row14: db 0000
row15: db 0000
