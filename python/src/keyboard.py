import curses
from curses import wrapper


def main(stdscr):
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_AND_BLACK = curses.color_pair(1)

    stdscr.nodelay(True)
    keys = []

    while True:
        while True:
            c = stdscr.getch()

            if c == -1:
                # keys = []
                break

            keys.append(c)

        if keys:
            stdscr.clear()

            if 97 in keys:
                stdscr.addstr(1, 1, 'a', GREEN_AND_BLACK | curses.A_BOLD)
            if 115 in keys:
                stdscr.addstr(1, 2, 's', GREEN_AND_BLACK | curses.A_BOLD)

        stdscr.refresh()
        # keys = []


wrapper(main)
