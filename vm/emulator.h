
#ifndef __EMULATOR_H__
#define __EMULATOR_H__

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#define TEXT_BUFFER_SIZE (2048)
#define NUM_BREAKPOINTS (64)
#define STACK_SIZE (1000)
#define MEMORY_SIZE (0x7FFF)

typedef struct  {
	uint16_t pc;
	uint16_t registers[8];
	uint16_t memory[MEMORY_SIZE];

	uint16_t breakpoints[NUM_BREAKPOINTS];
	uint16_t breakpoint_write_pointer;
	uint16_t stack[STACK_SIZE];
	uint16_t stack_write_pointer;

	uint64_t cycles;

	char input_buffer[TEXT_BUFFER_SIZE];
	char output_buffer[TEXT_BUFFER_SIZE];

	int halted;
	int program_loaded;
	int waiting_for_input;
	int output_buffer_full;
	int stack_overflow;
	int at_breakpoint;

} virtual_machine;

void reset(virtual_machine* vm);
void load(virtual_machine* vm, uint16_t* program, uint32_t length);
void run_n(virtual_machine* vm, uint32_t n);
void run(virtual_machine* vm);
void add_breakpoint(virtual_machine *vm, uint16_t breakpoint);
void remove_breakpoint(virtual_machine *vm, uint16_t breakpoint);
void clear_breakpoints(virtual_machine *vm);
#endif
