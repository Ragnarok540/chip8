import pygame
from chip8 import Chip8

c8 = Chip8()
c8.load_rom('6-keypad.ch8')

pygame.init()
screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()
running = True
dt = 0

while running:
    c8.emulate_cycle()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    c8.keys[0x0] = keys[pygame.K_0]
    c8.keys[0x1] = keys[pygame.K_1]
    c8.keys[0x2] = keys[pygame.K_2]
    c8.keys[0x3] = keys[pygame.K_3]
    c8.keys[0x4] = keys[pygame.K_4]
    c8.keys[0x5] = keys[pygame.K_5]
    c8.keys[0x6] = keys[pygame.K_6]
    c8.keys[0x7] = keys[pygame.K_7]
    c8.keys[0x8] = keys[pygame.K_8]
    c8.keys[0x9] = keys[pygame.K_9]
    c8.keys[0xA] = keys[pygame.K_a]
    c8.keys[0xB] = keys[pygame.K_b]
    c8.keys[0xC] = keys[pygame.K_c]
    c8.keys[0xD] = keys[pygame.K_d]
    c8.keys[0xE] = keys[pygame.K_e]
    c8.keys[0xF] = keys[pygame.K_f]

    if c8.draw_flag:
        screen.fill("black")

        for y in range(0, 32):
            for x in range(0, 64):
                if c8.gfx[x + y * 64]:
                    pygame.draw.rect(screen,
                                     "white",
                                     pygame.Rect(x * 10, y * 10, 10, 10),
                                     0)

        pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
