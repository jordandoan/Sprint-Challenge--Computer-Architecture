HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
PRA = 0b01001000
class Dispatch():
    def __init__(self):
        self.dispatch = {
            HLT: self.halt,
            LDI: self.load_immediate,
            PRN: self.print,
            MUL: self.multiply,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            ADD: self.add,
            CMP: self.compare,
            JMP: self.jump,
            JEQ: self.equal,
            JNE: self.not_equal,
            PRA: self.ascii
        }
    def ascii(self, cpu):
        print(chr((cpu.register[cpu.ram_read(cpu.pc+1)])))
        cpu.pc += 1
    def run(self, command, cpu):
        return self.dispatch[command](cpu)

    def halt(self, cpu):
        return True

    def compare(self, cpu):
        reg1 = cpu.ram_read(cpu.pc+1)
        reg2 = cpu.ram_read(cpu.pc+2)
        cpu.alu('CMP', reg1, reg2)
        cpu.pc += 2

    def call(self, cpu):
        RET = 0b00010001
        self.push(cpu, cpu.pc)
        cpu.pc = cpu.register[cpu.ram_read(cpu.pc)]
        while cpu.ram_read(cpu.pc) != RET:
            self.run(cpu.ram_read(cpu.pc), cpu)
            cpu.pc += 1
        top = cpu.ram_read(cpu.sc + 1)
        cpu.ram_write(cpu.sc + 1, 0)
        cpu.sc += 1
        cpu.pc = top + 1

    def load_immediate(self, cpu):
        reg_id = cpu.ram_read(cpu.pc + 1)
        val = cpu.ram_read(cpu.pc + 2)
        cpu.register[reg_id] = val
        cpu.pc += 2

    def print(self, cpu):
        print(cpu.register[cpu.ram_read(cpu.pc + 1)])
        cpu.pc += 1

    def add(selfm, cpu):
        val1 = cpu.ram_read(cpu.pc + 1)
        val2 = cpu.ram_read(cpu.pc + 2)
        cpu.pc += 2
        cpu.register[val1] += cpu.register[val2]

    def multiply(self, cpu):
        val1 = cpu.ram_read(cpu.pc + 1)
        val2 = cpu.ram_read(cpu.pc + 2)
        cpu.pc += 2
        print(cpu.register[val1] * cpu.register[val2])

    def push(self, cpu, val=None):
        if not val:
            register = cpu.ram_read(cpu.pc + 1)
            val = cpu.register[register]
        cpu.ram_write(cpu.sc, val)
        cpu.sc -= 1
        cpu.pc += 1

    def pop(self, cpu):
        top = cpu.ram_read(cpu.sc+1)
        register = cpu.ram_read(cpu.pc + 1)
        cpu.register[register] = top
        cpu.ram_write(cpu.sc, 0)
        cpu.sc += 1
        cpu.pc += 1

    def jump(self, cpu):
        reg = cpu.ram_read(cpu.pc + 1)
        cpu.pc = cpu.register[reg]-1

    def equal(self, cpu):
        # equal flag is 0b00000001, = 1
        if cpu.fl == 1:
            self.jump(cpu)
        else:
            cpu.pc += 1

    def not_equal(self, cpu):
        # not equal means flag is 0b00000010
        # or 0b00000100
        if cpu.fl > 1:
            self.jump(cpu)
        else:
            cpu.pc += 1