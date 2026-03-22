import curses
from curses import wrapper
from curses.textpad import rectangle


def main(stdscr):
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_AND_BLACK = curses.color_pair(1)

    stdscr.nodelay(True)

    y = 32
    x = 64

    # counter_win = curses.newwin(6, 0, y + 6, x)

    while True:
        try:
            key = stdscr.getkey()
        except Exception:
            key = None

        if key:
            stdscr.clear()

            rectangle(stdscr, 0, 0, 5, 8)
            rectangle(stdscr, 6, 0, y + 6, x)

            if key == '1':
                stdscr.addstr(1, 1, '1', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(1, 1, '1', GREEN_AND_BLACK | curses.A_DIM)

            if key == '2':
                stdscr.addstr(1, 3, '2', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(1, 3, '2', GREEN_AND_BLACK | curses.A_DIM)

            if key == '3':
                stdscr.addstr(1, 5, '3', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(1, 5, '3', GREEN_AND_BLACK | curses.A_DIM)

            if key == '4':
                stdscr.addstr(1, 7, 'C', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(1, 7, 'C', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'q':
                stdscr.addstr(2, 1, '4', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(2, 1, '4', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'w':
                stdscr.addstr(2, 3, '5', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(2, 3, '5', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'e':
                stdscr.addstr(2, 5, '6', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(2, 5, '6', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'r':
                stdscr.addstr(2, 7, 'D', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(2, 7, 'D', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'a':
                stdscr.addstr(3, 1, '7', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(3, 1, '7', GREEN_AND_BLACK | curses.A_DIM)

            if key == 's':
                stdscr.addstr(3, 3, '8', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(3, 3, '8', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'd':
                stdscr.addstr(3, 5, '9', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(3, 5, '9', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'f':
                stdscr.addstr(3, 7, 'E', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(3, 7, 'E', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'z':
                stdscr.addstr(4, 1, 'A', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(4, 1, 'A', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'x':
                stdscr.addstr(4, 3, '0', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(4, 3, '0', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'c':
                stdscr.addstr(4, 5, 'B', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(4, 5, 'B', GREEN_AND_BLACK | curses.A_DIM)

            if key == 'v':
                stdscr.addstr(4, 7, 'F', GREEN_AND_BLACK | curses.A_BOLD)
            else:
                stdscr.addstr(4, 7, 'F', GREEN_AND_BLACK | curses.A_DIM)

            stdscr.refresh()


wrapper(main)
