gcc -c -O3 -std=c99 vm/*.c 
gcc --shared -o emu.dll *.o
del *.o