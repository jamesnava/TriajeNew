import pyodbc
from tkinter import messagebox
import configparser
from codificacion import descifrar,cifrar

class Conexion_Galen(object):
	def __init__(self):
		self.configuracion=configparser.ConfigParser()
		self.configuracion.read('config_GALEN.ini')
		self.llave='qBBws2UNvFJNFZ5oRh5yx04AIhSzhCgjsfS3Q44QL_M='
	def ejecutar_conn(self):
		servidor=self.configuracion['DEFAULT']['SERVER']
		bd=self.configuracion['DEFAULT']['DATABASE']
		user=self.configuracion['DEFAULT']['USER']
		password=self.configuracion['DEFAULT']['PASSWORD']
		
		user1=descifrar(self.llave,user)
		pwd=descifrar(self.llave,password)
		driver='{SQL Server}'					
		self.conn = pyodbc.connect(f"""DRIVER={driver};SERVER={servidor};DATABASE={bd};UID={user1};PWD={pwd}""")		
	def get_cursor(self):
		try:
			self.puntero=self.conn.cursor()
			return self.puntero
		except Exception as e:
			messagebox.showinfo('Notificación','No pudo conectarse al servidor SISGALENPLUS')		
		
	def close_conection(self):
		self.conn.close()

class Conexion_Triaje(object):
	def __init__(self):
		self.configuracion=configparser.ConfigParser()
		self.configuracion.read('config_Triaje.ini')
		self.llave='qBBws2UNvFJNFZ5oRh5yx04AIhSzhCgjsfS3Q44QL_M='
	def ejecutar_conn(self):
		servidor=self.configuracion['DEFAULT']['SERVER']
		bd=self.configuracion['DEFAULT']['DATABASE']
		user=self.configuracion['DEFAULT']['USER']
		password=self.configuracion['DEFAULT']['PASSWORD']

		user1=descifrar(self.llave,user)
		pwd=descifrar(self.llave,password)
		driver='{SQL Server}'					
		self.conn = pyodbc.connect(f"""DRIVER={driver};SERVER={servidor};DATABASE={bd};UID={user1};PWD={pwd}""")		
	def get_cursor(self):
		try:
			self.puntero=self.conn.cursor()
			return self.puntero
		except Exception as e:
			messagebox.showinfo('Notificación','No pudo conectarse al servidor SISGALENPLUS')		
		
	def close_conection(self):		
		self.conn.close()

class Conexion_Externo(object):
	def __init__(self):
		self.configuracion=configparser.ConfigParser()
		self.configuracion.read('config_EXT.ini')
		self.llave='qBBws2UNvFJNFZ5oRh5yx04AIhSzhCgjsfS3Q44QL_M='
	def ejecutar_conn(self):
		servidor=self.configuracion['DEFAULT']['SERVER']
		bd=self.configuracion['DEFAULT']['DATABASE']
		user=self.configuracion['DEFAULT']['USER']
		password=self.configuracion['DEFAULT']['PASSWORD']
		
		user1=descifrar(self.llave,user)
		pwd=descifrar(self.llave,password)	
		driver='{SQL Server}'					
		self.conn = pyodbc.connect(f"""DRIVER={driver};SERVER={servidor};DATABASE={bd};UID={user1};PWD={pwd}""")		
	def get_cursor(self):
		try:
			self.puntero=self.conn.cursor()
			return self.puntero
		except Exception as e:
			messagebox.showinfo('Notificación','No pudo conectarse al servidor SISGALENPLUS')		
		
	def close_conection(self):
		self.puntero.close()
		self.conn.close()

