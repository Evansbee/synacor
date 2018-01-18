#include "emulator.h"

#define ARRAY_SIZE_FACTOR (2)


typedef struct  {
	uint16_t pc;
	uint16_t registers[8];
	uint16_t memory[0x7FFF];

   uint16_t *breakpoints;
   uint16_t breakpoint_write_pointer;
   uint16_t breakpoint_reserved;

   uint16_t *stack;
   uint16_t stack_write_pointer;
   uint16_t stack_reserved;

   uint64_t cycles;
	
   char input_buffer[2048];
	char output_buffer[2048];
	
   bool halted;
	bool program_loaded;
	bool waiting_for_input;
	bool at_breakpoint;

} virtual_machine;


void do_instruction(virtual_machine *vm);

void reset(virtual_machine* vm)
{
   if(vm->stack)
   {
      free(vm->stack);
      vm->stack = NULL;
   }

   if(vm->breakpoints)
   {
      free(vm->breakpoints);
      vm->breakpoints = NULL;
   }

   vm->breakpoint_write_pointer = 0;
   vm->breakpoint_reserved = 16;
   vm->breakpoints = malloc(vm->breakpoint_reserved * sizeof(uint16_t));

   vm->stack_write_pointer = 0;
   vm->stack_reserved = 16;
   vm->stack = malloc(vm->stack_reserved * sizeof(uint16_t));

   vm->cycles = 0;

   for(int i = 0; i < 2048; ++i)
   {
      vm->input_buffer[i] = 0;
      vm->output_buffer[i] = 0;
   }

   for(int i = 0; i < 0x7FFF; ++i)
   {
      vm->memory[i] = 0;
   }

   for(int i = 0; i < 8; ++i)
   {
      vm->registers[i] = 0
   }

   vm->halted = false;
   vm->at_breakpoint = false;
   vm->waiting_for_input = false;
   vm->program_loaded = false; 
   vm->pc = 0;
}

void load(virtual_machine* vm, uint16_t* program, size_t length)
{
   for(int i = 0; i < length ;++i)
   {
      vm->memory[i] = program[i];
   }
   vm->halted = false;
   vm->program_loaded = true;
}

void run_n(virtual_machine* vm, size_t n)
{
   for(int i = 0; i < n; ++i)
   {
      do_instruction(vm);
      if(vm->waiting_for_input || vm->halted)
      {
         return;
      }
      for(auto j = 0; j < vm->breakpoint_write_pointer; ++j)
      {
         if(vm->pc == vm->breakpoints[j])
         {
            vm->at_breakpoint = true;
            return;
         }
      }
}

inline bool is_reg(uint16_t value)
{
	return value >= 32768 && value <= 32775;
}


inline size_t reg_number(value)
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

void do_instruction(virtual_machine *vm)
{
	auto opcode = vm->memory[vm->pc];
	if(opcode > 21)
	{
		vm->halted = true;
		return
	}


	switch(opcode)
	{
		case 0:
			vm->halted = true;
			return;
		case 1:
			vm->registers[reg_number(vm->memory[vm->pc + 1]] = get_value(vm, vm->memory[vm->pc+2])
			vm->pc += 3;
			return;
		case 2:
			vm->stack.push_back(get_value(vm,vm->memory[vm->pc+1]));
			vm->pc += 2;
			return;
		case 3:
			vm->registers[reg_number(vm->memory[vm->pc + 1]] = vm->stack.back()
			vm->stack.pop_back();
			vm->pc += 2;
			return;
		case 4:
			vm->registers[reg_number(vm->memory[vm->pc + 1]] = ()
	}
}
