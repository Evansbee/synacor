'''Interface to the SYNACOR VM functionality'''

from .assembler import (
    Assemble, 
    AssembleFile, 
    Disassemble, 
    DisassembleFile,
    Pretty,
    PrettyFile,
)

from .emulator import (
    VirtualMachine
)

from .benchmark import (
    Benchmark
)