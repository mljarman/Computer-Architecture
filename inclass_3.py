import sys
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3 # save a value in a register
PRINT_REG = 4
ADD = 5 # add 2 registers R0 += R1
PUSH = 6

memory = [0] * 256

registers = [0,0,0,0,0,0,0,0] # like variables, named R0-R7
halted = False
pc = 0 # index into the memory array. program counter.
# aka pointer, address, location
SP = 7
registers[SP] = 0xf4 # initialized at place in memory

# load the program from disk
address = 0
with open(sys.argv[1]) as f:
    for line in f:
        string_val = line.split('#')[0].strip()
        if string_val == '':
            continue
        v = int(string_val) # will be different, need specify binary (string_val, 2)
        # print(v)
        memory[address] = v
        address += 1
# run the CPU:
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
    elif instruction == ADD:
        reg_num_a = memory[pc + 1]
        reg_num_b = memory[pc + 2]

        registers[reg_num_a] += registers[reg_num_b]
    elif instruction == PRINT_REG:
        reg_num = memory[pc + 1]
        print(registers[reg_num])
        pc += 2
    elif instruction == PUSH: # eg PUSH R3
        #1. decrement SP
        registers[SP] -= 1
        # get register number
        reg_num = memory[pc + 1]
        # get value out of register:
        val = registers[reg_num]
        # store value in memory at SP
        top_of_stack_addr = registers[SP]
        memory[top_of_stack_addr] = val
        pc += 2


    elif instruction == HALT:
        halted = True
    else:
        print(f'unknown instruction {instruction} at address {pc}')
        sys.exit(1)
