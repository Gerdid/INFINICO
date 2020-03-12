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

ser=serial.Serial('/dev/ttyACM0',9600)

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

def get_balance(cursor,uid):
	client=[]
	uid_string=uid
	cursor.execute("SELECT balance FROM test.cliente WHERE uid=?",(uid,))
	for(uid) in cursor:
		client=(f"{uid}")
	balance=int(re.search(r'\d+',client).group(0))
	print("El saldo de la tarjeta ",uid_string," es de:",balance)
	return uid_string,balance

def read_balance(cursor,uid):
	#client=[]
	uid=read_card()
	uid_string=uid
	cursor.execute("SELECT balance FROM test.cliente WHERE uid=?",(uid,))
	for(uid) in cursor:
		client=(f"{uid}")
	balance=int(re.search(r'\d+',client).group(0))
	return balance

def read_points(cursor,uid):
	#uid_string=uid
	cursor.execute("SELECT points FROM test.cliente WHERE uid=?",(uid,))
	for(uid) in cursor:
		client=(f"{uid}")
	points=int(re.search(r'\d+',client).group(0))
	return points

def read_balance_and_points(cursor,uid):
	balance=read_balance(cursor,uid)
	points=read_points(cursor,uid)
	return uid,balance,points

def recharge(cursor,uid):
	uid_string,balance=get_balance(cursor,uid)
	print("Introduzca el monto a recargar: ")
	toCharge=int(input())
	new_balance=balance+toCharge
	update_balance(cursor,uid_string,new_balance)

def update_balance(cursor,uid_string,new_balance):
	#Actualiza el saldo del uid correspondiente
	cursor.execute("UPDATE test.cliente SET balance=? WHERE uid=?",(new_balance,uid_string))

def update_points(cursor,uid_string,new_points):
	#Actualiza los puntos del uid correspondiente
	cursor.execute("UPDATE test.cliente SET points=? WHERE uid=?",(new_points,uid_string))

def cobrar(cursor,uid):
	print("Ingrese total a cobrar: ")
	ammount=int(input())
	balance=read_balance(cursor)
	if(balance>=ammount):
		new_balance=balance-ammount
		update_balance(cursor,uid_string,new_balance)
	else:
		print("Saldo insuficiente, use otro metodo de pago")

def points_to_balance(cursor,uid):
	#10 puntos= $1
	points=read_points(cursor,uid)
	balance=read_balance(cursor,uid)
	#new_balance=balance+(points/10)
	#uid_string,balance,points=read_balance_and_points(cursor)
	#update_balance(cursor,uid,new_balance)
	#print(type(balance))
	#new_balance=balance+(points/10)
	#new_points=points-points
	balance_to_add=balance+balance//10
	rem_points=balance%10
	update_balance(cursor,uid,balance_to_add)
	update_points(cursor,uid,rem_points)

def display_card_summary(cursor,uid):
	#uid,balance,points=read_balance_and_points(cursor)
	balance=read_balance(cursor,uid)
	points=read_points(cursor,uid)
	print("-------------------------------------")
	print("------------Tarjeta No.--------------")
	print("-------",uid,"--------")
	print("SALDO:$ ",balance)
	print("PUNTOS: ",points)
	print("-------------------------------------")

def read_card():
	#Se abre el puerto serial para el ordenar a terminal y recepcion de datos de terminal
	#Serial toma dos parametros: dispositivo serial y el baudrate
	print("Escanee tarjeta")
	ser=serial.Serial('/dev/ttyACM0',9600)
	ser.write(value) #Escribe los bytes al puerto. Este debe de ser tipo byte (o compatible como bytearray)
	ser.flush() #Espera a que todos los datos esten escritos
	uid=ser.readline() #lee una linea terminada por '\n'. En nuestro caso despues de recibir el UID de la terminal
	uid=str(uid) #Convierte el UID a tipo string
	uid=uid[2:22] #Y se extra los caracteres basura
	ser.close() #Se cierra el puerto
	return uid

while True:
	print("Introduzca operacion: \n 1.Resumen de tarjeta \n 2.Recargar saldo \n 3.Cobrar \n 4.Convertir puntos a saldo")
	op=input()
	uid=read_card(cursor)
	if(op=='1'):
		display_card_summary(cursor,uid)
	if(op=='2'):
		recharge(cursor)
	if(op=='3'):
		cobrar(cursor)
	if(op=='4'):
		points_to_balance(cursor)


