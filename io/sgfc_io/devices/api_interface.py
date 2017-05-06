from abc import ABCMeta, abstractmethod

class IoDeviceApiV1(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def set_front_left_pwm(self, ratio):
        raise NotImplementedError()

class IoDeviceApi(IoDeviceApiV1):
    pass
