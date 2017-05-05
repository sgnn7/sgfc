#!/usr/bin/env python2

import time

from devices.zigbee_xbee import XBeeCommDevice
from protobufs import sgfc_pb2 as fc_proto


def test_comms():
    dev1 = None
    dev2 = None

    fc_message = fc_proto.FlightMessage()

    fc_message.sender = "Me"

    payload = fc_proto.Payload()
    payload.type = fc_proto.GPS_POSITION

    payload.gps_position.has_fix = False
    payload.gps_position.latitude = 1.1111
    payload.gps_position.longitude = 22.222
    payload.gps_position.altitude = 333.33
    payload.gps_position.speed = 4444.4

    fc_message.payload.extend([payload])

    print(fc_message)

    def callback(data):
        print("Client got a message!")
        proto_message = fc_proto.FlightMessage()
        proto_message.ParseFromString(data)
        print("Size: %d bytes" % (len(data),))
        print('=' * 40)
        print(proto_message)
        print('=' * 40)


    def error_callback(error):
        print("Client got error: %s" % (error,))

    # TODO: argparse the device
    try:
        dev1 = XBeeCommDevice('/dev/ttyUSB0', '\x00\x01',
                              callback=callback,
                              error_callback=error_callback,
                              network_id='\xab\xcd')

        dev2 = XBeeCommDevice('/dev/ttyUSB1', '\x00\x02',
                              callback=callback,
                              error_callback=error_callback,
                              network_id='\xab\xcd')

        print('')

        dev2.tx('\x00\x01', fc_message.SerializeToString())

        time.sleep(1)
        print('')

        dev1.tx('\x00\x02', fc_message.SerializeToString())

        time.sleep(1)

        print('')
        print("Testing high-speed transfer")
        serialized_message = fc_message.SerializeToString()
        start = time.time()
        for index in range(100):
            dev1.tx('\x00\x02', serialized_message)
            dev2.tx('\x00\x02', serialized_message)
        end = time.time()

        time.sleep(1)

        print("Elapsed: %.2fs" % (end - start,))

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
