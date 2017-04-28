#!/usr/bin/env python2

import argparse
import random
import time
import serial
import uuid

from xbee import XBee

SERIAL_TIMEOUT = 5.0
POLLING_DELAY = 5.0

CHUNK_SIZE = 16

class CommDevice(object):
    def __init__(self, dev_name, network_id='\x12\x23'):
        self._dev_name = dev_name
        self._network_id = network_id

        print("Device: %s" % (dev_name,))
        print("Network ID: %s" % self._to_hex(network_id))
        self._dev_serial = serial.Serial(dev_name, 9600, timeout=SERIAL_TIMEOUT)

        print("Entering command mode...")
        self.exec_at(b'+++', newline=False)

        # Set API mode
        self.exec_at(b'ATAP 1')

        # Set PAN
        self.exec_at(b'ATID %s' % self._to_hex(network_id, delimit=False))

        # Check PAN
        self.exec_at(b'ATID')

        # Apply changes
        self.exec_at(b'ATAC')

        # Exit command mode
        self.exec_at(b'ATCN')

    def wait_for_at_ack(self, debug=False):
        response = ''
        if debug:
            print("- ACK wait...")

        while True:
            if len(response) > 0 and response[-1] == '\r':
                break

            char = self._dev_serial.read(1)
            if not char:
                raise RuntimeError("Could not read response!")

            if debug:
                print(self._to_hex(char))

            response += char

        print("- " + response[:-1])

        if response == 'ERROR\r':
            raise RuntimeError("Error response!")

        print('')

    def _to_hex(self, data, delimit=True):
        delimiter = ' '
        prefix = '0x'

        if not delimit:
            delimiter = ''
            prefix = ''

        return delimiter.join([prefix + "{:02x}".format(ord(char)).upper() for char in data])

    def exec_at(self, command, newline=True, debug=False):
        if newline:
            command += '\r'

        print("Sending: %s" % (command,))
        if debug:
            print("Sending: %s" % (self._to_hex(command)))

        self._dev_serial.write(command)
        self.wait_for_at_ack()

    def send(self, debug=True):
        xbee = XBee(self._dev_serial) #, error_callback=err_cb)

        print("Querying ATID")

        frame_id = "%c" % random.randint(0, 255)
        print("- Frame: %s" % self._to_hex(frame_id))

        xbee.at(frame_id=frame_id, command='ID')

        response = xbee.wait_read_frame()
        print("- Response: %s" % response)

        xbee.halt()
        self._dev_serial.close()

if __name__ == '__main__':
    # TODO: argparse the device
    CommDevice('/dev/ttyUSB0', network_id='\xab\xcd').send()
