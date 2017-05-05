from abc import ABCMeta, abstractmethod

class ControlDeviceApiV1(object):
    __metaclass__ = ABCMeta
    _callback = None

    # Fake enum
    class CONTROL_TYPE:
        LONGITUDINAL = 'LONGITUDINAL'
        LATERAL = 'LATERAL'
        PITCH = 'PITCH'
        ROLL = 'ROLL'
        YAW = 'YAW'
        THROTTLE = 'THROTTLE'

    def _send_callback(self, callback_type, scalar):
        if not self._callback:
            return

        self._callback({ 'type': callback_type,
                         'scalar': scalar })

    def set_longitudinal_scalar(self, scalar, range=1.0, delta_based=False):
        print("Long:", scalar)
        self._send_callback(self.CONTROL_TYPE.LONGITUDINAL, scalar)

    def set_lateral_scalar(self, scalar, range=1.0, delta_based=False):
        print("Lat:", scalar)
        self._send_callback(self.CONTROL_TYPE.LATERAL, scalar)

    def set_pitch_scalar(self, scalar, range=1.0, delta_based=False):
        print("Pitch:", scalar)
        self._send_callback(self.CONTROL_TYPE.PITCH, scalar)

    def set_roll_scalar(self, scalar, range=1.0, delta_based=False):
        print("Roll:", scalar)
        self._send_callback(self.CONTROL_TYPE.ROLL, scalar)

    def set_yaw_scalar(self, scalar, range=1.0, delta_based=False):
        print("Yaw:", scalar)
        self._send_callback(self.CONTROL_TYPE.YAW, scalar)

    def set_throttle_scalar(self, scalar, range=1.0, delta_based=False):
        print("Throttle:", scalar)
        self._send_callback(self.CONTROL_TYPE.THROTTLE, scalar)

    @abstractmethod
    def close(self):
        raise NotImplementedError()

class ControlDeviceApi(ControlDeviceApiV1):
    pass
