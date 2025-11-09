import random


class Chip8:
    def __init__(self):
        self.opcode = 0
        self.memory = [0x0] * 4096
        self.gfx = [0] * 2048  # graphics
        self.regs = [0] * 16  # registers
        self.index = 0
        self.pc = 0x0200  # program_counter

        self.delay_timer = 0
        self.sound_timer = 0
        self.draw_flag = False

        self.stack = [0] * 16
        self.sp = 0  # stack_pointer

        self.keys = [0] * 16

    @property
    def vxi(self):
        return (self.opcode & 0x0F00) >> 8

    @property
    def vyi(self):
        return (self.opcode & 0x00F0) >> 4

    @property
    def n(self):
        return self.opcode & 0x000F

    @property
    def nn(self):
        return self.opcode & 0x00FF

    @property
    def nnn(self):
        return self.opcode & 0x0FFF

    def load_rom(self, path: str):
        counter = 0

        with open(path, 'rb') as rom:
            while True:
                chunk = rom.read(1)

                if not chunk:
                    break

                self.memory[self.pc + counter] = chunk[0]
                counter += 1

    def draw_console(self):
        for y in range(0, 32):
            for x in range(0, 64):
                if self.gfx[x + y * 64]:
                    print('█', end='')
                else:
                    print(' ', end='')

                if x == 63:
                    print()

    def emulate_cycle(self):
        self.draw_flag = False
        self.fetch_opcode()
        print(hex(self.opcode))
        self.pc += 2
        self.decode_opcode()

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1

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

    # 00E0 TESTED
    def clear_screen(self):
        """
        clear the screen
        """
        self.gfx = [0] * 2048

    # 00EE TESTED
    def ret(self):
        """
        return from a subroutine
        """
        self.sp -= 1
        self.pc = self.stack[self.sp]

    # 1NNN TESTED
    def goto(self):
        """
        jump to location nnn
        """
        self.pc = self.nnn

    # 2NNN TESTED
    def call(self):
        """
        call subroutine at nnn
        """
        self.stack[self.sp] = self.pc
        self.sp += 1
        self.pc = self.nnn

    # 3XNN TESTED
    def skip_equal(self):
        """
        skip next instruction if vX = NN
        """
        if self.regs[self.vxi] == self.nn:
            self.pc += 2

    # 4XNN TESTED
    def skip_not_equal(self):
        """
        skip next instruction if vX != NN
        """
        if self.regs[self.vxi] != self.nn:
            self.pc += 2

    # 5XY0 TESTED
    def skip_equal_reg(self):
        """
        skip next instruction if vX = vY
        """
        if self.regs[self.vxi] == self.regs[self.vyi]:
            self.pc += 2

    # 6XNN TESTED
    def load_reg(self):
        """
        set vX = NN
        """
        self.regs[self.vxi] = self.nn

    # 7XNN TESTED
    def add_constant(self):
        """
        set vX = vX + NN
        """
        val = self.regs[self.vxi] + self.nn
        self.regs[self.vxi] = val & 0xFF

    # 8XY0 TESTED
    def set_reg(self):
        """
        set vX to the value of vY
        """
        self.regs[self.vxi] = self.regs[self.vyi]

    # 8XY1 TESTED
    def bitwise_or(self):
        """
        set vX = vX OR vY
        """
        self.regs[self.vxi] = self.regs[self.vxi] | self.regs[self.vyi]

    # 8XY2 TESTED
    def bitwise_and(self):
        """
        set vX = vX AND vY
        """
        self.regs[self.vxi] = self.regs[self.vxi] & self.regs[self.vyi]

    # 8XY3 TESTED
    def bitwise_xor(self):
        """
        set vX = vX XOR vY
        """
        self.regs[self.vxi] = self.regs[self.vxi] ^ self.regs[self.vyi]

    # 8XY4 TESTED
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

    # 8XY5 TESTED
    def sub(self):
        """
        set vF = 1 if vX > vY, set vX = vX - vY
        """
        val_0 = self.regs[self.vxi]
        val_1 = self.regs[self.vxi] - self.regs[self.vyi]
        self.regs[self.vxi] = val_1 & 0xFF

        if val_0 >= self.regs[self.vyi]:
            self.regs[0xF] = 0x1
        else:
            self.regs[0xF] = 0x0

    # 8XY6 TESTED
    def shr(self):
        """
        set vX = vY
        if the least-significant bit of vX is 1, then vF = 1
        shift vX one bit to the right
        """
        # self.regs[self.vxi] = self.regs[self.vyi]

        val = self.regs[self.vxi]
        self.regs[self.vxi] = (self.regs[self.vxi] >> 1) & 0xFF
        self.regs[0xF] = val & 0x1

    # 8XY7 TESTED
    def subn(self):
        """
        set vF = 1 if vY > vX, set vX = vY - vX
        """
        val = self.regs[self.vyi] - self.regs[self.vxi]
        self.regs[self.vxi] = val & 0xFF

        if self.regs[self.vyi] > self.regs[self.vxi]:
            self.regs[0xF] = 0x1
        else:
            self.regs[0xF] = 0x0

    # 8XYE TESTED
    def shl(self):
        """
        set vX = vY
        if the most-significant bit of vX is 1, then vF = 1
        shift vX one bit to the left
        """
        # self.regs[self.vxi] = self.regs[self.vyi]

        val = self.regs[self.vxi]
        self.regs[self.vxi] = (self.regs[self.vxi] << 1) & 0xFF
        self.regs[0xF] = (val & 0x80) >> 7

    # 9XY0 TESTED
    def skip_reg_not_equal(self):
        """
        skip next instruction if vX != vY
        """
        if self.regs[self.vxi] != self.regs[self.vyi]:
            self.pc += 2

    # ANNN TESTED
    def load_index(self):
        """
        set I to NNN
        """
        self.index = self.nnn

    # BNNN
    def jump(self):
        """
        jump to address NNN + v0
        """
        self.pc = self.regs[0] + self.nnn

    # CXNN
    def random_value(self):
        """
        set vX to a random value masked (bitwise AND) with NN
        """
        result = random.randint(0, 255) & self.nn
        self.regs[self.vxi] = result

    # DXYN TESTED
    def draw(self):
        """
        draw 8xN pixel sprite at position vX, vY
        with data starting at the address in I
        set vF = collision
        """
        x = self.vxi
        x_pos = self.regs[x] % 64
        y = self.vyi
        y_pos = self.regs[y] % 32
        height = self.n
        self.regs[0xF] = 0

        for row in range(0, height):
            pixel = self.memory[self.index + row]

            for col in range(0, 8):
                if (pixel & (0x80 >> col)) != 0:
                    pix = x_pos + col + ((y_pos + row) * 64)
                    print('>>>>>>>>', pix % 2048)

                    if self.gfx[pix % 2048] == 1:
                        self.regs[0xF] = 1

                    self.gfx[pix % 2048] ^= 1

        self.draw_flag = True

    # EX9E
    def skip_key_pressed(self):
        """
        skip next instruction if key with the value of vX is pressed
        """
        if self.keys[self.regs[self.vxi]] == 1:
            self.pc += 2

    # EXA1
    def skip_key_not_pressed(self):
        """
        skip next instruction if key with the value of vX is not pressed
        """
        if self.keys[self.regs[self.vxi]] == 0:
            self.pc += 2

    # FX07
    def load_delay(self):
        """
        set vX = delay timer value
        """
        self.regs[self.vxi] = self.delay_timer & 0xFF

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
        self.delay_timer = self.regs[self.vxi] & 0xFF

    # FX18
    def set_sound(self):
        """
        set sound timer value = vX
        """
        self.sound_timer = self.regs[self.vxi] & 0xFF

    # FX1E TESTED
    def add_index(self):
        """
        set I = I + vX
        """
        self.index = self.index + self.regs[self.vxi]

    # FX29
    def load_hex_sprite(self):
        """
        set I = location of sprite for digit vX
        """

    # FX33 TESTED
    def store_bcd(self):
        """
        store BCD representation of vX in memory locations I, I+1, and I+2
        """
        hundred = self.regs[self.vxi] // 100 % 10
        ten = self.regs[self.vxi] // 10 % 10
        one = self.regs[self.vxi] % 10

        self.memory[self.index] = hundred
        self.memory[self.index + 1] = ten
        self.memory[self.index + 2] = one

    # FX55 TESTED
    def store_regs(self):
        """
        store registers v0 through vX in memory starting at location I
        """
        for i in range(self.vxi + 1):
            self.memory[self.index + i] = self.regs[i]

    # FX65 TESTED
    def read_regs(self):
        """
        read registers v0 through vX from memory starting at location I
        """
        for i in range(self.vxi + 1):
            self.regs[i] = self.memory[self.index + i]


class DecodeError(Exception):
    """
    use when the opcode can not be decoded
    """
    def __init__(self, message):
        self.message = f'opcode could not be decoded: {message}'

    def __str__(self):
        return self.message
