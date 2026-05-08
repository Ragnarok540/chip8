from chip8 import Chip8
import curses
from curses import wrapper
from curses.textpad import rectangle
from time import sleep


def draw_curses(stdscr, color, chip8):
    for y in range(0, 32):
        for x in range(0, 64):
            if chip8.gfx[x + y * 64]:
                stdscr.addstr(7 + y, 1 + x, '█', color)
            else:
                stdscr.addstr(7 + y, 1 + x, ' ', color)


def main(stdscr):
    cycles_per_frame = 10
    c8 = Chip8()
    # c8.load_rom('1-chip8-logo.ch8')
    # c8.load_rom('2-ibm-logo.ch8')
    # c8.load_rom('3-corax+.ch8')
    # c8.load_rom('4-flags.ch8')
    c8.load_rom('6-keypad.ch8')

    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_AND_BLACK = curses.color_pair(1)

    stdscr.nodelay(True)

    y = 32 + 1
    x = 64 + 1

    while True:
        for _ in range(cycles_per_frame):
            c8.emulate_cycle()

        try:
            key = stdscr.getkey()
        except Exception:
            key = None
            # c8.keys = [0] * 16

        if key:
            stdscr.clear()

            rectangle(stdscr, 0, 0, 5, 8)
            rectangle(stdscr, 6, 0, y + 6, x)

            if key == '1':
                c8.keys[0x1] = 1
                stdscr.addstr(1, 1, '1', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0x1] = 0
                stdscr.addstr(1, 1, '1', GREEN_AND_BLACK | curses.A_DIM)

            if key == '2':
                c8.keys[0x2] = 1
                stdscr.addstr(1, 3, '2', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0x2] = 0
                stdscr.addstr(1, 3, '2', GREEN_AND_BLACK | curses.A_DIM)

            if key == '3':
                c8.keys[0x3] = 1
                stdscr.addstr(1, 5, '3', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0x3] = 0
                stdscr.addstr(1, 5, '3', GREEN_AND_BLACK | curses.A_DIM)

            if key == '4':
                c8.keys[0xC] = 1
                stdscr.addstr(1, 7, 'C', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0xC] = 0
                stdscr.addstr(1, 7, 'C', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'q':
                c8.keys[0x4] = 1
                stdscr.addstr(2, 1, '4', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0x4] = 0
                stdscr.addstr(2, 1, '4', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'w':
                c8.keys[0x5] = 1
                stdscr.addstr(2, 3, '5', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0x5] = 0
                stdscr.addstr(2, 3, '5', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'e':
                c8.keys[0x6] = 1
                stdscr.addstr(2, 5, '6', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0x6] = 0
                stdscr.addstr(2, 5, '6', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'r':
                c8.keys[0xD] = 1
                stdscr.addstr(2, 7, 'D', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0xD] = 0
                stdscr.addstr(2, 7, 'D', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'a':
                c8.keys[0x7] = 1
                stdscr.addstr(3, 1, '7', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0x7] = 0
                stdscr.addstr(3, 1, '7', GREEN_AND_BLACK | curses.A_DIM)

            if key == 's':
                c8.keys[0x8] = 1
                stdscr.addstr(3, 3, '8', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0x8] = 0
                stdscr.addstr(3, 3, '8', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'd':
                c8.keys[0x9] = 1
                stdscr.addstr(3, 5, '9', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0x9] = 0
                stdscr.addstr(3, 5, '9', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'f':
                c8.keys[0xE] = 1
                stdscr.addstr(3, 7, 'E', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0xE] = 0
                stdscr.addstr(3, 7, 'E', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'z':
                c8.keys[0xA] = 1
                stdscr.addstr(4, 1, 'A', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0xA] = 0
                stdscr.addstr(4, 1, 'A', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'x':
                c8.keys[0x0] = 1
                stdscr.addstr(4, 3, '0', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0x0] = 0
                stdscr.addstr(4, 3, '0', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'c':
                c8.keys[0xB] = 1
                stdscr.addstr(4, 5, 'B', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0xB] = 0
                stdscr.addstr(4, 5, 'B', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'v':
                c8.keys[0xF] = 1
                stdscr.addstr(4, 7, 'F', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                c8.keys[0xF] = 0
                stdscr.addstr(4, 7, 'F', GREEN_AND_BLACK | curses.A_DIM)

        draw_curses(stdscr, GREEN_AND_BLACK, c8)
        stdscr.refresh()
        sleep(0.0016)


wrapper(main)
