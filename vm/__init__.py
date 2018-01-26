'''Interface to the SYNACOR VM functionality'''

from .assembler import (
    Assemble, 
    AssembleFile, 
    Disassemble, 
    DisassembleFile,
    Pretty,
    PrettyFile,
    Parse,
    ParseFile
)

from .emulator import (
    VirtualMachine
)

from .benchmark import (
    Benchmark
)

from .views import (
    SynacorWorkspace
)