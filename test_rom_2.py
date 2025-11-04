from src.chip8 import Chip8

c8 = Chip8()
c8.load_rom('2-ibm-logo.ch8')

for _ in range(0, 21):
    c8.emulate_cycle()

c8.draw_console()
