#!/usr/bin/env python

import sys
import time

from api_interface import ControlDeviceApi

from steamcontroller import SteamController, SCButtons
from steamcontroller.events import EventMapper, Pos
from steamcontroller.uinput import Keys

class SteamControllerDevice(ControlDeviceApi):
    def __init__(self, callback = None, debug=False):
        self._debug = debug
        self._callback = callback

        evm = self._evminit()
        self._sc = SteamController(callback=evm.process)

    def run(self):
        self._sc.run()

    def close(self):
        if self._sc:
            self._sc.addExit()

    def _evminit(self):
        evm = EventMapper()
        for button in SCButtons:
            evm.setButtonCallback(button, self._button_pressed_callback)

    #   evm.setPadButtonCallback(Pos.LEFT, self._touchpad_touch_callback)
        evm.setPadButtonCallback(Pos.RIGHT, self._touchpad_touch_callback)
    #   evm.setPadButtonCallback(Pos.RIGHT, self._touchpad_click_callback, clicked=True)
        evm.setStickAxesCallback(self._stick_axes_callback)
    #   evm.setStickPressedCallback(self._stick_pressed_callback)
        evm.setTrigAxesCallback(Pos.LEFT, self._trigger_axes_callback)
        evm.setTrigAxesCallback(Pos.RIGHT, self._trigger_axes_callback)

        return evm

    def _button_pressed_callback(self, evm, btn, pressed):
        for button in SCButtons:
            if btn == button:
                print "Pressed", btn, "on" if pressed else "off"

        if btn == SCButtons.STEAM and not pressed:
            close(usb)
            sys.exit()

        if btn == SCButtons.START and pressed:
            for i in range(255, 5):
                set_duty_cycle(i)
                time.sleep(0.001)

            for i in range(255, 0, -5):
                set_duty_cycle(i)
                time.sleep(0.001)

    def _touchpad_click_callback(self, evm, pad, pressed):
        print "Touchpad {} was {}".format(pad, 'pressed' if pressed else 'released')

    def _touchpad_touch_callback(self, evm, pad, x, y):
        percent_x = x / ((2<<14) + 0.0)
        percent_x = min(1, percent_x)
        percent_x = max(-1, percent_x)

        percent_y = y / ((2<<14) + 0.0)
        percent_y = min(1, percent_y)
        percent_y = max(-1, percent_y)

        # Convert -1.0-1.0 range to a 0.0-1.0 range
        self.set_throttle_scalar((percent_y + 1) / 2.0)

        if self._debug:
            print "Touchpad Position is {:2.2f}, {:2.2f}".format(percent_x, percent_y)

    def _stick_pressed_callback(self, evm):
        print "Stick pressed"

    def _stick_axes_callback(self, evm, x, y):
        percent_x = x / ((2<<14) + 0.0)
        percent_x = min(1, percent_x)
        percent_x = max(-1, percent_x)

        percent_y = y / ((2<<14) + 0.0)
        percent_y = min(1, percent_y)
        percent_y = max(-1, percent_y)
        self.set_pitch_scalar(percent_y)
        self.set_roll_scalar(percent_x)

        if self._debug:
            print "Stick Position is {:2.2f}, {:2.2f}".format(percent_x, percent_y)

    def _trigger_axes_callback(self, evm, pos, value):
        percent = value / ((2<<7) + 0.0)
        percent = min(1, percent)
        percent = max(-1, percent)

        # Right trigger button
        if pos == 0:
            self.set_yaw_scalar(percent)
        elif pos == 1:
            self.set_yaw_scalar(-percent)

        if self._debug:
            print "Trigger axes {} has value {:2.2f}".format(pos, percent)

if __name__ == '__main__':
    SteamControllerDevice()
