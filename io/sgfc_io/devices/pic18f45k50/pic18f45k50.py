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

        # Set all registers RD* and RB* to digital
        sfr_set_regbit(self._usb, self._pwm.ANSELD, 0, 0)

        # Set all RD* and all RB* to output
        sfr_set_regbit(self._usb, self._pwm.TRISD,  0, dir_input)

        # PWM timer selection C/C == TMR1, PWM == TMR2
        sfr_set_reg(self._usb, self._pwm.CCPTMRS, 0x00)

        # CCP PWM mode
        sfr_set_reg(self._usb, self._pwm.CCP1CON, 0b00001100)

        sfr_set_reg(self._usb, self._pwm.PR2, 0xBA)
        sfr_set_reg(self._usb, self._pwm.CCPR1L, 0x00)
        sfr_set_reg(self._usb, self._pwm.T2CON, 0b01111110)

        # Define output
        sfr_set_regbit(self._usb, self._pwm.PSTR1CON, 1, 0b00001111)
        sfr_set_regbit(self._usb, self._pwm.TRISD,  0b00000101, dir_output)

        sfr_set_reg(self._usb, self._pwm.CCPR1L, 0x22)

    def close(self):
        usb_close(self._usb)

    def set_front_left_pwm(self, ratio):
        print("Ratio:", ratio)

        value = int(ratio * 0xBA)
        print("Register:", "0x" + "{:02x}".format(value).upper())

        sfr_set_reg(self._usb, self._pwm.CCPR1L, value)
