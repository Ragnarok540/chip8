import random


class Chip8:
    def __init__(self):
        self.opcode = 0
        self.memory = [0] * 4096
        self.gfx = [0] * 2048  # graphics
        self.regs = [0] * 16  # registers
        self.index = 0
        self.pc = 0x0200  # program_counter

        self.delay_timer = 0
        self.sound_timer = 0

        self.stack = [0] * 16
        self.sp = 0  # stack_pointer

        self.keys = [0] * 16

    @property
    def vxi(self):
        return (self.opcode & 0x0F00) >> 8

    @property
    def vyi(self):
        return (self.opcode & 0x00F0) >> 4

    def emulate_cycle(self):
        self.fetch_opcode()
        self.decode_opcode()
        # update timers

    def fetch_opcode(self):
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]

    def decode_opcode(self):
        match self.opcode & 0xF000:
            case 0x0000:
                match self.opcode & 0x00FF:
                    case 0x00E0:
                        self.clear_screen()
                    case 0x00EE:
                        self.ret()
                    case _:
                        raise DecodeError(hex(self.opcode))
            case 0x1000:
                self.goto()
            case 0x2000:
                self.call()
            case 0x3000:
                self.skip_equal()
            case 0x4000:
                self.skip_not_equal()
            case 0x5000:
                self.skip_equal_reg()
            case 0x6000:
                self.load_reg()
            case 0x7000:
                self.add_constant()
            case 0x8000:
                match self.opcode & 0x000F:
                    case 0x0000:
                        self.set_reg()
                    case 0x0001:
                        self.bitwise_or()
                    case 0x0002:
                        self.bitwise_and()
                    case 0x0003:
                        self.bitwise_xor()
                    case 0x0004:
                        self.add()
                    case 0x0005:
                        self.sub()
                    case 0x0006:
                        self.shr()
                    case 0x0007:
                        self.subn()
                    case 0x000E:
                        self.shl()
                    case _:
                        raise DecodeError(hex(self.opcode))
            case 0x9000:
                self.skip_reg_not_equal()
            case 0xA000:
                self.load_index()
            case 0xB000:
                self.jump()
            case 0xC000:
                self.random_value()
            case 0xD000:
                self.draw()
            case 0xE000:
                match self.opcode & 0x00FF:
                    case 0x009E:
                        self.skip_key_pressed()
                    case 0x00A1:
                        self.skip_key_not_pressed()
                    case _:
                        raise DecodeError(hex(self.opcode))
            case 0xF000:
                match self.opcode & 0x00FF:
                    case 0x0007:
                        self.load_delay()
                    case 0x000A:
                        self.load_key_pressed()
                    case 0x0015:
                        self.set_delay()
                    case 0x0018:
                        self.set_sound()
                    case 0x001E:
                        self.add_index()
                    case 0x0029:
                        self.load_hex_sprite()
                    case 0x0033:
                        self.store_bcd()
                    case 0x0055:
                        self.store_regs()
                    case 0x0065:
                        self.read_regs()
                    case _:
                        raise DecodeError(hex(self.opcode))
            case _:
                raise DecodeError(hex(self.opcode))

    # 00E0
    def clear_screen(self):
        """
        clear the screen
        """
        self.gfx = [0] * 2048
        self.pc += 2

    # 00EE
    def ret(self):
        """
        return from a subroutine
        """
        self.sp -= 1
        self.pc = self.stack[self.sp]

    # 1NNN
    def goto(self):
        """
        jump to location nnn
        """
        self.pc = self.opcode & 0x0FFF

    # 2NNN
    def call(self):
        """
        call subroutine at nnn
        """
        self.stack[self.sp] = self.pc
        self.sp += 1
        self.pc = self.opcode & 0x0FFF

    # 3XNN
    def skip_equal(self):
        """
        skip next instruction if vX = NN
        """
        vx = self.regs[self.vxi]

        if vx == (self.opcode & 0x00FF):
            self.pc += 4
        else:
            self.pc += 2

    # 4XNN
    def skip_not_equal(self):
        """
        skip next instruction if vX != NN
        """
        vx = self.regs[self.vxi]

        if vx != (self.opcode & 0x00FF):
            self.pc += 4
        else:
            self.pc += 2

    # 5XY0
    def skip_equal_reg(self):
        """
        skip next instruction if vX = vY
        """
        vx = self.regs[self.vxi]
        vy = self.regs[self.vyi]

        if vx == vy:
            self.pc += 4
        else:
            self.pc += 2

    # 6XNN
    def load_reg(self):
        """
        set vX = NN
        """
        self.regs[self.vxi] = self.opcode & 0x00FF
        self.pc += 2

    # 7XNN
    def add_constant(self):
        """
        set vX = vX + NN
        """
        self.regs[self.vxi] += self.opcode & 0x00FF
        self.pc += 2

    # 8XY0
    def set_reg(self):
        """
        set vX to the value of vY
        """
        self.regs[self.vxi] = self.regs[self.vyi]
        self.pc += 2

    # 8XY1
    def bitwise_or(self):
        """
        set vX = vX OR vY
        """
        self.regs[self.vxi] = self.regs[self.vxi] | self.regs[self.vyi]
        self.pc += 2

    # 8XY2
    def bitwise_and(self):
        """
        set vX = vX AND vY
        """
        self.regs[self.vxi] = self.regs[self.vxi] & self.regs[self.vyi]
        self.pc += 2

    # 8XY3
    def bitwise_xor(self):
        """
        set vX = vX XOR vY
        """
        self.regs[self.vxi] = self.regs[self.vxi] ^ self.regs[self.vyi]
        self.pc += 2

    # 8XY4
    def add(self):
        """
        set vX = vX + vY, set vF = 1 if vX > 255
        """
        val = self.regs[self.vxi] + self.regs[self.vyi]
        self.regs[self.vxi] = val & 0xFF

        if val > 0xFF:
            self.regs[0xF] = 0x1
        else:
            self.regs[0xF] = 0x0

        self.pc += 2

    # 8XY5
    def sub(self):
        """
        set vF = 1 if vX > vY, set vX = vX - vY
        """
        if self.regs[self.vxi] > self.regs[self.vyi]:
            self.regs[0xF] = 0x1
        else:
            self.regs[0xF] = 0x0

        self.regs[self.vxi] = self.regs[self.vxi] - self.regs[self.vyi]
        self.pc += 2

    # 8XY6
    def shr(self):
        """
        set vX = vY
        if the least-significant bit of vX is 1, then vF = 1
        shift vX one bit to the right
        """
        self.regs[self.vxi] = self.regs[self.vyi]

        if self.regs[self.vxi] & 0b1 == 0b1:
            self.regs[0xF] = 0x1
        else:
            self.regs[0xF] = 0x0

        self.regs[self.vxi] = self.regs[self.vxi] >> 1
        self.pc += 2

    # 8XY7
    def subn(self):
        """
        set vF = 1 if vY > vX, set vX = vY - vX
        """
        if self.regs[self.vyi] > self.regs[self.vxi]:
            self.regs[0xF] = 0x1
        else:
            self.regs[0xF] = 0x0

        self.regs[self.vxi] = self.regs[self.vyi] - self.regs[self.vxi]
        self.pc += 2

    # 8XYE
    def shl(self):
        """
        set vX = vY
        if the most-significant bit of vX is 1, then vF = 1
        shift vX one bit to the left
        """
        self.regs[self.vxi] = self.regs[self.vyi]

        if self.regs[self.vxi] & 0b10000000 == 0b10000000:
            self.regs[0xF] = 0x1
        else:
            self.regs[0xF] = 0x0

        self.regs[self.vxi] = self.regs[self.vxi] << 1
        self.pc += 2

    # 9XY0
    def skip_reg_not_equal(self):
        """
        skip next instruction if vX != vY
        """

    # ANNN
    def load_index(self):
        """
        set I to NNN
        """
        self.index = self.opcode & 0x0FFF
        self.pc += 2

    # BNNN
    def jump(self):
        """
        jump to address NNN + v0
        """
        self.pc = self.regs[0] + (self.opcode & 0x0FFF)

    # CXNN
    def random_value(self):
        """
        set vX to a random value masked (bitwise AND) with NN
        """
        result = random.randint(0, 255) & (self.opcode & 0x00FF)
        self.regs[self.vxi] = result
        self.pc += 2

    # DXYN
    def draw(self):
        """
        draw 8xN pixel sprite at position vX, vY with data starting at the address in I
        """

    # EX9E
    def skip_key_pressed(self):
        """
        skip next instruction if key with the value of vX is pressed
        """

    # EXA1
    def skip_key_not_pressed(self):
        """
        skip next instruction if key with the value of vX is not pressed
        """

    # FX07
    def load_delay(self):
        """
        set vX = delay timer value
        """

    # FX0A
    def load_key_pressed(self):
        """
        set vX = key pressed
        """

    # FX15
    def set_delay(self):
        """
        set delay timer value = vX
        """

    # FX18
    def set_sound(self):
        """
        set sound timer value = vX
        """

    # FX1E
    def add_index(self):
        """
        set I = I + vX
        """

    # FX29
    def load_hex_sprite(self):
        """
        set I = location of sprite for digit vX
        """

    # FX33
    def store_bcd(self):
        """
        store BCD representation of vX in memory locations I, I+1, and I+2
        """

    # FX55
    def store_regs(self):
        """
        store registers v0 through vX in memory starting at location I
        """

    # FX65
    def read_regs(self):
        """
        read registers v0 through vX from memory starting at location I
        """


class DecodeError(Exception):
    """
    use when the opcode can not be decoded
    """
    def __init__(self, message):
        self.message = f'opcode could not be decoded: {message}'

    def __str__(self):
        return self.message
