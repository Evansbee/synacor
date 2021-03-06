
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include "emulator.h"

#define ARRAY_SIZE_FACTOR (2)


void do_instruction(virtual_machine *vm);




static uint8_t arg_count[22] = {
      0,2,1,1,3,    3,1,2,2,3,    3,3,3,3,2,   2,2,1,0,1,  1,0
};


void reset(virtual_machine* vm)
{
   
//    if(vm->breakpoints)
//    {
//       free(vm->breakpoints);
//       vm->breakpoints = NULL;
//    }

   vm->stack_write_pointer = 0;
   vm->breakpoint_write_pointer = 0;

   vm->cycles = 0;

   for(int i = 0; i < TEXT_BUFFER_SIZE; ++i)
   {
      vm->input_buffer[i] = 0;
      vm->output_buffer[i] = 0;
   }
   vm->input_buffer_write_pointer = 0;

   for(int i = 0; i < MEMORY_SIZE; ++i)
   {
      vm->memory[i] = vm->stored_memory[i] = 0;
   }

   for(int i = 0; i < 8; ++i)
   {
      vm->registers[i] = 0;
   }

   clear_memory_history(vm);

   vm->halted = false;
   vm->at_breakpoint = false;
   vm->waiting_for_input = false;
   vm->program_loaded = false; 
   vm->output_buffer_full = false;
   vm->stack_overflow = false;
   vm->pc = 0;
}

void load(virtual_machine* vm, uint16_t* program, uint32_t length)
{
   for(int i = 0; i < length ;++i)
   {
      vm->memory[i] = vm->stored_memory[i] =  program[i];
   }
   vm->halted = false;
   vm->program_loaded = true;
}

void run_n(virtual_machine* vm, uint32_t n)
{
   for(int i = 0; i < n && !vm->halted; ++i)
   {
      do_instruction(vm);
      if(vm->waiting_for_input || vm->halted || vm->output_buffer_full)
      {
            return;
      }
      vm->at_breakpoint = false;
      for(int i = 0; i < vm->breakpoint_write_pointer; ++i)
      {
            if(vm->pc == vm->breakpoints[i])
            {
                  vm->at_breakpoint = true;
                  return;
            }
      }
   }
}

void run(virtual_machine* vm)
{
      while(!vm->halted)
      {
            do_instruction(vm);
            if(vm->waiting_for_input || vm->halted || vm->output_buffer_full)
            {
                  return;
            }
            vm->at_breakpoint = false;
            for(int i = 0; i < vm->breakpoint_write_pointer; ++i)
            {
                  if(vm->pc == vm->breakpoints[i])
                  {
                        vm->at_breakpoint = true;
                        return;
                  }
            }
      }   
}

inline bool is_reg(uint16_t value)
{
	return value >= 32768 && value <= 32775;
}


inline uint32_t reg_number(uint16_t value)
{
	return value - 32768;
}

inline uint16_t get_value(virtual_machine *vm, uint16_t value)
{
	if(is_reg(value))
	{
		return vm->registers[reg_number(value)];
	}
	return value;
}

inline void push_value_to_stack(virtual_machine *vm, uint16_t value)
{
      vm->stack[vm->stack_write_pointer] = value;
      vm->stack_write_pointer++;     
}

void add_breakpoint(virtual_machine *vm, uint16_t breakpoint)
{
      for(int i = 0; i < vm->breakpoint_write_pointer; ++i)
      {
            if(breakpoint == vm->breakpoints[i])
            {
                  return;
            }
      }

      if(vm->breakpoint_write_pointer < NUM_BREAKPOINTS)
      {
            vm->breakpoints[vm->breakpoint_write_pointer] = breakpoint;
            vm->breakpoint_write_pointer++;
      }
}

void remove_breakpoint(virtual_machine *vm, uint16_t breakpoint)
{
      for(int i = 0; i < vm->breakpoint_write_pointer; ++i)
      {
            if(breakpoint == vm->breakpoints[i])
            {
                  vm->breakpoint_write_pointer--;
                  vm->breakpoints[i] = vm->breakpoints[vm->breakpoint_write_pointer];
                  return;
            }
      }
}
void clear_breakpoints(virtual_machine *vm)
{
      vm->breakpoint_write_pointer = 0;
}

void do_instruction(virtual_machine *vm)
{
      uint32_t len;
	uint16_t opcode = vm->memory[vm->pc];
    
      vm->pc++;
      vm->cycles++;
      
	if(opcode > 21)
	{
            printf("Invalid opcode: %d at pc = %d\n",opcode,vm->pc-1);
            vm->halted = true;
		return;
	}

   //printf("EXPECTED ARGS FOR OP (%d) is %d\n",opcode, arg_count[opcode]);
      uint16_t args[3];
      for(int i=0; i < arg_count[opcode];++i)
      {
            args[i] = vm->memory[vm->pc];
            vm->pc++;
      }


	switch(opcode)
	{
		case 0:
			vm->halted = true;
			return;
		case 1:
			vm->registers[reg_number(args[0])] = get_value(vm,args[1]);
			return;
		case 2:
                  push_value_to_stack(vm,get_value(vm,args[0]));

			return;
		case 3:
                  if(vm->stack_write_pointer == 0)
                  {
                        vm->halted = true;
                        return;
                  }
                  vm->stack_write_pointer--;
			vm->registers[reg_number(args[0])] = vm->stack[vm->stack_write_pointer];
			return;
		case 4:
			vm->registers[reg_number(args[0])] = get_value(vm, args[1]) == get_value(vm, args[2]);
                  return;
            case 5:
                  vm->registers[reg_number(args[0])] = get_value(vm, args[1]) > get_value(vm, args[2]);
                  return;
            case 6:
                  vm->pc = get_value(vm, args[0]);
                  return;
            case 7: //jnz
                  if(get_value(vm, args[0]) != 0)
                  {
                        vm->pc = get_value(vm, args[1]);
                  }
                  return;
            case 8: //jzz
                  if(get_value(vm, args[0]) == 0)
                  {
                        vm->pc = get_value(vm, args[1]);
                  }
                  return;
            case 9:
                  vm->registers[reg_number(args[0])] = (get_value(vm, args[1]) + get_value(vm, args[2])) % 32768;
                  return;
            case 10:
                  vm->registers[reg_number(args[0])] = (get_value(vm, args[1]) * get_value(vm, args[2])) % 32768;
                  return;
            case 11:
                  vm->registers[reg_number(args[0])] = (get_value(vm, args[1]) % get_value(vm, args[2])) % 32768;
                  return;
            case 12:
                  vm->registers[reg_number(args[0])] = (get_value(vm, args[1]) & get_value(vm, args[2])) % 32768 ;
                  return;
            case 13:
                  vm->registers[reg_number(args[0])] = (get_value(vm, args[1]) | get_value(vm, args[2])) % 32768;
                  return;
            case 14:
                  vm->registers[reg_number(args[0])] = (~get_value(vm, args[1]) & 0x7FFF);
                  return;
            case 15: //rmem
                  vm->registers[reg_number(args[0])] = vm->memory[get_value(vm, args[1])];
                  vm->memory_read_history[get_value(vm, args[1])]++;
                  return;
            case 16:
                  vm->memory[get_value(vm, args[0])] = get_value(vm, args[1]);
                  vm->memory_write_history[get_value(vm, args[0])]++;
                  return;
            case 17:
                  push_value_to_stack(vm, vm->pc);
                  vm->pc = get_value(vm, args[0]);
                  return;
            case 18:
                  if(vm->stack_write_pointer == 0)
                  {
                        vm->halted = true;
                        return;
                  }
                  vm->stack_write_pointer--;
			vm->pc = vm->stack[vm->stack_write_pointer];
                  return;
            case 19:
                  len = strlen(vm->output_buffer);
                  if(len < TEXT_BUFFER_SIZE - 1)
                  {
                        vm->output_buffer_full = false;
                        vm->output_buffer[len] = get_value(vm,args[0]);
                        vm->output_buffer[len+1] = '\0';
                  }
                  else
                  {
                        vm->output_buffer_full = true;
                        vm->cycles -= 1;
                        vm->pc -= 2;
                  }
                  return;
            case 20:
                  if(vm->input_buffer[0] == 0)
                  {
                        vm->cycles -= 1;
                        vm->pc -= 2;
                        vm->waiting_for_input = true;
                  }
                  else
                  {
                        vm->waiting_for_input = false;
                        vm->registers[reg_number(args[0])] = vm->input_buffer[0];
                        for(int i = 0; i < TEXT_BUFFER_SIZE-1 != 0; ++i)
                        {
                              vm->input_buffer[i] = vm->input_buffer[i+1];
                              if(vm->input_buffer[i+1] == 0)
                              {
                                    break;
                              }
                              vm->input_buffer[i+1] = 0;
                        }
                  }
                  return;
            case 21:
                  return;
	}
}

void clear_memory_history(virtual_machine* vm)
{
      for(int i=0; i < MEMORY_SIZE; ++i)
      {
            vm->stored_memory[i] = vm->memory[i];
            vm->memory_read_history[i] = 0;
            vm->memory_write_history[i] = 0;
      }
}