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
                self.load_register()
            case 0x7000:
                self.add_constant()
            case 0x8000:
                match self.opcode & 0x000F:
                    case 0x0000:
                        self.set_register()
                    case 0x0001:
                        self.bitwise_or()
                    case 0x0002:
                        self.bitwise_and()
                    case 0x0003:
                        self.bitwise_xor()
                    case _:
                        raise DecodeError(hex(self.opcode))
            case 0xA000:
                self.load_index()
            case 0xB000:
                self.jump()
            case 0xC000:
                self.random_value()
            case _:
                raise DecodeError(hex(self.opcode))

    # 00E0
    def clear_screen(self):
        """
        clear the screen
        """
        self.gfx = [0] * 2048

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

    # 3XKK
    def skip_equal(self):
        """
        skip next instruction if vX = KK
        """
        vx = self.regs[(self.opcode & 0x0F00) >> 8]

        if vx == (self.opcode & 0x00FF):
            self.pc += 4
        else:
            self.pc += 2

    # 4XKK
    def skip_not_equal(self):
        """
        skip next instruction if vX != KK
        """
        vx = self.regs[(self.opcode & 0x0F00) >> 8]

        if vx != (self.opcode & 0x00FF):
            self.pc += 4
        else:
            self.pc += 2

    # 5XY0
    def skip_equal_reg(self):
        """
        skip next instruction if vX = vY
        """
        vx = self.regs[(self.opcode & 0x0F00) >> 8]
        vy = self.regs[(self.opcode & 0x00F0) >> 4]

        if vx == vy:
            self.pc += 4
        else:
            self.pc += 2

    # 6XKK
    def load_register(self):
        """
        set vX = KK
        """
        vxi = (self.opcode & 0x0F00) >> 8
        self.regs[vxi] = self.opcode & 0x00FF
        self.pc += 2

    # 7XKK
    def add_constant(self):
        """
        set vX = vX + KK
        """
        vxi = (self.opcode & 0x0F00) >> 8
        self.regs[vxi] += self.opcode & 0x00FF
        self.pc += 2

    # 8XY0
    def set_register(self):
        """
        set vX to the value of vY
        """
        vxi = (self.opcode & 0x0F00) >> 8
        vyi = (self.opcode & 0x00F0) >> 4
        self.regs[vxi] = self.regs[vyi]
        self.pc += 2

    # 8XY1
    def bitwise_or(self):
        """
        set vX = vX OR vY
        """
        vxi = (self.opcode & 0x0F00) >> 8
        vyi = (self.opcode & 0x00F0) >> 4
        self.regs[vxi] = self.regs[vxi] | self.regs[vyi]
        self.pc += 2

    # 8XY2
    def bitwise_and(self):
        """
        set vX = vX AND vY
        """
        vxi = (self.opcode & 0x0F00) >> 8
        vyi = (self.opcode & 0x00F0) >> 4
        self.regs[vxi] = self.regs[vxi] & self.regs[vyi]
        self.pc += 2

    # 8XY3
    def bitwise_xor(self):
        """
        set vX = vX XOR vY
        """
        vxi = (self.opcode & 0x0F00) >> 8
        vyi = (self.opcode & 0x00F0) >> 4
        self.regs[vxi] = self.regs[vxi] ^ self.regs[vyi]
        self.pc += 2

    # ANNN
    def load_index(self):
        """
        set I to NNN
        """
        self.index = self.opcode & 0x0FFF
        self.pc += 2

    # BNNN
    def jump(self):
        v0 = self.regs[0]
        self.pc = v0 + (self.opcode & 0x0FFF)

    # CXKK
    def random_value(self):
        """
        set vX to a random value masked (bitwise AND) with KK
        """
        result = random.randint(0, 255) & (self.opcode & 0x00FF)
        vxi = (self.opcode & 0x0F00) >> 8
        self.regs[vxi] = result
        self.pc += 2


class DecodeError(Exception):
    """
    use when the opcode can not be decoded
    """
    def __init__(self, message):
        self.message = f'opcode could not be decoded: {message}'

    def __str__(self):
        return self.message

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
