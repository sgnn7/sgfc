#!/usr/bin/python2

import curses
import time
import sys

import sgfc_io


def test_io():
    io_dev = sgfc_io.get_device('pic18f45k50')

    try:
        window = curses.initscr()
        # window.nodelay(1)
        curses.savetty()
        curses.noecho()

        while True:
            ch = window.getkey()
            if ch == -1:
                time.sleep(0.1)
                continue

            if ch == curses.KEY_ENTER:
                break
            elif ch == "0" or \
                 ch == "1" or \
                 ch == "2" or \
                 ch == "3" or \
                 ch == "4" or \
                 ch == "5" or \
                 ch == "6" or \
                 ch == "7" or \
                 ch == "8" or \
                 ch == "9":
                io_dev.set_front_left_pwm(int(ch) / 10.0)
            elif ch == "-":
                io_dev.set_front_left_pwm(1.0)
            window.addnstr(0, 0, ch + '\n', curses.A_NORMAL)
    except KeyboardInterrupt:
        pass
    finally:
        curses.resetty()
        curses.endwin()
        io_dev.set_front_left_pwm(0.0)
        io_dev.close()

if __name__ == '__main__':
    test_io()
