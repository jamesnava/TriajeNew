from tkinter import ttk
import tkinter as tk
from tktimepicker import SpinTimePickerModern

def llenarText(diccionario):
	for clave,valor in diccionario.items():
		clave.delete(0,"end")
		clave.insert('end',valor)
def llenarDate(diccionario):
	for clave,valor in diccionario.items():
		
		if valor.find(":")>=0:					
			clave.set24Hrs(valor[:valor.find(":")])
			clave.setMins(valor[valor.find(":")+1:])
def marcarCheck(diccionario):
	for clave,valor in diccionario.items():		
		valor[0].set(valor[1])

def activarCampos(*args):
	for val in args:
		val.config(state="normal")
		
def soloLecturaCampos(*args):
	for val in args:
		val.config(state="readonly")

def llenar_Table(tabla,rows,lista):
	for val in rows:
		valores=tuple(getattr(val,valor) for valor in lista)
		tabla.insert('','end',values=valores)

def getValuesWidget(frame):
	data={}
	for widget in frame.winfo_children():
		if hasattr(widget,"custom_name"):
			if isinstance(widget, tk.Entry):
				data[widget.custom_name] = widget.get()
			elif isinstance(widget, tk.Text):
				data[widget.custom_name] = widget.get("1.0", "end-1c") 
			elif isinstance(widget, ttk.Combobox):
				data[widget.custom_name] = widget.get()  
			elif isinstance(widget, tk.Checkbutton):
				var=widget.cget("variable")
				data[widget.custom_name] = widget.getvar(var)
			elif isinstance(widget,SpinTimePickerModern):
				data[widget.custom_name]="{}:{}".format(*widget.time())

	return data


		