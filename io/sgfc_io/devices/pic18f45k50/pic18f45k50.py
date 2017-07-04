import sys
import time

from .constants import PIC_REGISTER, PIC_BITS
from .hk_usb_io import *
from .hk_usb_io import close as usb_close

from ..api_interface import IoDeviceApi

from .pca9685 import PCA9685, PCA9685_ADDRESS


# Shim for Adafruit / RPi I2C compat
class I2cComm(object):
    def __init__(self, usb, debug=False):
        self._usb = usb
        self._debug = debug

        i2c_init(self._usb)

    def get_i2c_device(self, device_address, *args, **kwargs):
        self._device_addr = device_address
        return self

    def write8(self, addr, value):
        # Clip value to 1 byte
        value = value & 0xFF

        if self._debug:
            print("Writing to %s[%s]: %s" % (hex(self._device_addr),
                                             hex(addr),
                                             hex(value)))

        i2c_start(self._usb, I2C_START_CMD)
        i2c_write(self._usb, (self._device_addr << 1 | I2C_WRITE_CMD))
        while(i2c_slave_ack(self._usb)):
            time.sleep(0.1)

        # Select the register to write to
        i2c_write(self._usb, addr)
        while (i2c_slave_ack(self._usb)):
            time.sleep(0.1)
        # Write the value to the previously selected reg
        i2c_write(self._usb, value)
        while (i2c_slave_ack(self._usb)):
            time.sleep(0.1)
        i2c_stop(self._usb)

    def readU8(self, addr):
        i2c_start(self._usb, I2C_START_CMD)
        i2c_write(self._usb, (self._device_addr << 1 | I2C_WRITE_CMD))
        while (i2c_slave_ack(self._usb)):    # wait for slave ack
            time.sleep(0.1)
        # select the register address to read
        i2c_write(self._usb, addr)
        while (i2c_slave_ack(self._usb)):    # wait for slave ack
            time.sleep(0.1)
        i2c_start(self._usb, I2C_REP_START_CMD)
        i2c_write(self._usb, (self._device_addr << 1 | I2C_READ_CMD))
        # read the value from the register
        while (i2c_slave_ack(self._usb)):    # wait for slave ack
            time.sleep(0.1)
        ret_val = i2c_read(self._usb)
        # ack the byte
        i2c_master_ack(self._usb, I2C_DATA_NOACK)
        i2c_stop(self._usb)
        return ret_val


class Pic18F45K50IoDevice(IoDeviceApi):
    PWM_FREQUENCY = 500

    def __init__(self, flags=0x0, debug=False):
        self._debug = debug
        self._usb = init()

        self._using_i2c = flags and ((flags | IoDeviceApi.I2C) == IoDeviceApi.I2C)
        if self._using_i2c:
            print("Using I2C mode")
            self._i2c = I2cComm(self._usb)
            self._pca9685 = PCA9685(i2c=self._i2c)
            self._pca9685.set_pwm_freq(Pic18F45K50IoDevice.PWM_FREQUENCY)

    def close(self):
        usb_close(self._usb)

    def _set_channel_pwm(self, channel, ratio):
        print("Ratio:", ratio)
        off_at=int(4095 * ratio)
        self._pca9685.set_pwm(channel, 0x00, off_at)

    def set_front_left_pwm(self, ratio):
        if self._using_i2c:
            self._set_channel_pwm(1, ratio)

    def set_front_right_pwm(self, ratio):
        if self._using_i2c:
            self._set_channel_pwm(2, ratio)

    def set_back_left_pwm(self, ratio):
        if self._using_i2c:
            self._set_channel_pwm(0, ratio)

    def set_back_right_pwm(self, ratio):
        if self._using_i2c:
            self._set_channel_pwm(3, ratio)
