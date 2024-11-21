from tkinter import *
from ModifyIcon import modificar_Icon

class Perfiles(object):
	def __init__(self):
		pass
	def MUsuarioAdd(self,barr):
		self.Barra_Menu=barr
		addressIcon="img/menue/"
		self.M_Usuario=Menu(self.Barra_Menu,tearoff=False)
		self.icono=modificar_Icon(addressIcon+"addUser.png")			
		#self.M_Usuario.add_command(label='Agregar Usuario',command=self.Desk_User,image=self.icono,compound="left")
		
		#self.IcLUser=modificar_Icon(addressIcon+"ListUser.png")
		#self.M_Usuario.add_command(label='Reporte Usuario',command=self.Reporte_Usuarios,image=self.IcLUser,compound="left")
		self.Barra_Menu.add_cascade(label='Configuracion',menu=self.M_Usuario)
		
	#def MUsuarioAdd(self,barr):