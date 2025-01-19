import unittest

from src.chip8 import Chip8


class Chip8Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_index(self):
        c8 = Chip8()
        c8.memory[c8.pc] = 0xA2
        c8.memory[c8.pc + 1] = 0xF0
        c8.emulate_cycle()
        observed = hex(c8.index)
        self.assertEqual('0x2f0', observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    def test_set_register(self):
        c8 = Chip8()
        c8.memory[c8.pc] = 0x80
        c8.memory[c8.pc + 1] = 0x10
        c8.regs[1] = 0xFF
        c8.emulate_cycle()
        observed = hex(c8.regs[0])
        self.assertEqual('0xff', observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)

    def test_random_value(self):
        c8 = Chip8()
        c8.memory[c8.pc] = 0xC0
        c8.memory[c8.pc + 1] = 0xFF
        c8.emulate_cycle()
        observed = c8.regs[0]
        self.assertGreaterEqual(255, observed)
        self.assertLessEqual(0, observed)
        observed = c8.pc
        self.assertEqual(0x0202, observed)
