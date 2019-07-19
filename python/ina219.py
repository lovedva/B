#!/usr/bin/env python
<<<<<<< HEAD
from ina219_pi import INA219
from ina219_pi import DeviceRangeError
=======
# -*- coding: utf-8 -*-
#INA219电流传感器
from pi_ina219 import INA219
from pi_ina219 import DeviceRangeError
>>>>>>> c136cbb53e8d61b8a4e23313872786d320e77e92

SHUNT_OHMS = 0.1


def read():
    ina = INA219(SHUNT_OHMS)
    ina.configure()

    print("Bus Voltage: %.3f V" % ina.voltage())
    try:
        print("Bus Current: %.3f mA" % ina.current())
        print("Power: %.3f mW" % ina.power())
        print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)


if __name__ == "__main__":
    read()