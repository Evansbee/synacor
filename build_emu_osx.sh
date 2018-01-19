gcc -c -O3 -std=c99 utils/*.c -o utils/emulator.o -fPIC
gcc --shared -o bin/_emu utils/*.o 
rm utils/*.o
