''' Benchmarks a file'''

import time
from assembler import AssembleFile,PrettyFile
from emulator import VirtualMachine

import sys

def println(s):
    sys.stdout.write(s)
    sys.stdout.flush()
    

def Benchmark(filename, runtime = 10.0, batch = 100000):
    spinner = ['-','\\','|','/']
    spinner_idx = 0
    print("*" * 80)
    print(" [+] Benchmarking File:",filename)
    machine = VirtualMachine()
    println(" [-] Assembling...")
    program = AssembleFile(filename)
    println("\r [+] Assembling...\n")
    machine.LoadProgramFromData(program)
    println(" [-] Running Benchmark...")
    start = time.time()
    while True:
        println("\r [{}] Running Benchmark...".format(spinner[spinner_idx % 4]))
        spinner_idx += 1
        machine.Run_N(batch)
        elapsed = time.time() - start
        if elapsed > runtime:
            break
    println("\r [+] Running Benchmark...\n")
    calc_hz = machine.cycles / elapsed
    mhz = calc_hz / 1000000.0

    print(" [+] Executed {} cycles in {:.1f}s".format(machine.cycles,elapsed))
    print(" [+] Effective clock rate: {:.1f} MHz".format(mhz))
    print("*" * 80)



if __name__ == '__main__':
    myprog = 'programs/conway_life.asm'
    Benchmark(myprog)