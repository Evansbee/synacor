#include "emulator.h"

typedef struct  {
	uint16_t pc;
	uint16_t registers[8];
	uint16_t memory[0x7FFF];
	uint64_t cycles;
	std::vector<uint16_t> stack;
	std::string input_buffer;
	std::string output_buffer;
	bool halted;
	bool program_loaded;
	bool waiting_for_input;
	bool at_breakpoint;
	std::set<uint16_t> breakpoints;
} virtual_machine;


void do_instruction(virtual_machine *vm);

void reset(virtual_machine* vm);
void load(virtual_machine* vm, uint16_t* program, size_t length);
void run_n(virtual_machine* vm, size_t)
{
	
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
			vm->registers[reg_number(vm->memory[vm->pc + 1]] = get_value(vm->memory[vm->pc+2])
			vm->pc += 2;
			return;
	}
}