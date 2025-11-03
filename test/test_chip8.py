import unittest

from src.chip8 import Chip8


class Chip8Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # 2NNN 00EE
    def test_call_ret(self):
        """
        call subroutine at NNN
        return from a subroutine
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x23
        c8.memory[c8.pc + 1] = 0x00
        c8.emulate_cycle()
        observed = c8.sp
        self.assertEqual(1, observed)
        observed = c8.stack[c8.sp - 1]
        self.assertEqual(0x200, observed)
        observed = c8.pc
        self.assertEqual(0x300, observed)
        c8.memory[c8.pc] = 0x00
        c8.memory[c8.pc + 1] = 0xEE
        c8.emulate_cycle()
        observed = c8.pc
        self.assertEqual(0x0200, observed)

    # 1NNN
    def test_goto(self):
        """
        jump to location NNN
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x16
        c8.memory[c8.pc + 1] = 0x66
        c8.emulate_cycle()
        observed = c8.pc
        self.assertEqual(0x0666, observed)

    # 3XNN
    def test_skip_equal(self):
        """
        skip next instruction if vX = NN
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x30
        c8.memory[c8.pc + 1] = 0xFF
        c8.regs[0] = 0xFF
        c8.emulate_cycle()
        observed = c8.pc
        self.assertEqual(0x0204, observed)

    # 4XNN
    def test_skip_not_equal(self):
        """
        skip next instruction if vX != NN
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x40
        c8.memory[c8.pc + 1] = 0xFF
        c8.regs[0] = 0x00
        c8.emulate_cycle()
        observed = c8.pc
        self.assertEqual(0x0204, observed)

    # 5XY0
    def test_skip_equal_reg(self):
        """
        skip next instruction if vX = vY
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x50
        c8.memory[c8.pc + 1] = 0x10
        c8.regs[0] = 0xFF
        c8.regs[1] = 0xFF
        c8.emulate_cycle()
        observed = c8.pc
        self.assertEqual(0x0204, observed)

    # 6XNN
    def test_load_register(self):
        """
        set vX = NN
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x60
        c8.memory[c8.pc + 1] = 0xFF
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0xFF, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 7XNN
    def test_add_constant(self):
        """
        set vX = vX + NN
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x70
        c8.memory[c8.pc + 1] = 0x01
        c8.regs[0] = 0x01
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0x02, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 8XY0
    def test_set_register(self):
        """
        set vX to the value of vY
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x80
        c8.memory[c8.pc + 1] = 0x10
        c8.regs[1] = 0xFF
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0xFF, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 8XY1
    def test_bitwise_or(self):
        """
        set vX = vX OR vY
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x80
        c8.memory[c8.pc + 1] = 0x11
        c8.regs[0] = 0x12
        c8.regs[1] = 0x34
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0x36, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 8XY2
    def test_bitwise_and(self):
        """
        set vX = vX AND vY
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x80
        c8.memory[c8.pc + 1] = 0x12
        c8.regs[0] = 0x12
        c8.regs[1] = 0x34
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0x10, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 8XY3
    def test_bitwise_xor(self):
        """
        set vX = vX XOR vY
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x80
        c8.memory[c8.pc + 1] = 0x13
        c8.regs[0] = 0x12
        c8.regs[1] = 0x34
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0x26, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 8XY4
    def test_add(self):
        """
        set vX = vX + vY, set vF = 1 if vX > 255
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x80
        c8.memory[c8.pc + 1] = 0x14
        c8.regs[0] = 0xFF
        c8.regs[1] = 0xFF
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0xFE, observed)
        observed = c8.regs[0xF]
        self.assertEqual(1, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 8XY5
    def test_sub(self):
        """
        set vF = 1 if vX > vY, set vX = vX - vY
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x80
        c8.memory[c8.pc + 1] = 0x15
        c8.regs[0] = 0xFF
        c8.regs[1] = 0xEE
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0x11, observed)
        observed = c8.regs[0xF]
        self.assertEqual(1, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 8XY6
    def test_shr(self):
        """
        set vX = vY
        if the least-significant bit of vX is 1, then vF = 1
        shift vX one bit to the right
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x80
        c8.memory[c8.pc + 1] = 0x16
        c8.regs[0] = 0x00
        c8.regs[1] = 0xFF
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0x7F, observed)
        observed = c8.regs[0xF]
        self.assertEqual(1, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 8XY7
    def test_subn(self):
        """
        set vF = 1 if vY > vX, set vX = vY - vX
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x80
        c8.memory[c8.pc + 1] = 0x17
        c8.regs[0] = 0xEE
        c8.regs[1] = 0xFF
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0x11, observed)
        observed = c8.regs[0xF]
        self.assertEqual(1, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 8XYE
    def test_shl(self):
        """
        set vX = vY
        if the most-significant bit of vX is 1, then vF = 1
        shift vX one bit to the left
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x80
        c8.memory[c8.pc + 1] = 0x1E
        c8.regs[0] = 0x00
        c8.regs[1] = 0x11
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0x22, observed)
        observed = c8.regs[0xF]
        self.assertEqual(0, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 9XY0
    def test_skip_reg_not_equal(self):
        """
        skip next instruction if vX != vY
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x90
        c8.memory[c8.pc + 1] = 0x10
        c8.regs[0] = 0xFF
        c8.regs[1] = 0xFE
        c8.emulate_cycle()
        observed = c8.pc
        self.assertEqual(0x0204, observed)

    # ANNN
    def test_load_index(self):
        """
        set I to NNN
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0xA2
        c8.memory[c8.pc + 1] = 0xF0
        c8.emulate_cycle()
        observed = c8.index
        self.assertEqual(0x2F0, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # BNNN
    def test_jump(self):
        """
        jump to address NNN + v0
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0xB6
        c8.memory[c8.pc + 1] = 0x65
        c8.regs[0] = 0x01
        c8.emulate_cycle()
        observed = c8.pc
        self.assertEqual(0x0666, observed)

    # CXNN
    def test_random_value(self):
        """
        set vX to a random value masked (bitwise AND) with NN
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0xC0
        c8.memory[c8.pc + 1] = 0xFF
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertGreaterEqual(255, observed)
        self.assertLessEqual(0, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # EX9E
    def test_skip_key_pressed(self):
        """
        skip next instruction if key with the value of vX is pressed
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0xE0
        c8.memory[c8.pc + 1] = 0x9E
        c8.regs[0] = 0x1
        c8.keys[1] = 0x1
        c8.emulate_cycle()
        observed = c8.pc
        self.assertEqual(0x0204, observed)
