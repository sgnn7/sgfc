#!/usr/bin/env python2

import time

from functools import partial

import sgfc_communication
import sgfc_io

from sgfc_communication.protobufs import sgfc_pb2 as fc_proto

class SgfcDrone(object):
    def __init__(self):
        self._throttle = 0.0
        self._yaw = 0.0
        self._pitch = 0.0

    def comm_callback(self, io_dev, data):
        message = fc_proto.FlightMessage()
        message.ParseFromString(data)

        commands = message.payload
        for command in commands:
            if command.type == fc_proto.FLIGHT_CONTROL_COMMAND:
                fc_command = command.flight_control_command
                if fc_command.throttle:
                    throttle = fc_command.throttle
                    if (throttle != self._throttle):
                        print("Throttle: %s" % throttle)
                        self._throttle = throttle
                        io_dev.set_all_pwm(throttle)
                    else:
                        print("WARN: Redundant throttle msg!")
                if fc_command.yaw:
                    yaw = fc_command.yaw
                    if (yaw != self._yaw):
                        print("Yaw: %s" % yaw)
                        self._yaw = yaw
                        # Do something different here
                        io_dev.set_all_pwm(yaw)
                    else:
                        print("WARN: Redundant yaw msg!")
                if fc_command.pitch:
                    pitch = fc_command.pitch
                    if (pitch != self._pitch):
                        print("Pitch: %s" % pitch)
                        self._pitch = pitch
                        # Do something different here
                        io_dev.set_all_pwm(pitch)
                    else:
                        print("WARN: Redundant pitch msg!")

    def comm_error_callback(self, error):
        print(error)

    def open_comms(self):
        comm_device = None
        io_dev = None
        try:
            io_dev = sgfc_io.get_device('pic18f45k50', sgfc_io.I2C)

            io_dev.set_all_pwm(0.0)
            time.sleep(0.2)

            io_dev.set_all_pwm(1.0)
            time.sleep(1)

            io_dev.set_all_pwm(0.1)
            io_dev.set_all_pwm_clamp(lower=0.5)

            comm_device = sgfc_communication.get_device('zigbee_xbee',
                                                        '\x00\x02',
                                                        partial(self.comm_callback, io_dev),
                                                        self.comm_error_callback,
                                                        device='/dev/ttyUSB0')


        except KeyboardInterrupt as kbi:
            if comm_device:
                comm_device.close()

            if io_dev:
                io_dev.set_all_pwm_clamp(lower=0.0)
                io_dev.set_all_pwm(0.0)
                io_dev.close()

if __name__ == '__main__':
    SgfcDrone().open_comms()
