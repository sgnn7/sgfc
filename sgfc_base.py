#!/usr/bin/env python2

import sys

import sgfc_communication
import sgfc_control


class SgfcBase(object):
    def __init__(self):
        self._controller = None
        self._comm_device = None

    def _comm_callback(self, data):
        print(data)

    def _comm_error_callback(self, error):
        print("Comm error callback");
        print(error)


    def _exit_gracefully(self):
        print("Exit requested")
        if self._controller:
            self._controller.close()

        if self._comm_device:
            self._comm_device.close()

        sys.exit()

    def _controller_callback(self, data):
        print(data)
        try:
            self._comm_device.send_control_update('\x00\02', data)
        except KeyboardInterrupt as kbi:
            self._exit_gracefully()

    def activate(self):
        self._comm_device = sgfc_communication.get_device('zigbee_xbee',
                                                          '\x00\x01',
                                                          self._comm_callback,
                                                          self._comm_error_callback,
                                                          device='/dev/ttyUSB0')

        try:
            self._controller = sgfc_control.get_device('steam_controller',
                                                       self._controller_callback)
            self._controller.run()
        except KeyboardInterrupt as kbi:
            pass
        finally:
            self._exit_gracefully()

if __name__ == '__main__':
    SgfcBase().activate()
