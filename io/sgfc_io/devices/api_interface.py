from abc import ABCMeta, abstractmethod

class IoDeviceApiV1(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def close(self):
        raise NotImplementedError()

    @abstractmethod
    def set_front_left_pwm(self, ratio):
        raise NotImplementedError()

    def set_front_right_pwm(self, ratio):
        raise NotImplementedError()

    def set_back_left_pwm(self, ratio):
        raise NotImplementedError()

    def set_back_right_pwm(self, ratio):
        raise NotImplementedError()

    def set_all_pwm(self, ratio):
        self.set_front_left_pwm(ratio)
        self.set_front_right_pwm(ratio)
        self.set_back_left_pwm(ratio)
        self.set_back_right_pwm(ratio)

class IoDeviceApi(IoDeviceApiV1):
    I2C = 0b00000001
