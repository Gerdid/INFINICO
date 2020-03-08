"""
PROYECTO INTEGRADOR
INFINICO
8-Mar-2020

Authors:
Sandra Cristina Sixtos Barrera
Gerhard Didier de la Mora
"""

#module imports
import mariadb
import sys
import serial
import re

ser=serial.Serial('/dev/ttyACM1',9600)

#variable que almacena el arreglo con el valor tipo byte 49 (ASCII 1)
value=bytearray([49])
#Cuando se envia el valor 49 por el puerto serial se le manda decir a la terminal que lea la tarjeta

#Conexion a servidor
try:
    conn=mariadb.connect(
        user="root",
        password="root",
        host='192.168.137.1',
        port=3306)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
#To interact with and manage databases on MariaDB Platform, we must instantiate  a cursor 
#The cursor provides methods for interacting with data from Python code. The cursor provides two
#methods for executing SQL code: execute() and executemany()
cursor=conn.cursor()

def get_balance(cursor):
	print("Escanee tarjeta")
	client=[]
	uid=read_card()
	uid_string=uid
	cursor.execute("SELECT balance FROM test.cliente WHERE uid=?",(uid,))
	for(uid) in cursor:
		client=(f"{uid}")
	balance=int(re.search(r'\d+',client).group(0))
	print("El saldo de la tarjeta ",uid_string," es de:",balance)
	return uid_string,balance

def read_balance(cursor,uid):
	#print("Escanee tarjeta")
	#client=[]
	#uid=read_card()
	uid_string=uid
	cursor.execute("SELECT balance FROM test.cliente WHERE uid=?",(uid,))
	for(uid) in cursor:
		client=(f"{uid}")
	balance=int(re.search(r'\d+',client).group(0))
	return balance

def read_points(cursor,uid):
	#print("Escanee tarjeta")
	#client=[]
	#uid=read_card()
	uid_string=uid
	cursor.execute("SELECT points FROM test.cliente WHERE uid=?",(uid,))
	for(uid) in cursor:
		client=(f"{uid}")
	points=int(re.search(r'\d+',client).group(0))
	return points

def read_balance_and_points(cursor):
	#client=[]
	uid=read_card()
	uid_string=uid
	balance=read_balance(cursor,uid)
	points=read_points(cursor,uid)
	return uid_string,balance,points

def recharge(cursor):
	uid_string,balance=get_balance(cursor)
	print("Introduzca el monto a recargar: ")
	toCharge=int(input())
	new_balance=balance+toCharge
	print(new_balance)
	print(uid_string)
	update_balance(cursor,uid_string,new_balance)

def update_balance(cursor,uid_string,new_balance):
	#Actualiza el saldo del uid correspondiente
	cursor.execute("UPDATE test.cliente SET balance=? WHERE uid=?",(new_balance,uid_string))

def read_card():
	#Se abre el puerto serial para el ordenar a terminal y recepcion de datos de terminal
	#Serial toma dos parametros: dispositivo serial y el baudrate
	print("Escanee tarjeta")
	#client=[]
	#uid=read_card()
	ser=serial.Serial('/dev/ttyACM1',9600)
	ser.write(value) #Escribe los bytes al puerto. Este debe de ser tipo byte (o compatible como bytearray)
	ser.flush() #Espera a que todos los datos esten escritos
	uid=ser.readline() #lee una linea terminada por '\n'. En nuestro caso despues de recibir el UID de la terminal
	uid=str(uid) #Convierte el UID a tipo string
	uid=uid[2:22] #Y se extra los caracteres basura
	ser.close() #Se cierra el puerto
	return uid

def cobrar(cursor):
	print("Ingrese total a cobrar: ")
	ammount=int(input())
	uid_string,balance=read_balance(cursor)
	if(balance>=ammount):
		new_balance=balance-ammount
		update_balance(cursor,uid_string,new_balance)
	else:
		print("Saldo insuficiente, use otro metodo de pago")

def display_card_summary(cursor):
	uid_string,balance,points=read_balance_and_points(cursor)
	print("-------------------------------------")
	print("------------Tarjeta No.--------------")
	print("-------",uid_string,"--------")
	print("SALDO:$ ",balance)
	print("PUNTOS: ",points)
	print("-------------------------------------")


while True:
	print("Introduzca operacion: 1.Resumen de tarjeta 2.Recargar saldo 3.Cobrar")
	op=input()
	if(op=='1'):
		display_card_summary(cursor)
	if(op=='2'):
		recharge(cursor)
	if(op=='3'):
		cobrar(cursor)


