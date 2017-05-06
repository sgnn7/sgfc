#!/usr/bin/python2

import time
import sgfc_io


def test_io():
    io_dev = sgfc_io.get_device('pic18f45k50')

    try:
        for index in range(0, 100):
            io_dev.set_front_left_pwm(index / 100.0)
            time.sleep(0.01)

        for index in range(100, 0, -1):
            io_dev.set_front_left_pwm(index / 100.0)
            time.sleep(0.01)

        time.sleep(3)

        for index in range(0, 100):
            io_dev.set_front_left_pwm(index / 100.0)
            time.sleep(0.01)

        for index in range(100, 0, -1):
            io_dev.set_front_left_pwm(index / 100.0)
            time.sleep(0.01)

        time.sleep(3)

        io_dev.set_front_left_pwm(0.5)
        time.sleep(10)
    finally:
        io_dev.set_front_left_pwm(0.0)
        io_dev.close()

if __name__ == '__main__':
    test_io()
