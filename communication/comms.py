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
    def __init__(self, dev_name, id, network_id='\x12\x23', debug=False):
        self._xbee = None
        self._dev_serial = None
        self._debug = debug

        self._dev_name = dev_name
        self._network_id = network_id
        self._tx_responses = {}

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

        self.exec_at(b'ATMY %s' % self._to_hex(id, delimit=False))

        # Apply changes
        self.exec_at(b'ATAC')

        time.sleep(0.2)

        # Exit command mode
        self.exec_at(b'ATCN')

        time.sleep(0.1)

        self._xbee = XBee(self._dev_serial, callback=self._rx_callback, error_callback=self._err_callback)

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
        self.wait_for_at_ack(debug)

    def tx(self, dest, debug=True):
        frame_id = "%c" % random.randint(0, 255)

        print("- Frame: %s" % self._to_hex(frame_id))
        self._xbee.tx(frame_id=frame_id, dest_addr=dest, data='Hello World')

        print("- Waiting for response...")
        while not self._got_response_to(frame_id):
            time.sleep(0.0001)

        return True

    def _got_response_to(self, frame_id):
        if frame_id in self._tx_responses:
            del self._tx_responses[frame_id]
            return True

        return False

    def _rx_callback(self, data):
        print("YAY!")
        if data['id'] == 'tx_status':
            self._tx_responses[data['frame_id']] = True
            return

        print(data)

    def _err_callback(self, err):
        print("NOES!")
        print(err.message)
        raise Exception(err)

    def close(self):
        if self._xbee:
            self._xbee.halt()
            self._xbee = None

        if self._dev_serial:
            self._dev_serial.close()
            self._dev_serial = None


if __name__ == '__main__':
    dev1 = None
    dev2 = None

    # TODO: argparse the device
    try:
        dev1 = CommDevice('/dev/ttyUSB0', '\x00\x01', network_id='\xab\xcd')
        dev2 = CommDevice('/dev/ttyUSB1', '\x00\x02', network_id='\xab\xcd')

        dev2.tx(dest='\x00\x01')

        time.sleep(3)

        dev1.tx(dest='\x00\x02')

        time.sleep(1)
    except Exception as e:
        print(e)

    print("Cleaning up")
    if dev1:
        dev1.close()
    if dev2:
        dev2.close()

    print("Done")
