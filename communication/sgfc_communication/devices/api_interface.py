from abc import ABCMeta, abstractmethod

from ..protobufs import sgfc_pb2 as fc_proto

class CommDeviceApiV1(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def tx(self, dest, data):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @staticmethod
    def to_hex(data, delimit=True):
        delimiter = ' '
        prefix = '0x'

        if not delimit:
            delimiter = ''
            prefix = ''

        return delimiter.join([prefix + "{:02x}".format(ord(char)).upper() for char in data])

    def send_control_update(self, dest, data):
        print(data)
        scalar_value = data['scalar']
        scalar_type = data['type']

        fc_message = fc_proto.FlightMessage()

        fc_message.sender = "Me"

        payload = fc_proto.Payload()
        payload.type = fc_proto.FLIGHT_CONTROL_COMMAND

        setattr(payload.flight_control_command, scalar_type.lower(), scalar_value)

        fc_message.payload.extend([payload])
        print(fc_message)

        self.tx(dest, fc_message.SerializeToString())

class CommDeviceApi(CommDeviceApiV1):
    pass
