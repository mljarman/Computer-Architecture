"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

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
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
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

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000

        halted = False

        while not halted:
            instruction = self.ram_read(IR)
            operand_a = self.ram_read(IR + 1)
            operand_b = self.ram_read(IR + 2)


            if instruction == LDI:
                reg_num = operand_a
                value = operand_b
                self.reg[reg_num] = value
                IR += 3
            elif instruction == PRN:
                reg_num = self.reg[operand_a]
                print(reg_num)
                IR += 2
            elif instruction == MUL:
                self.alu('MUL', operand_a, operand_b)
                IR += 3
            elif instruction == ADD:
                self.alu('ADD', operand_a, operand_b)
                IR += 3
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
                IR += 2
            elif instruction == POP:
                reg_num = operand_a
                #Copy the value from the address pointed to by SP to the given register.
                top_of_stack_addr = self.reg[SP]
                value = self.ram[top_of_stack_addr]
                # store the value to the given register:
                self.reg[reg_num] = value
                #Increment SP.
                self.reg[SP] += 1
                IR += 2

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

            elif instruction == RET:
                top_of_stack_addr = self.reg[SP]
                return_addr = self.ram[top_of_stack_addr]
                self.reg[SP] += 1

                IR = return_addr

            elif instruction == HLT:
                halted = True
            else:
                print(f'unknown instruction {instruction} at address {IR}')
                sys.exit(1)
