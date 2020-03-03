"""CPU functionality."""

import sys

from dispatch import Dispatch

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * (2 ** 8)
        self.register = [0] * 8
        self.register[-1] = 0xF4
        self.pc = 0
        self.dispatch = Dispatch()
        self.sc = 0xF3
        self.fl = 0b00000000

    def ram_read(self, memory):
        return self.ram[memory]

    def ram_write(self, memory, value):
        self.ram[memory] = value

    def load(self):
        """Load a program into memory."""

        address = 0
        try:
            path = sys.argv[1]
        except:
            path = 'examples/print8.ls8'
        with open(path, 'r') as program:

            for instruction in program:
                splits = instruction.split('\\n')
                for i in splits:
                    self.ram[address] = int(i, 2)
                    address += 1
                # if len(instruction) > 1:
                #     if instruction[0] != '#':
                #         self.ram[address] = int(instruction[0:8],2)
                #         address += 1
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        elif op == "CMP":
            if self.register[reg_a] < self.register[reg_b]:
                self.fl = 0b00000100
            elif self.register[reg_a] > self.register[reg_b]:
                self.fl = 0b00000010
            else:
                self.fl = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')
        print()

    def run(self):
        """Run the CPU."""
        while True:
            command = self.ram_read(self.pc)
            # self.trace()
            halt = self.dispatch.run(command, self)
            if halt:
                break
            self.pc += 1