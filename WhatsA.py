#from tkinter import *
#from tkinter import ttk
#from tkinter import filedialog
#import pandas as pd
#import pywhatkit
#import time 
#import pyautogui
#from pynput.keyboard import Key, Controller



#class MessageW(object):
#	
#	def __init__(self):
#		
#		self.ventana=Toplevel()
#		self.ventana.geometry("400x300")
#		self.ventana.title('Enviar Mensaje')
#		self.ventana.grab_set()
#		label=Label(self.ventana,text="Ruta del Archivo")
#		label.grid(row=1,column=1,pady=10)
#		self.EntryRuta=ttk.Entry(self.ventana)
#		self.EntryRuta.grid(row=1,column=2,columnspan=2,pady=10,padx=5)
#		btnBuscar=ttk.Button(self.ventana,text="...")
#		btnBuscar['command']=self.get_address
#		btnBuscar.grid(row=1,column=4,pady=10)
#
#		label=Label(self.ventana,text="Mensaje: ")
#		label.grid(row=2,column=1,pady=10)
#		self.mensaje=Text(self.ventana,width=25,height=4)
#		self.mensaje.grid(row=2,column=2,columnspan=3,pady=10)
#
#
#		btnEnviar=ttk.Button(self.ventana,text="Eviar")
#		btnEnviar.grid(row=3,column=1,pady=10)
#		btnEnviar['command']=self.Enviar_msg
#
#
#		btnCancelar=ttk.Button(self.ventana,text="Cancelar")
#		btnCancelar.grid(row=3,column=2,pady=10)
#
#	def get_address(self):
#		filename=filedialog.askopenfilename(title='Seleccione un archivo excel',initialdir='/',filetypes=[("Archivos Excel",'*.xlsx')])
#		if filename:
#			self.EntryRuta.delete(0,'end')
#			self.EntryRuta.insert("end",filename)
#
#	def Enviar_msg(self):
#		keyboard = Controller()
#		ruta=self.EntryRuta.get()
#		dataframe=pd.read_excel(ruta)
#		columna=dataframe.iloc[:,1]
#
#		texto=self.mensaje.get("1.0","end")
#		for numeros in columna:
#			try:				
#				#pywhatkit.sendwhatmsg_instantly(phone_no="+51"+str(numeros),message=texto)
#				pywhatkit.sendwhatmsg_instantly(phone_no="+51"+str(numeros),message=texto,tab_close=True)
#				time.sleep(10)
#				pyautogui.click()
#				time.sleep(2)
#				keyboard.press(Key.enter)
#				keyboard.release(Key.enter)    			       
#				self.ventana.destroy
#			except Exception as e:
#				print(e)



		