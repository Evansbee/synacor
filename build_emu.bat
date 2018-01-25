gcc -c -O3 -std=c99 utils/*.c -o utils/emulator.o
gcc --shared utils/emulator.o -o bin/_emu.dll 
del utils\emulator.o
