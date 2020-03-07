# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 11:37:19 2020

@author: Gerhard Didier
"""

import serial #Modulo que encapsula el acceso al puerto serial

#Serial toma dos parametros: dispositivo serial y el baudrate
ser=serial.Serial('/dev/ttyACM0',9600)

value=bytearray([49])#variable que almacena el arreglo con el valor tipo byte 49 (ASCII 1)
#Cuando se envia el valor 49 por el puerto serial se la manda decir a la terminal que lea la tarjeta

#Loop infinito
while True:
    ser.write(value) #Escribe los bytes al puerto. Este debe de ser tipo byte (o compatible como bytearray)
    ser.flush() #Espera a que todos los datos esten escritos
    uid=ser.readline() #lee una linea terminada por '\n'. En nuestro caso despues de recibir el UID de la terminal
    uid=str(uid)#Convierte el UID a tipo string
    uid=uid[2:22]#Y se extraen los caracteres basura
    print(uid)#Se imprime el uid para confirmar la recepcion    
    ser.close()#Se cierra el puerto     
    break 


