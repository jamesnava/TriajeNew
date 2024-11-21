from tkinter import *
from tkinter import ttk
from Consulta_Externo import consultaExterno


class Alerta(object):
	"""docstring for Alerta"""
	def __init__(self):
		pass
	def Ventana_Alert(self):
		font1=('Comic Sans MS',12,'bold')
		obj_consulta=consultaExterno()
		rows=obj_consulta.numberFuas()

		inicio=int(rows[0].FuaUltimoGenerado)
		fin =int(rows[0].FuaNumeroFinal)
		restante=fin-inicio

		if restante<500:

			ventanaAlert=Toplevel(bg="#b81414")
			ventanaAlert.geometry("600x150+50+100")
			ventanaAlert.grab_set()
			ventanaAlert.overrideredirect(True)		

			label=Label(ventanaAlert,text="ALERTA!!!",bg="#b81414",fg="#fff",font=('Comic Sans MS',14,'bold'))
			label.grid(row=0,column=0,columnspan=10,pady=5)
			label=Label(ventanaAlert,text=f"""TENER EN CUENTA QUE SOLAMENTE LE QUEDAN {restante} FUAS PARA ATENCIONES \n EN CONSULTORIO EXTERNO""",bg="#b81414",fg="#fff",font=('Comic Sans MS',10,'bold'))
			label.grid(row=1,column=0,columnspan=10,pady=5)

			buttoClose=ttk.Button(ventanaAlert,text="Aceptar")
			buttoClose.grid(row=2,column=1,columnspan=10,pady=10)
			buttoClose.configure(command=ventanaAlert.destroy)
