import sys
import time

from .constants import PIC_REGISTER, PIC_BITS
from .hk_usb_io import *
from .hk_usb_io import close as usb_close

from ..api_interface import IoDeviceApi


class Pic18F45K50IoDevice(IoDeviceApi):
    def __init__(self, debug=False):
        self._debug = debug
        self._usb = init()

        self._pwm = Bunch(PIC_REGISTER)
        self._bit = Bunch(PIC_BITS)

        sfr_set_regbit(self._usb, self._pwm.ANSELD, 5, 0)
        sfr_set_regbit(self._usb, self._pwm.TRISD,  5, dir_input)
        sfr_set_reg(self._usb, self._pwm.CCPTMRS, 0x00)
        sfr_set_reg(self._usb, self._pwm.PR2, 250)
        sfr_set_reg(self._usb, self._pwm.CCP1CON, 0b00001100)
        sfr_set_reg(self._usb, self._pwm.CCPR1L, 0x00)
        sfr_set_reg(self._usb, self._pwm.T2CON, 0b01111101)
        sfr_set_regbit(self._usb, self._pwm.PSTR1CON, 1, 1)
        sfr_set_regbit(self._usb, self._pwm.TRISD,  5, dir_output)
        sfr_set_reg(self._usb, self._pwm.CCPR1L, 0x64)

    def close(self):
        usb_close(self._usb)

    def set_front_left_pwm(self, ratio):
        print("Ratio:", ratio)

        value = int(ratio * 0x7d * 2)
        print("Register:", "0x" + "{:02x}".format(value).upper())

        sfr_set_reg(self._usb, self._pwm.CCPR1L, value)
