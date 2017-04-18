#!/usr/bin/env python2

import time
import serial

from pynmea2 import nmea, NMEAStreamReader


SERIAL_TIMEOUT = 5.0
POLLING_DELAY = 5.0

CHUNK_SIZE = 16


def read_gps(dev_serial, debug=True):
    com = None
    reader = NMEAStreamReader()

    latitude = None
    longitude = None

    while True:
        if not com:
          try:
            com = serial.Serial(dev_serial, timeout=SERIAL_TIMEOUT)
          except serial.SerialException as e:
            print('Timed out connecting to %s (%s). Waiting %ss...' % (dev_serial, e, SERIAL_TIMEOUT))
            time.sleep(POLLING_DELAY)
            continue

        data = com.read(CHUNK_SIZE)

        try:
            for message in reader.next(data):
                # print(message)
                # print(dir(message))
                if message.sentence_type == 'GGA' or message.sentence_type == 'RMC':
                    curr_latitude = message.latitude
                    curr_longitude = message.longitude
                    if curr_latitude == latitude and curr_longitude == longitude:
                        continue

                    latitude = curr_latitude
                    longitude = curr_longitude

                    if latitude == longitude == 0:
                        print("No fix available")
                        continue

                    if debug:
                        for index, field in enumerate(message.data):
                            print('%s: %s' % (message.fields[index], field))

                    # print(dir(message))
                    print('%s, %s' % (message.latitude, message.longitude))
                elif message.sentence_type == 'GSA':
                    # Fix info / DOP
                    # print(dir(message))
                    pass
                elif message.sentence_type == 'GSV':
                    # Sats in view info
                    # print(dir(message))
                    pass
                elif message.sentence_type == 'RMC':
                    # Recommended min GPS/transit data
                    #print(dir(message))
                    pass
                elif message.sentence_type == 'VTG':
                    # Speed
                    if debug:
                        for index, field in enumerate(message.data):
                            print('%s: %s' % (message.fields[index], field))
                else:
                    print(message.sentence_type)
        except nmea.ParseError as pe:
            continue


read_gps('/dev/ttyUSB0')
