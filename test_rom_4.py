from src.chip8 import Chip8

c8 = Chip8()
c8.load_rom('4-flags.ch8')

for _ in range(0, 960):
    c8.emulate_cycle()

c8.draw_console()
