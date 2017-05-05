#!/usr/bin/env python2

import sgfc_communication
import sgfc_control


def comm_callback(data):
    print(data)

def comm_error_callback(error):
    print(error)

comm_device = sgfc_communication.get_device('zigbee_xbee',
                                            comm_callback,
                                            comm_error_callback,
                                            device='/dev/ttyUSB0')

def controller_callback(data):
    print(data)
    comm_device.send_control_update('\x00\02', data)


controller = None
try:
    controller = sgfc_control.get_device('steam_controller',
                                         controller_callback)
    controller.run()
except KeyboardInterrupt as kbi:
    controller.close()
    comm_device.close()
