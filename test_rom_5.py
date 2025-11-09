from src.chip8 import Chip8

c8 = Chip8()
c8.load_rom('5-quirks.ch8')
c8.memory[0x1FF] = 1

for _ in range(0, 6410):
    c8.emulate_cycle()

c8.draw_console()
