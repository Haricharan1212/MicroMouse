import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib

import threading

#define GPIO pins
GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction1 = 22      # Direction -> GPIO Pin
step1 = 27      # Step -> GPIO Pin

direction2 = 24
step2 = 23

# Declare an named instance of class pass GPIO pins numbers

mymotortest = RpiMotorLib.A4988Nema(direction1, step1, GPIO_pins, "A4988")

mymotortest2 = RpiMotorLib.A4988Nema(direction2, step2, GPIO_pins, "A4988")

# call the function, pass the arguments
def f1():
    mymotortest.motor_go(False, "Full" , 100, .005, True, 0)

def f2():
    mymotortest2.motor_go(True, "Half", 200, 0.0025, True, 0)


thr1 = threading.Thread(target = f1)
thr2 = threading.Thread(target = f2)

thr1.start()
thr2.start()

