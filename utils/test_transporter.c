#include <stdio.h>
#include <stdint.h>

uint16_t r0 = 4;
uint16_t r1 = 1;
uint16_t r7 = 2;

void sub1();
void sub3();
void sub4();

inline void sub1()
{
    r0 = 4;
    uint16_t stored;
    r1 = r7;
    r0 = 3;
    sub3();
    r1 = r0;
    r0 = 3;
    sub4();
    r1 = r0;
    printf("MID: %d %d %d\n",r0,r1,r7);
    
    r0 = 3;
    sub3();

    r1 = r0;

    printf("MID2: %d %d %d\n",r0,r1,r7);


    r0 = 3;
    sub4();    
} 


inline void sub3()
{
    uint16_t stored;
    //---------
    uint16_t start_r0 = r0;
    uint16_t start_r1 = r1;    

    //---------
    if (r1 == 1)
    {
        r1 = r7;
        if (r0 == 1)
        {
            r0 = r7 + 1;
            //printf("(Sub 3) Start: %d %d End: %d %d\n",start_r0, start_r1, r0,r1);
            return;
        }
        r0 = (r0 - 1) & 0x7FFF;
        stored = r0;
        sub3();
        r1 = r0;
        r0 = stored;
        sub4();
        //printf("(Sub 3) Start: %d %d End: %d %d\n",start_r0, start_r1, r0,r1);
        return;
    }
    r1 = (r1 - 1) & 0x7FFF;
    stored = r0;
    sub3();
    r1 = r0;
    r0 = stored;
    sub4();
    //printf("(Sub 3) Start: %d %d End: %d %d\n",start_r0, start_r1, r0,r1);
} 


inline void sub4()
{
    uint16_t stored;
    uint16_t start_r0 = r0;
    uint16_t start_r1 = r1;   
    if (r0 == 1)
    {
        r0 = (r1 + 1) & 0x7FFF;
        //printf("(Sub 4) Start: %d %d End: %d %d\n",start_r0, start_r1, r0,r1);
        return;
    }
    r0 = (r0 - 1) & 0x7FFF;
    stored = r0;
    sub3();
    r1 = r0;
    r0 = stored;
    sub4();   
    printf("(Sub 4) Start: %d %d End: %d %d\n",start_r0, start_r1, r0,r1); 
} 


















void sub()
{
    uint16_t stored;
    if (r0 == 0)
    {
        r0 = (r1 + 1) & 0x7FFF;
        return;
    }

    if (r1 == 0)
    {
        r0 = (r0 - 1) & 0x7FFF;
        r1 = r7;
        sub2();
        return;
    }

    stored = r0;
    r1 = (r1 - 1) & 0x7FFF;
    sub3();
    r1 = r0;
    r0 = stored;
    r0 = (r0 - 1) & 0x7FFF;
    sub();
} 

void sub2()
{
    uint16_t stored;
    if (r0 == 0)
    {
        r0 = (r1 + 1) & 0x7FFF;
        return;
    }

    if (r1 == 0)
    {
        r0 = (r0 - 1) & 0x7FFF;
        r1 = r7;
        sub2();
        return;
    }

    stored = r0;
    r1 = (r1 - 1) & 0x7FFF;
    sub3();
    r1 = r0;
    r0 = stored;
    r0 = (r0 - 1) & 0x7FFF;
    sub4();
} 


void sub3()
{
    uint16_t stored;
    if (r0 == 0)
    {
        r0 = (r1 + 1) & 0x7FFF;
        return;
    }

    if (r1 == 0)
    {
        r0 = (r0 - 1) & 0x7FFF;
        r1 = r7;
        sub2();
        return;
    }

    stored = r0;
    r1 = (r1 - 1) & 0x7FFF;
    sub3();
    r1 = r0;
    r0 = stored;
    r0 = (r0 - 1) & 0x7FFF;
    sub4();
} 

void sub3()
{
    uint16_t stored;
    if (r0 == 0)
    {
        r0 = (r1 + 1) & 0x7FFF;
        return;
    }

    if (r1 == 0)
    {
        r0 = (r0 - 1) & 0x7FFF;
        r1 = r7;
        sub2();
        return;
    }

    stored = r0;
    r1 = (r1 - 1) & 0x7FFF;
    sub3();
    r1 = r0;
    r0 = stored;
    r0 = (r0 - 1) & 0x7FFF;
    sub4();
} 








int main()
{
   
        r0 = 4;

        r7 = 1;
        sub1();
        if(r0 == 6)
        {
            printf("MADE IT-> r0:%x r1:%x r7:%x\n",r0,r1,r7);
        }
        else
        {
            printf("FAIL-> r0:%x r1:%x r7:%x\n",r0,r1,r7);
        }
    
    return 0;
}