''' Benchmarks a file'''

import time
from .assembler import AssembleFile
from .emulator import VirtualMachine



def Benchmark(filename, runtime = 10.0, batch = 10000):
    print("*" * 80)
    print("** Benchmarking File:",filename)
    print("** Assembling...)
    vm = VirtualMachine()
    print("** Assembling...)
    program = AssembleFile(filename)
    vm.LoadProgram(program)
    print("** Running Benchmark...)
    start = time.time()
    while True:
        vm.RunNCycles(batch)
        vm.output_buffer = ''
        elapsed = time.time() - start
        if elapsed > runtime:
            break
    print("** Benchmark Complete...)
    hz = vm.cycles / elapsed
    mhz = hz / 1000000.0

    print("** Executed {} cycles in {:.2}s".format(vm.cycles,elapsed))
    print("** Effective clock rate: {:.1} MHz".format(mhz))
    print("*" * 80)



if __name__ == '__main__':
    program = 'programs/conway_life.asm'
    Benchmark(program)