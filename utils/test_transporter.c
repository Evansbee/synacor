#include <stdio.h>
#include <stdint.h>

uint16_t r0 = 4;
uint16_t r1 = 1;
uint16_t r7 = 2;

void sub()
{
    uint16_t stored;
	//printf("CALL: %d %d\n",r0,r1);
    if(r0 == 0)
	{
		r0 = r1 + 1;
        r0 = r0 & 0x7FFF;
		return;
	}
	
	if(r1 == 0)
	{
		r0 = r0 - 1;
        r0 = r0 & 0x7fFF;
		r1 = r7;
		sub();
		return;
	}
	
	stored = r0;
	r1 = r1 - 1;
    r1 = r1 & 0x7FFF;
	sub();
	r1 = r0;
	r0 = stored;
	r0 = r0 - 1;
    r0 = r0 & 0x7FFF;
	sub();
	return;
}

int main()
{
    r0 = 4;
    r1 = 1;
    for(r7 = 0; r7 < 20; ++r7)
    {
    sub();
    if(r0 == 6)
    {
        printf("MADE IT-> r0:%x r1:%x r7:%x\n",r0,r1,r7);
    }
    else
    {
        printf("FAIL-> r0:%x r1:%x r7:%x\n",r0,r1,r7);
    }
    }
    
    return 0;
}