gcc -c -O3 -std=c99 utils/*.c -o utils/emulator.o
gcc --shared -o bin/_emu.dll utils/*.o 
del utils/*.o
