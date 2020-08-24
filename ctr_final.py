# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
import detect_dnn
import detect_face
import requests

# Import the PCA9685 module.
import Adafruit_PCA9685


while(true) :
    # face detection -> find id
    classes = ['KEC', 'PSI', 'SJS', 'SSJ', 'AJH',
               'YSS', 'LSH', 'LJH', 'LJY', 'JKS', 'JKY', 'JSY', 'CDW']
    user_list = facefunc()
    user_max = 0
    user_index = 0
    for i in range(len(user_list[12])):
        if (user_list[i] > user_max):
            user_index = i
            user_max = user_list[i]


    a = classes[user_index]
    userdata = {"id": a}

    # trash detection value
    trash_list = trashfunc()
    trash_id = 0
    trash_m = 0
    for i in range(len(trash_list)):
        if (trash_list[i] > trash_m):
            trash_id = i
            trash_m = trash_list[i]

    # Uncomment to enable debug output.
    # import logging
    # logging.basicConfig(level=logging.DEBUG)

    # Initialise the PCA9685 using the default address (0x40).
    pwm = Adafruit_PCA9685.PCA9685()

    # Alternatively specify a different address and/or bus:
    # pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

    # Configure min and max servo pulse lengths
    # servo0
    servo0_min = 200  # Min pulse length out of 4096
    servo0_mid = 370  # Max pulse length out of 4096
    servo0_max = 550
    # servo1
    servo1_min = 190  # Min pulse length out of 4096
    servo1_mid = 310  # 380
    servo1_max = 540


    # Helper function to make setting a servo pulse width simpler.
    def set_servo_pulse(channel, pulse):
        pulse_length = 1000000  # 1,000,000 us per second
        pulse_length //= 60  # 60 Hz
        print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096  # 12 bits of resolution
        print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        pwm.set_pwm(channel, 0, pulse)


    # Set frequency to 60hz, good for servos.
    pwm.set_pwm_freq(60)

    # move servo0,servo1 to mid
    pwm.set_pwm(0, 0, servo0_mid)
    pwm.set_pwm(1, 0, servo1_mid)

    # 'cardboard/paper','glass','metal','plastic','trash'
    # servo channel 0 : cardboard/paper
    time.sleep(10)
    if trash_id == 0:
        pwm.set_pwm(0, 0, servo0_max)
        time.sleep(1)
        pwm.set_pwm(0, 0, servo0_mid)
        time.sleep(1)
        resp = requests.post('http://211.117.148.206/add20point.php', data=userdata)
    # servo channel 0 : glass, metal
    elif trash_id == 1:
        pwm.set_pwm(0, 0, servo0_min)
        time.sleep(1)
        pwm.set_pwm(0, 0, servo0_mid)
        time.sleep(1)
        resp = requests.post('http://211.117.148.206/add30point.php', data=userdata)

    # servo channel 1 : plastic
    elif trash_id == 2:
        pwm.set_pwm(1, 0, servo1_max)
        time.sleep(1)
        pwm.set_pwm(1, 0, servo1_mid)
        time.sleep(1)
        resp = requests.post('http://211.117.148.206/add30point.php', data=userdata)

    # servo channel 1 : trash
    elif trash_id == 3:
        pwm.set_pwm(1, 0, servo1_min)
        time.sleep(1)
        pwm.set_pwm(1, 0, servo1_mid)
        time.sleep(1)