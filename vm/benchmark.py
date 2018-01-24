''' Benchmarks a file'''

import time
from assembler import AssembleFile
from emulator import VirtualMachine

import sys

def println(s):
    sys.stdout.write(s)
    sys.stdout.flush()
    

def Benchmark(filename, runtime = 10.0, batch = 100000):
    spinner = ['-','\\','|','/']
    spinner_idx = 0


    print("*" * 80)
    print("[+] Benchmarking File:",filename)
    #vm = VirtualMachine()
    println("[-] Assembling...")
    #program = AssembleFile(filename)
    println("\r[+] Assembling...\n")
    #vm.LoadProgram(program)
    println("[-] Running Benchmark...")
    start = time.time()
    while True:
        println("\r[{}] Running Benchmark...".format(spinner[spinner_idx % 4]))
        spinner_idx += 1
        #vm.RunNCycles(batch)
        #vm.output_buffer = ''
        time.sleep(.1)
        elapsed = time.time() - start
        if elapsed > runtime:
            break
    println("\r[+] Running Benchmark...\n")
    hz = vm.cycles / elapsed
    mhz = hz / 1000000.0

    print(" [+] Executed {} cycles in {:.2}s".format(vm.cycles,elapsed))
    print(" [+] Effective clock rate: {:.1} MHz".format(mhz))
    print("*" * 80)



if __name__ == '__main__':
    program = 'programs/conway_life.asm'
    Benchmark(program)