#Module imports
import mariadb
import sys
import serial
#Serial toma dos parametros: dispositivo serial y el baudrate
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
#To interact with with and manage databases on MariaDB Platform, we must instantiate  a cursor 
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
	balance=client.split(',')
	print("El saldo de la tarjeta ",uid_string," es de: ",balance[0])

def recharge():
	read_card()

def read_card():
	ser.write(value) #Escribe los bytes al puerto. Este debe de ser tipo byte (o compatible como bytearray)
	ser.flush() #Espera a que todos los datos esten escritos
	uid=ser.readline() #lee una linea terminada por '\n'. En nuestro caso despues de recibir el UID de la terminal
	uid=str(uid) #Convierte el UID a tipo string
	uid=uid[2:22] #Y se extra los caracteres basura	
	ser.close() #Se cierra el puerto
	return uid

while True:
	print("Introduzca operacion: 1.Ver saldo 2. Cobrar")
	op=input()
	if(op=='1'):
		#recargar_saldo()
		get_balance(cursor)
		#print_clientes(cursor)
	

