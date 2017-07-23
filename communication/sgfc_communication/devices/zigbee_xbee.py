#!/usr/bin/env python2

import argparse
import random
import time
import serial

from xbee import XBee

from .api_interface import CommDeviceApi

SERIAL_TIMEOUT = 5.0

class ZigbeeXbeeCommDevice(CommDeviceApi):
    def __init__(self, dev_name, id,
                 network_id='\x12\x23',
                 callback=None,
                 error_callback=None,
                 debug=False):
        self._xbee = None
        self._dev_serial = None
        self._debug = debug

        self._dev_name = dev_name
        self._network_id = network_id
        self._tx_responses = {}

        self._client_callback = callback
        self._client_error_callback = error_callback

        print("Device: %s" % (dev_name,))
        print("Network ID: %s" % self.to_hex(network_id))

        # Bump serial speed to 115200 bps if on default
        tmp_dev_serial = None
        try:
            tmp_dev_serial = serial.Serial(dev_name, 9600, timeout=SERIAL_TIMEOUT)
            print("Entering command mode...")
            self.exec_at(b'+++', device=tmp_dev_serial, newline=False)

            # Set speed to 115,200 bps
            self.exec_at(b'ATBD 7', device=tmp_dev_serial)

            # Apply changes
            self.exec_at(b'ATAC', device=tmp_dev_serial)

            time.sleep(0.2)

            # Exit command mode
            self.exec_at(b'ATCN', device=tmp_dev_serial)

            time.sleep(0.1)
        except Exception as e:
            # We intentionally ignore errors here
            pass
        finally:
            if tmp_dev_serial:
                tmp_dev_serial.close()
                tmp_dev_serial = None

        self._dev_serial = serial.Serial(dev_name, 115200, timeout=SERIAL_TIMEOUT)
        print("Entering command mode...")
        self.exec_at(b'+++', newline=False)

        # Set API mode
        self.exec_at(b'ATAP 2')

        # Set PAN
        self.exec_at(b'ATID %s' % self.to_hex(network_id, delimit=False))

        # Check PAN
        self.exec_at(b'ATID')

        self.exec_at(b'ATMY %s' % self.to_hex(id, delimit=False))

        # Apply changes
        self.exec_at(b'ATAC')

        time.sleep(0.2)

        # Exit command mode
        self.exec_at(b'ATCN')

        time.sleep(0.1)

        self._xbee = XBee(self._dev_serial,
                          escaped=True,
                          callback=self._rx_callback,
                          error_callback=self._error_callback)

    def wait_for_at_ack(self, device=None, debug=False):
        response = ''
        device = device or self._dev_serial
        if debug:
            print("- ACK wait...")

        while True:
            if len(response) > 0 and response[-1] == '\r':
                break

            char = device.read(1)
            if not char:
                raise RuntimeError("Could not read response!")

            if debug:
                print(self.to_hex(char))

            response += char

        print("- " + response[:-1])

        if response == 'ERROR\r':
            raise RuntimeError("Error response!")

        print('')

    def exec_at(self, command, device=None, newline=True, debug=False):
        if newline:
            command += '\r'

        print("Sending: %s" % (command,))
        if debug:
            print("Sending: %s" % (self.to_hex(command)))

        device = device or self._dev_serial
        device.write(command)
        self.wait_for_at_ack(device=device, debug=debug)

    def tx(self, dest, data, debug=True):
        frame_id = "%c" % random.randint(1, 255)

        print("- Frame: %s" % self.to_hex(frame_id))
        self._xbee.tx(frame_id=frame_id, dest_addr=dest, data=data)

        # TODO: This is only sync right now - need to do it async somehow 
        #       in a nicer API than the XBee package
        print("- Waiting for response...")
        while not self._got_response_to(frame_id):
            try:
                time.sleep(0.0001)
            except KeyboardInterrupt as kbi:
                raise kbi

        return True

    def _got_response_to(self, frame_id):
        if frame_id in self._tx_responses:
            del self._tx_responses[frame_id]
            return True

        return False

    def _rx_callback(self, data, debug=False):
        if data['id'] == 'tx_status':
            # Receipt for sent packet
            self._tx_responses[data['frame_id']] = True
            return

        if debug:
            print(data)

        payload = data.get('rf_data')

        if self._client_callback:
            self._client_callback(payload)

    def _error_callback(self, error):
        print("ERROR RECEIVED!")
        print(error.message)

        if self._client_error_callback:
            self._client_error_callback(error)

    def close(self):
        if self._xbee:
            self._xbee.halt()
            self._xbee = None

        if self._dev_serial:
            self._dev_serial.close()
            self._dev_serial = None

def test_comms():
    dev1 = None
    dev2 = None

    def callback(data):
        print("Client got: %s" % (data,))

    def error_callback(error):
        print("Client got error: %s" % (error,))

    # TODO: argparse the device
    try:
        dev1 = CommDevice('/dev/ttyUSB0', '\x00\x01',
                          callback=callback,
                          error_callback=error_callback,
                          network_id='\xab\xcd')

        dev2 = CommDevice('/dev/ttyUSB1', '\x00\x02',
                          callback=callback,
                          error_callback=error_callback,
                          network_id='\xab\xcd')

        print('')

        dev2.tx('\x00\x01', "Hello world from #1!")

        time.sleep(1)
        print('')

        dev1.tx('\x00\x02', "Hello world from #2!")

        time.sleep(1)
    except Exception as e:
        print(e)

    print('')
    print("Cleaning up")
    if dev1:
        dev1.close()
    if dev2:
        dev2.close()

    print("Done")


if __name__ == '__main__':
    test_comms()
