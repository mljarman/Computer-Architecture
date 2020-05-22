"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.fl = {'E': 0, 'L': 0, 'G':0}

        # self.branchtable = {}
        # self.branchtable[HLT] = self.hlt
        # self.branchtable[LDI] = self.ldi
        # self.branchtable[PRN] = self.prn

    def ram_read(self, address):
        """Accept the address to read and return the value stored there."""
        return self.ram[address]

    def ram_write(self, value, address):
        """Accept a value to write, and the address to write it to."""
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    string_val = line.split("#")[0].strip()
                    if string_val == '':
                        continue
                    v = int(string_val, 2)
                    self.ram[address] = v
                    address += 1
        except:
            if len(sys.argv) == 1:
                print('Error, must provide filename.')

            else:
                print('Error, incorrect filename.')
            sys.exit(1)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            # add the values of two regiesters and
            # store in reg_a:
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            # multiply the values of two registers and
            # store in reg_a:
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            # compare the values in two registers:
            # if they are equal:
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl['E'] = 1
            # if reg_a is less than reg_b:
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl['L'] = 1
            # if reg_a is greater than reg_b:
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl['G'] = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # def hlt(self):
    #     pass


    def run(self):
        """Run the CPU."""
        IR = self.pc
        SP = 7
        self.reg[SP] = 0xf4

        ADD = 0b10100000
        CALL = 0b01010000
        CMP = 0b10100111
        HLT = 0b00000001
        JEQ =  0b01010101
        JMP = 0b01010100
        JNE = 0b01010110
        LDI = 0b10000010
        MUL = 0b10100010
        POP = 0b01000110
        PRN = 0b01000111
        PUSH = 0b01000101
        RET = 0b00010001
        #TRY = 0b00000000

        halted = False


        while not halted:
            instruction = self.ram_read(IR)
            operand_a = self.ram_read(IR + 1)
            operand_b = self.ram_read(IR + 2)

            if instruction == ADD:
                # call ALU to add 2 registers and store in reg_a
                self.alu('ADD', operand_a, operand_b)
                # 3 bit operation
                IR += 3

            elif instruction == CALL:
                return_addr = IR + 2
                self.reg[SP] -= 1
                # push it on the stack
                top_of_stack_addr = self.reg[SP]
                self.ram[top_of_stack_addr] = return_addr
                # set the IR to the subroutine addr
                reg_num = operand_a
                subroutine_addr = self.reg[reg_num]
                # don't increment IR because want it to go to
                # the subroutine_addr
                IR = subroutine_addr

            elif instruction == CMP:
                self.alu('CMP', operand_a, operand_b)
                # 3 bit operation
                IR += 3

            elif instruction == HLT:
                # halt program
                halted = True

            elif instruction == JEQ:
                # if equal flag is set to true (1):
                if self.fl['E'] == 1:
                    # jump to the address stored in the given register:
                    reg_num = operand_a
                    addr = self.reg[reg_num]
                    IR = addr
                else:
                    IR += 2

            elif instruction == JMP:
                # jump to address stored in the given register
                reg_num = operand_a
                addr_value = self.reg[reg_num]
                IR = addr_value

            elif instruction == JNE:
                # if equal flag is set to false (0), jump to the address stored
                # in registerB
                if self.fl['E'] == 0:
                    reg_num = operand_a
                    addr = self.reg[reg_num]
                    IR = addr
                else:
                    IR += 2

            elif instruction == LDI:
                reg_num = operand_a
                value = operand_b
                self.reg[reg_num] = value
                IR += 3


            elif instruction == MUL:
                # call ALU to multiply 2 registers and store in reg_a
                self.alu('MUL', operand_a, operand_b)
                # 3 bit operation
                IR += 3

            elif instruction == POP:
                reg_num = operand_a
                # copy the value from the address pointed to by SP to the given register.
                top_of_stack_addr = self.reg[SP]
                value = self.ram[top_of_stack_addr]
                # store the value to the given register:
                self.reg[reg_num] = value
                # increment SP.
                self.reg[SP] += 1
                # 2 bit operation
                IR += 2

            elif instruction == PRN:
                # print numeric value stored in given register
                value = self.reg[operand_a]
                print(value)
                # 2 bit operation
                IR += 2

            elif instruction == PUSH:
                # decrement SP:
                self.reg[SP] -= 1
                # get register #:
                reg_num = operand_a
                # get value out of register:
                value = self.reg[reg_num]
                # store value in memory at SP:
                top_of_stack_addr = self.reg[SP]
                self.ram[top_of_stack_addr] = value
                # 2 bit operation
                IR += 2

            elif instruction == RET:
                # return from subroutine
                # pop the value from the top of the stack and store in IR
                top_of_stack_addr = self.reg[SP]
                return_addr = self.ram[top_of_stack_addr]
                # increment SP
                self.reg[SP] += 1
                # set IR to return_address
                IR = return_addr

            else:
                print(f'unknown instruction {instruction} at address {IR}')
                sys.exit(1)
