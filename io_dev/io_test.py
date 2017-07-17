#!/usr/bin/python2

import curses
import time
import sys

import sgfc_io


def test_io():
    io_dev = sgfc_io.get_device('pic18f45k50', sgfc_io.I2C)
    # io_dev = sgfc_io.get_device('pic18f45k50')

    control_method = io_dev.set_all_pwm

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
            if ch == 'q':
                print("FRONT LEFT")
                control_method = io_dev.set_front_left_pwm
            if ch == 'e':
                print("FRONT RIGHT")
                control_method = io_dev.set_front_right_pwm
            if ch == 'a':
                print("BACK LEFT")
                control_method = io_dev.set_back_left_pwm
            if ch == 'd':
                print("BACK RIGHT")
                control_method = io_dev.set_back_right_pwm
            if ch == 's':
                print("ALL")
                control_method = io_dev.set_all_pwm
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
                control_method(int(ch) / 10.0)
            elif ch == "-":
                control_method(1.0)
            window.addnstr(0, 0, ch + '\n', curses.A_NORMAL)
    except KeyboardInterrupt:
        pass
    finally:
        curses.resetty()
        curses.endwin()
        io_dev.set_all_pwm(0.0)
        io_dev.close()

if __name__ == '__main__':
    test_io()
