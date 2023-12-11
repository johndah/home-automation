#!/usr/bin/python

import pigpio
import sys, math

def hsv_to_rgb(hue, saturation, value):
    n_sectors = 6

    hue = float(hue) / 360.0
    saturation = float(saturation) / 100.0
    value = float(value) / 255.0
    
    sector = math.floor(hue * n_sectors)
    fractional_part = hue * n_sectors - sector
    
    low = value * (1 - saturation)
    high = value * (1 - fractional_part * saturation)
    mid = value * (1 - (1 - fractional_part) * saturation)

    rgb_colors = [
        (value, mid, low),
        (high, value, low),
        (low, value, mid),
        (low, high, value),
        (mid, low, value),
        (value, low, high)
    ]
    
    r, g, b = rgb_colors[int(sector % n_sectors)]
    
    return int(r * 255), int(g * 255), int(b * 255)

pi = pigpio.pi()

RED_PIN = 17
GREEN_PIN = 22
BLUE_PIN = 24

hue = float(sys.argv[1])
saturation = float(sys.argv[2])
value = float(sys.argv[3])

red, green, blue = hsv_to_rgb(hue, saturation, value)

pi.set_PWM_dutycycle(RED_PIN, red)
pi.set_PWM_dutycycle(GREEN_PIN, green)
pi.set_PWM_dutycycle(BLUE_PIN, blue)

