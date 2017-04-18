#!/usr/bin/env python2

import time
import serial

from pynmea2 import NMEAStreamReader


SERIAL_TIMEOUT = 5.0
POLLING_DELAY = 5.0

CHUNK_SIZE = 16


def read_gps(dev_serial):
    com = None
    reader = NMEAStreamReader()

    while True:
        if not com:
          try:
            com = serial.Serial(dev_serial, timeout=SERIAL_TIMEOUT)
          except serial.SerialException:
            print('Timed out connecting to %s. Waiting %ss...' % (dev_serial, SERIAL_TIMEOUT))
            time.sleep(POLLING_DELAY)
            continue

        data = com.read(CHUNK_SIZE)
        for msg in reader.next(data):
            print(msg)

read_gps('something')
