#Module imports
import mariadb
import sys

#Instantiate Connection
try:
    conn=mariadb.connect(
        user="root",
        password="root",
        host='192.168.137.1',
        port=3306)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cursor=conn.cursor()
#val=(4,100,200)
#cursor.execute("INSERT INTO test.cliente(uid,puntos,saldo) VALUES(?,?,?)",val)

#Adds client
#def add_client(uid,puntos,saldo):

#    cursor.execute("INSERT INTO test.cliente(uid,puntos,saldo) VALUES(?,?,?)",(uid,puntos,saldo))

#add_client(5,5,1)
"""
#Imprime lista de clientes
def print_clientes(cursor):

	#Inicializacion de variables
	clientes=[]

	#Lee clientes
	cursor.execute("SELECT uid,puntos,saldo FROM test.cliente")

	#Preparar clientes
	for (uid,puntos,saldo) in cursor:
		clientes.append(f"{uid} {puntos} {saldo}")

	#lista de contactos
	print("\n".join(clientes))

#print_clientes(cursor)
"""
"""
def leer_tarjeta:
"""
import re
def get_client(cursor):
	print("Escanee tarjeta")
	cliente=[]
	uid=leer_tarjeta()
	uid_string=uid
	#print(uid)
	uid_tuple=(tuple(uid))
	cursor.execute("SELECT saldo FROM test.cliente WHERE uid=?",(uid,))
	#print(tuple(uid))
	#print(cursor)
	for(uid) in cursor:
		cliente=(f"{uid}")

	#print("\n".join(cliente))
	#print(type(cliente))
	saldo=cliente.split(',')
	print("El saldo de la tarjeta ",uid_string," es de: ",saldo[0])

def recargar_saldo():
	leer_tarjeta()

import serial
#Serial toma dos parametros: dispositivo serial y el baudrate
ser=serial.Serial('/dev/ttyACM0',9600)

#variable que almacena el arreglo con el valor tipo byte 49 (ASCII 1)
value=bytearray([49])
#Cuando se envia el valor 49 por el puerto serial se le manda decir a la terminal que lea la tarjeta



def leer_tarjeta():
	ser.write(value) #Escribe los bytes al puerto. Este debe de ser tipo byte (o compatible como bytearray)
	ser.flush() #Espera a que todos los datos esten escritos
	uid=ser.readline() #lee una linea terminada por '\n'. En nuestro caso despues de recibir el UID de la terminal
	uid=str(uid) #Convierte el UID a tipo string
	uid=uid[2:22] #Y se extra los caracteres basura
	#print(uid) #Se imprime el uid para confirmar la recepcion
	#print(type(uid))
	ser.close() #Se cierra el puerto
	return uid

while True:
	print("Introduzca operacion: 1.Ver saldo 2. Cobrar")
	operacion=input()
	if(operacion=='1'):
		#recargar_saldo()
		get_client(cursor)
		#print_clientes(cursor)
	

