#!/usr/bin/env python2

import time

import sgfc_communication

from sgfc_communication.protobufs import sgfc_pb2 as fc_proto


def comm_callback(data):
    message = fc_proto.FlightMessage()
    message.ParseFromString(data)
    print(message)

def comm_error_callback(error):
    print(error)

def open_comms():
    comm_device = None
    try:
        comm_device = sgfc_communication.get_device('zigbee_xbee',
                                                    '\x00\x02',
                                                    comm_callback,
                                                    comm_error_callback,
                                                    device='/dev/ttyUSB1')

    except KeyboardInterrupt as kbi:
        if comm_device:
            comm_device.close()

if __name__ == '__main__':
    open_comms()
