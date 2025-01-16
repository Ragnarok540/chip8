import random

class Chip8:
    def __init__(self):
        self.opcode = 0
        self.memory = [0] * 4096
        self.graphics = [0] * 2048
        self.registers = [0] * 16
        self.index = 0
        self.program_counter = 0x0200

        self.delay_timer = 0
        self.sound_timer = 0
        
        self.stack = [0] * 16
        self.stack_pointer = 0
        
        self.keys = [0] * 16

    def emulate_cycle(self):
        self.fetch_opcode()
        self.decode_opcode()
        # update timers

    def fetch_opcode(self):
        pc = self.program_counter
        self.opcode = self.memory[pc] << 8 | self.memory[pc + 1]

    def decode_opcode(self):
        branch = self.opcode & 0xF000

        if branch == 0x0000:
            branch = self.opcode & 0x000F

            if branch == 0x000E:
                self.ret()
                return

        if branch == 0x1000:
            self.goto()
            return

        if branch == 0x2000:
            self.call()
            return

        if branch == 0x3000:
            self.skip_equal()
            return

        if branch == 0x4000:
            self.skip_not_equal()
            return

        if branch == 0x5000:
            self.skip_equal_reg()
            return

        if branch == 0x6000:
            self.load_register()
            return

        if branch == 0x7000:
            self.add_constant()
            return

        if branch == 0x8000:
            branch = self.opcode & 0x000F

            if branch == 0x0000:
                self.set_register()
                return

        if branch == 0xA000:
            self.load_index()
            return

        if branch == 0xB000:
            self.jump()
            return

        if branch == 0xC000:
            self.random_value()
            return

        raise Exception(f'opcode could not be decoded: {hex(self.opcode)}')

    # 00EE
    def ret(self):
        self.stack_pointer -= 1
        self.program_counter = self.stack[self.stack_pointer]

    # 1NNN
    def goto(self):
        self.program_counter = self.opcode & 0x0FFF

    # 2NNN
    def call(self):
        self.stack[self.stack_pointer] = self.program_counter
        self.stack_pointer += 1
        self.program_counter = self.opcode & 0x0FFF

    # 3XKK
    def skip_equal(self):
        vx = self.registers[(self.opcode & 0x0F00) >> 8]

        if vx == (self.opcode & 0x00FF):
            self.program_counter += 4
        else:
            self.program_counter += 2    

    # 4XKK
    def skip_not_equal(self):
        vx = self.registers[(self.opcode & 0x0F00) >> 8]

        if vx != (self.opcode & 0x00FF):
            self.program_counter += 4
        else:
            self.program_counter += 2 

    # 5XY0
    def skip_equal_reg(self):
        vx = self.registers[(self.opcode & 0x0F00) >> 8]
        vy = self.registers[(self.opcode & 0x00F0) >> 4]

        if vx == vy:
            self.program_counter += 4
        else:
            self.program_counter += 2 

    # 6XKK
    def load_register(self):
        self.registers[(self.opcode & 0x0F00) >> 8] = self.opcode & 0x00FF
        self.program_counter += 2

    # 7XKK
    def add_constant(self):
        self.registers[(self.opcode & 0x0F00) >> 8] += self.opcode & 0x00FF
        self.program_counter += 2

    # 8XY0
    def set_register(self):
        self.registers[(self.opcode & 0x0F00) >> 8] = self.registers[(self.opcode & 0x00F0) >> 4]
        self.program_counter += 2

    # ANNN
    def load_index(self):
        self.index = self.opcode & 0x0FFF
        self.program_counter += 2

    # BNNN
    def jump(self):
        v0 = self.registers[0]
        self.program_counter = v0 + (self.opcode & 0x0FFF)

    # CXKK
    def random_value(self):
        result = random.randint(0, 255) & (self.opcode & 0x00FF)
        self.registers[(self.opcode & 0x0F00) >> 8] = result
        self.program_counter += 2


"""

import pygame, sys
from pygame.locals import *
import random
 
pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 
 
      def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
 
      def draw(self, surface):
        surface.blit(self.image, self.rect) 
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
 
    def update(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     
 
         
P1 = Player()
E1 = Enemy()
 
while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()
    E1.move()
     
    DISPLAYSURF.fill(WHITE)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
         
    pygame.display.update()
    FramePerSec.tick(FPS)

"""
