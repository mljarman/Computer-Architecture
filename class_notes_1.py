'''
Number Bases
------------

how many digits
     vv
base 10 'decimal'
base 2 'binary'
base 16 'hexadecimal' 'hex'
base 8 'octal' (rare these days)
base 64 'base 64'

0-9 10
a-z 26
A-Z 26

decimal
0
1
2
3
4
5
6
7
8
9
10


binary
0 0
1 1
10 2
11 3
100 4
101 5

ob1100 == 12
ob10000 == 16
ob01111 == 15

think of them as different languages
when you store a number, pure mathematical number. when you print it or have it
as input thats when you decide what language to use.

Hex (base 16, 0-9A-F)
0
1
2
3
4
5
6
7
8
9
A 10
B 11
C 12
D 13
E 14
F 15 == 15 == ob11111(biggest value you can represent in 4 bits) 4 bits is a nibble
10 - 16's place (1)  1's place (0)
100 - 256's place (1) 16's place(0) 1's place(0)

one hex digit is exactly 4 bits
 0x06 == ob??

 0         6
 0000     0110
 ==ob00000110

0x24 == 0b????
2         A
0010    1010
==00101010

0b11001100 == 0XCC

1100   1100
C       C

255 == 0b???

255 == ob11111111 (biggest number you can have in a single byte) == 0x???
1111 1111
 F     F
 == 0xFF
 FF00FF
 RRGGBB red green blue

'''

# a simple virtual CPU
# a program that pretends to be a CPU

# i want to:
#  * store a sequence of instructions
#  * go through instructions, doing whatever they ask me to do

# Instructions
#   * print 'beej' on the screen
#   * halts the program
import sys
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3 # save a value in a register
PRINT_REG = 4
ADD = 5 # add 2 registers R0 += R1


memory = [
    PRINT_BEEJ, # << pc=0
    SAVE_REG, # save_reg as RO, with value 12 opcode
    0, # operand (argument)
    12,
    PRINT_REG, # print reg R0
    0
    SAVE_REG,
    1,
    37,
    ADD, # what assignment today is
    0,
    1,
    HALT
]

registers = [0,0,0,0,0,0,0,0] # like variables, named R0-R7
halted = False
pc = 0 # index into the memory array. program counter.
# aka pointer, address, location
while not halted:
    instruction = memory[pc]
    if instruction == PRINT_BEEJ:
        print('Beej!')
        pc += 1
    elif instruction == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        registers[reg_num] = value
        pc += 3 # since 3 line instruction, 3 bytes so increment by 3
    elif instruction == PRINT_REG:
        reg_num = memory[pc + 1]
        print(registers[reg_num])
        pc += 2
    elif instruction == HALT:
        halted = True
    else:
        print(f'unknown instruction {instruction} at address {pc}')
        sys.exit(1)
