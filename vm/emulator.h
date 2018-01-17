#include <cstdint>
#include <string>
#include <vector>
#include <set>

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
	bool at_breakpoint;
	std::set<uint16_t> breakpoints;
} virtual_machine;

void initialize