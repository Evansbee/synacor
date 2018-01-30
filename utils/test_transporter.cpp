#include <cstdio>
#include <cstdint>
#include <unordered_map>
#include <string>

uint16_t r0 = 4;
uint16_t r1 = 1;
uint16_t r7 = 2;

std::unordered_map<uint32_t,uint32_t> sub_cache;

bool in_cache(uint16_t this_r0, uint16_t this_r1)
{
    uint32_t k = this_r0;
    k = k<<16;
    k += this_r1;

    return sub_cache.find(k) != sub_cache.end();
}

void set_return(uint16_t this_r0, uint16_t this_r1)
{
    uint32_t k = this_r0;
    k = k<<16;
    k += this_r1;

    auto search = sub_cache.find(k);
    if(search != sub_cache.end())
    {
        uint32_t v = search->second;
        r1 = v & 0x7FFF;
        v = v >> 16;
        r0 = v & 0x7FFF;
    }
}

void add_to_cache(uint16_t start_r0, uint16_t start_r1)
{
    uint32_t k = start_r0;
    k = k<<16;
    k += start_r1;

    uint32_t v = r0;
    v = v<<16;
    v += r1;

    sub_cache[k] = v;
}

void sub()
{
	uint16_t stored;
    uint16_t start_r0 = r0;
    uint16_t start_r1 = r1;

    if(in_cache(start_r0, start_r1))
    {
        set_return(start_r0, start_r1);
        return;
    }


	if(r0 == 0) 
	{
		r0 = r1 + 1;
        add_to_cache(start_r0, start_r1);
		return;
	}
	
	if(r1 == 0)
	{
		r0 = r0 - 1;
		r1 = r7;
		sub();
        add_to_cache(start_r0, start_r1);
		return;
	}
	
	stored = r0;     
	r1 = r1 - 1;     
	sub();
	r1 = r0;		 	
	r0 = stored;
	r0 = r0 - 1;
	
	sub();   //--will return when r0 = 0 
    add_to_cache(start_r0, start_r1);
}


int main(int argc, char **argv)
{
    for(r7 = 1; r7 <= 0x7FFF; ++r7)
    {
        sub_cache.clear();
        r0 = 4;
        r1 = 1;

        sub();
        if(r0 == 6)
        {
            printf("MADE IT-> r0:%x r1:%x r7:%x\n",r0,r1,r7);
            return 0;
        }
        else
        {
            printf("FAIL-> r0:%x r1:%x r7:%x\n",r0,r1,r7);
        }
    }
    return 0;
}