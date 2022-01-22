# Pico Cube Matrix effect
# this is based on the demo script "pico_led_cube_pattern.py"
# https://github.com/sbcshop/PICO-CUBE/
#
# Each layer is encoded as a 16bit number
# The script cycles through a list of these numbers with 
# only few bits set


from machine import Pin
import time
import random
import utime
from random import *

#LAYER = [9,8,7,6]#layers

#reverse layers for top to bottom
LAYER = [6,7,8,9]#layers

#columns
GRID_3D = [[17, 16, 0, 1], 
           [19, 18, 2, 3],
           [21, 20, 4, 5],
           [26, 22, 28, 27]]

# we don't need the 2d representation of a layer
GRID_2D = [17, 16, 0, 1, 19, 18, 2, 3, 21, 20, 4, 5, 26, 22, 28, 27]

numberList = []

def enable_layer(layer):
    a = Pin(LAYER[layer])
    a.on()

def disable_layer(layer):
    a = Pin(LAYER[layer])
    a.off()

def light_on(y,x, z,):
    enable_layer(y)
    pin_num = GRID_3D[x][z]
    print(pin_num)
    a = Pin(GRID_3D[x][z])
    a.on()

def light_on_bitmap(y, temp_array):
    enable_layer(y)
    for i in range(16):
        pin_num = GRID_2D[i]
        a = Pin(pin_num)
        if(temp_array[i] == 1):
            a.on()
        else:
            a.off()
    

def light_off(y, x, z):
    enable_layer(y)
    a = Pin(GRID_3D[x][z])
    a.off()
    

def reset(t):
    for x in range(4):
        for z in range(4):
            a = Pin(GRID_3D[x][z])
            a.off()
            time.sleep(t)
            
def resetlayer():
    for i in range(0,4):
        a = Pin(LAYER[i])
        a.off()
        time.sleep(0.01)

def count_ones(number):
    ones = 0
    while number > 0:
        mod = number % 2
        if mod == 1:
            ones = ones + 1
        number = number // 2
    return ones

def random_number_with_max_ones(max_ones):
    random_number = randint(0, 65535)
    while count_ones(random_number) > max_ones:
        random_number = randint(0, 65535)
    return random_number

def number_2_array(number):
    index = 0
    bin_number = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    while index < 16:
        mod = number % 2
        if mod == 1:
            bin_number[index] = 1;
        number = number // 2
        index = index + 1
    return bin_number
    
def rotate_numbers(numberList):
    numberList = numberList[1:] + numberList[:1]
    numberList[3] = random_number_with_max_ones(4)
    return numberList

for pin in LAYER:
    Pin(pin, Pin.OUT)

for x in range(4):
    for z in range(4):
        Pin(GRID_3D[x][z], Pin.OUT)

reset(0)
resetlayer()

#generate a list of numbers that only have 1 bit set to 1
for i in range(65535):
    print('.', end='')
    if(count_ones(i)<=1):
        numberList.append(i)
    if(len(numberList) >= 50):
        break



#since only one layer can be active at once we have to continually 
# cycle through them and rely on persistance of vision.
# each time the counter is hit we cycle through a new number
counter = 0
while True:
    counter = counter + 1
    if(counter > 10):
        numberList = rotate_numbers(numberList)
        counter = 0
    for y in range(4):
        enable_layer(y)
        light_on_bitmap(y, number_2_array(numberList[y]))
        utime.sleep(0.003)
        disable_layer(y)

    
