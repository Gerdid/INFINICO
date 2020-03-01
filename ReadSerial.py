# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 11:37:19 2020

@author: Gerhard Didier
"""

import serial
#Serial takes two parameters: serial device and baudrate
ser=serial.Serial('COM6',9600)
value=bytearray([49])

#import time
while True:
    
    ser.write(value)
    ser.flush()
    #time.sleep(5)
    data=ser.readline()
    data=str(data)
    data=data[2:22]
    print(data)    
    #print('Hola '+data)
    #print(type(data))
    ser.close()    
    break


