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

    # 3XKK
    def test_skip_equal(self):
        """
        skip next instruction if vX = KK
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x30
        c8.memory[c8.pc + 1] = 0xFF
        c8.regs[0] = 0xFF
        c8.emulate_cycle()
        observed = c8.pc
        self.assertEqual(0x0204, observed)

    # 4XKK
    def test_skip_not_equal(self):
        """
        skip next instruction if vX != KK
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

    # 6XKK
    def test_load_register(self):
        """
        set vX = KK
        """
        c8 = Chip8()
        c8.memory[c8.pc] = 0x60
        c8.memory[c8.pc + 1] = 0xFF
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertEqual(0xFF, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    # 7XKK
    def test_add_constant(self):
        """
        set vX = vX + KK
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

    # CXKK
    def test_random_value(self):
        """
        set vX to a random value masked (bitwise AND) with KK
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
