# 200 steps = 1 revolution = pi * 9 cm

from RpiMotorLib import RpiMotorLib
import threading
import RPi.GPIO as GPIO
import time

# Defining all Constants

STEP1 = 27      
DIRECTION1 = 22 

STEP2 = 23
DIRECTION2 = 24

# TODO important
GPIO_pins = (14, 15, 18)

GPIO_TRIGGER_FRONT = 27
GPIO_ECHO_FRONT = 22

GPIO_TRIGGER_BACK = 17
GPIO_ECHO_BACK = 27

GPIO_TRIGGER_LEFT = 17
GPIO_ECHO_LEFT = 27

GPIO_TRIGGER_RIGHT = 17
GPIO_ECHO_RIGHT = 27

# Setups and initializations

GPIO.setmode(GPIO.BCM) 
GPIO.setup(GPIO_TRIGGER_FRONT, GPIO.OUT)
GPIO.setup(GPIO_ECHO_FRONT, GPIO.IN)
# GPIO.setup(GPIO_TRIGGER_BACK, GPIO.OUT)
# GPIO.setup(GPIO_ECHO_BACK, GPIO.IN)
# GPIO.setup(GPIO_TRIGGER_LEFT, GPIO.OUT)
# GPIO.setup(GPIO_ECHO_LEFT, GPIO.IN)
# GPIO.setup(GPIO_TRIGGER_RIGHT, GPIO.OUT)
# GPIO.setup(GPIO_ECHO_RIGHT, GPIO.IN)

# motor1 = RpiMotorLib.A4988Nema(DIRECTION1, STEP1, GPIO_pins, "A4988")
# motor2 = RpiMotorLib.A4988Nema(DIRECTION2, STEP2, GPIO_pins, "A4988")

# Defining functions

def motor_1_distance(amount: int, dir: bool):

    # 200 steps = 1 revol = 9 pi cm
    # 7.0735 steps = 1 cm

    motor1.motor_go(dir, "Full" , int(7.0735 * amount), 0.005, True, 0)

def motor_2_distance(amount: int, dir: bool):

    motor2.motor_go(dir, "Full", int(7.0735 * amount), 0.005, True, 0)

def motor_1_steps(steps: int, dir: bool):

    # 200 steps: 1 full rotation

    motor1.motor_go(dir, "Full", steps, 0.005, True, 0)

def motor_2_steps(steps: int, dir: bool):

    motor2.motor_go(dir, "Full", steps, 0.005, True, 0)

def distance(trigger_pin: int, echo_pin: int) -> int:
    GPIO.output(trigger_pin, True)
 
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)
 
    initial_time = time.time()

    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(echo_pin) == 0:
        StartTime = time.time()

        # if (initial_time - StartTime > 5):
        #     return distance()

    while GPIO.input(echo_pin) == 1:
        StopTime = time.time()

        # if (initial_time - StartTime > 5):
        #     return distance()

    TimeElapsed = StopTime - StartTime
    dist = (TimeElapsed * 34300) / 2

    return dist

def turn_left():

    thr1 = threading.Thread(target = lambda: motor_1_steps(50, True))
    thr2 = threading.Thread(target = lambda: motor_1_steps(50, True))

    thr1.start()
    thr2.start()

    print("Turn left")

def turn_right():

    thr1 = threading.Thread(target = lambda: motor_1_steps(50, False))
    thr2 = threading.Thread(target = lambda: motor_1_steps(50, False))

    thr1.start()
    thr2.start()

    print("Turn right")

def go_straight(n):

    thr1 = threading.Thread(target = lambda: motor_1_distance(18 * n, True))
    thr2 = threading.Thread(target = lambda: motor_2_distance(18 * n, False))

    thr1.start()
    thr2.start()

    print("going straight by", n)

def go_back(n):

    thr1 = threading.Thread(target = lambda: motor_1_distance(18 * n, False))
    thr2 = threading.Thread(target = lambda: motor_2_distance(18 * n, True))

    thr1.start()
    thr2.start()

    print("going back by", n)

def is_wall_left():

    if (distance(GPIO_TRIGGER_LEFT, GPIO_ECHO_LEFT) > 5):
        return False
    return True

def is_wall_front():

    if (distance(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT) > 5):
        return False
    return True

def is_wall_right():

    if (distance(GPIO_TRIGGER_RIGHT, GPIO_ECHO_RIGHT) > 5):
        return False
    return True


def is_wall_back():

    if (distance(GPIO_TRIGGER_BACK, GPIO_ECHO_BACK) > 5):
        return False
    return True

if __name__ == '__main__':
    try:
        while True:
            dist = distance(GPIO_TRIGGER_FRONT, GPIO_ECHO_FRONT)
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
