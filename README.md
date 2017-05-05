# sgfc

My drone flight Command-and-Control implementation.
(Very early WIP)

## Communication module

This module is used to send and recieve protobufs between devices using an abstracted API. Currently only supports XBee.

## Control module

This module is used to take input from the user for controlling the drone. Currently only supports the Steam controller.

## Position module

This module can be used to read the position of a GPS module over UART. Currently only supports Adafruit GPS module.

## Vision module

This module takes pictures from two USB cameras and will eventually use that data to generate obstacle avoidance logic though right now it doesn't do much other than show the pictures taken.
