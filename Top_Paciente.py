from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import Consulta_Triaje
import apis

class Paciente(object):
	def __init__(self):
		self.font_text=('Candara',12,'bold')
		#self.obj_ConsultaGalen=Consulta_Galen.queryGalen()
		self.obj_ConsultaTriaje=Consulta_Triaje.queryTriaje()		
	def Top_Agregar(self):
		self.ventana_Paciente=Toplevel()
		self.ventana_Paciente.geometry('500x350')
		#self.ventana_Paciente.attributes('-topmost',True)
		self.ventana_Paciente.title('Agregar Paciente')
		self.ventana_Paciente.iconbitmap('img/paciente.ico')
		etiqueta_nombre=Label(self.ventana_Paciente,text='Dni: ',font=self.font_text,fg='#105B79')
		etiqueta_nombre.grid(row=1,column=0,pady=10)
		self.Entry_Dni=ttk.Entry(self.ventana_Paciente,width=50)
		self.Entry_Dni.bind('<KeyRelease>',self.validar_dni)
		self.Entry_Dni.bind('<Return>',self.consultar_api)
		self.Entry_Dni.bind('<Button-1>',self.evento_borrar)		
		self.Entry_Dni.grid(row=1,column=1,pady=10)

		etiqueta_nombre=Label(self.ventana_Paciente,text='Nombres: ',font=self.font_text,fg='#105B79')
		etiqueta_nombre.grid(row=2,column=0,pady=10)
		self.Entry_Nombre=ttk.Entry(self.ventana_Paciente,width=50)
		self.Entry_Nombre.grid(row=2,column=1,pady=10)

		etiqueta_apellidoP=Label(self.ventana_Paciente,text='Ap. Paterno: ',font=self.font_text,fg='#105B79')
		etiqueta_apellidoP.grid(row=3,column=0)
		self.Entry_apellidoP=ttk.Entry(self.ventana_Paciente,width=50)
		self.Entry_apellidoP.grid(row=3,column=1,pady=6)

		etiqueta_apellidoM=Label(self.ventana_Paciente,text='Ap. Materno: ',font=self.font_text,fg='#105B79')
		etiqueta_apellidoM.grid(row=4,column=0)
		self.Entry_apellidoM=ttk.Entry(self.ventana_Paciente,width=50)
		self.Entry_apellidoM.grid(row=4,column=1,pady=6)

		etiqueta_Telefono=Label(self.ventana_Paciente,text='Telefono: ',font=self.font_text,fg='#105B79')
		etiqueta_Telefono.grid(row=5,column=0,pady=6)
		self.Entry_Telefono=ttk.Entry(self.ventana_Paciente,width=50)
		self.Entry_Telefono.grid(row=5,column=1,pady=6)

		etiqueta_Procedencia=Label(self.ventana_Paciente,text='Procedencia: ',font=self.font_text,fg='#105B79')
		etiqueta_Procedencia.grid(row=6,column=0,pady=6)
		self.Entry_Procedencia=ttk.Entry(self.ventana_Paciente,width=50)
		self.Entry_Procedencia.grid(row=6,column=1,pady=6)		

		self.btn_Guardar=ttk.Button(self.ventana_Paciente,text='GUARDAR')
		self.btn_Guardar['command']=self.Insert_Paciente
		self.btn_Guardar.grid(row=10,column=0,padx=10,sticky='e')	

		self.btn_Cancelar=ttk.Button(self.ventana_Paciente,text='CANCELAR')
		self.btn_Cancelar['command']=self.ventana_Paciente.destroy
		self.btn_Cancelar.grid(row=10,column=0,columnspan=2)
		self.ventana_Paciente.focus()
		self.ventana_Paciente.grab_set()	
		self.ventana_Paciente.mainloop()
	def Insert_Paciente(self):
		dni=self.Entry_Dni.get()
		nombres=self.Entry_Nombre.get()
		apellidoP=self.Entry_apellidoP.get()
		apellidoM=self.Entry_apellidoM.get()
		telefono=self.Entry_Telefono.get()
		procedencia=self.Entry_Procedencia.get()
		if len(dni)!=0:
			if len(apellidoP)!=0 and len(apellidoM)!=0:
				datos={'dni':dni,'nombres':nombres,'apellidoP':apellidoP,'apellidoM':apellidoM,'telefono':telefono,'procedencia':procedencia}
				try:
					self.obj_ConsultaTriaje.Insert_Paciente(datos)
					messagebox.showinfo('Alerta','los datos se ingresaron correctamente')
					self.borrado_widget()
				except Exception as e:
					messagebox.showerror('Alerta',f'no se pudo insertar {e}')
				
			else:
				messagebox.showinfo('Notificación','Llene los campos')
		else:
			self.Entry_Dni.focus()
			messagebox.showinfo('Notificación','Llene el campo DNI')
	def consultar_api(self,event):
		dni=self.Entry_Dni.get()
		url=f'https://dniruc.apisperu.com/api/v1/dni/{dni}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im5vZG9oc3JhQGdtYWlsLmNvbSJ9.WkIBBcgkPKa--f49K61ReAErp0JbrPu9wULMOaqR9_E'
		nombre,apellidop,apellidom=apis.datos_persona(url)
		if len(nombre)!=0:
			self.Entry_Nombre.insert('end',nombre)
			self.Entry_apellidoP.insert('end',apellidop)
			self.Entry_apellidoM.insert('end',apellidom)
		else:
			messagebox.showinfo('Alerta','No hay comunicacion con la Reniec, ingrese manualmente')

	def validar_dni(self,event):
		dni=self.Entry_Dni.get()
		if not dni.isdigit():
			messagebox.showinfo('Alerta','Solo Acepta datos numericos')
			self.Entry_Dni.delete(0,'end')
	def evento_borrar(self,event):
		self.borrado_widget()
	def borrado_widget(self):
		self.Entry_Dni.delete(0,'end')
		self.Entry_Nombre.delete(0,'end')
		self.Entry_apellidoP.delete(0,'end')
		self.Entry_apellidoM.delete(0,'end')		
		self.Entry_Telefono.delete(0,'end')
		self.Entry_Procedencia.delete(0,'end')

	def paciente_Visualizacion(self):
		self.TopVisualizar=Toplevel()
		self.TopVisualizar.resizable(0,0)
		self.TopVisualizar.geometry("865x400+350+50")
		self.TopVisualizar.iconbitmap('img/paciente.ico')
		self.TopVisualizar.title('Lista de pacientes')
		self.TopVisualizar.focus_set()	
		self.TopVisualizar.grab_set()

		label_title=Label(self.TopVisualizar,text='Buscar')
		label_title.place(x=20,y=20)
		self.Entry_buscar_General=ttk.Entry(self.TopVisualizar,width=30)
		self.Entry_buscar_General.focus()
		self.Entry_buscar_General.place(x=80,y=20)
		self.Entry_buscar_General.bind('<KeyRelease>',self.search_paciente)
		#tabla...
		self.table_General=ttk.Treeview(self.TopVisualizar,columns=('#1','#2','#3','#4','#5','#6'),show='headings')		
		self.table_General.heading("#1",text="DNI")
		self.table_General.column("#1",width=100,anchor="center")
		self.table_General.heading("#2",text="NOMBRES")
		self.table_General.column("#2",width=100,anchor="center")
		self.table_General.heading("#3",text="APELLIDO PATERNO")
		self.table_General.column("#3",width=200,anchor="center")
		self.table_General.heading("#4",text="APELLIDO MATERNO")
		self.table_General.column("#4",width=200,anchor="center")
		self.table_General.heading("#5",text="TELEFONO")
		self.table_General.column("#5",width=100,anchor="center")
		self.table_General.heading("#6",text="PROCEDENCIA")
		self.table_General.column("#6",width=150,anchor="center")									
		self.table_General.place(x=10,y=70,width=840,height=290)
		self.llenar_TablePacientes()
		#self.table_General.bind('<<TreeviewSelect>>',self.itemTable_selected)

		self.Link_Modificar=Label(self.TopVisualizar,text='Modificar',fg='#28159E',cursor='hand2')
		self.Link_Modificar.configure(underline=1)
		self.Link_Modificar.bind('<Button-1>',self.top_Modificar)
		self.Link_Modificar.place(x=20,y=370)	
	def llenar_TablePacientes(self):
		
		rows=self.obj_ConsultaTriaje.Consulta_DatosPaciente()
		for valores in rows:
			self.table_General.insert('','end',values=(valores.dni,valores.Nombre,valores.Apellido_Paterno,valores.Apellido_Materno,valores.Telefono,valores.Procedencia))
	def search_paciente(self,event):
		parametro=''
		self.borrar_tabla()
		if len(self.Entry_buscar_General.get())!=0:
			parametro=parametro+self.Entry_buscar_General.get()
			rows=self.obj_ConsultaTriaje.Consulta_DatosPacienteLIKE(parametro)
			for valores in rows:
				self.table_General.insert('','end',values=(valores.dni,valores.Nombre,valores.Apellido_Paterno,valores.Apellido_Materno,valores.Telefono,valores.Procedencia))

	def borrar_tabla(self):
		for item in self.table_General.get_children():
			self.table_General.delete(item)

	def top_Modificar(self,event):

		dni=''
		try:
			dni=self.table_General.item(self.table_General.selection()[0],option='values')[0]
		except Exception as e:
			messagebox.showerror('Error',f'Seleccione un item {e}') 
		
		if len(dni)!=0:

			self.ventana_UpdatePaciente=Toplevel()
			self.ventana_UpdatePaciente.geometry('500x300')
			#self.ventana_Paciente.attributes('-topmost',True)
			self.ventana_UpdatePaciente.iconbitmap('img/actualizar.ico')
			self.ventana_UpdatePaciente.title('Modificar datos del Paciente')
			self.ventana_UpdatePaciente.grab_set()
			etiqueta_nombre=Label(self.ventana_UpdatePaciente,text='Nombres: ',font=self.font_text,fg='#105B79')
			etiqueta_nombre.grid(row=2,column=0,pady=10)
			self.Entry_UNombre=ttk.Entry(self.ventana_UpdatePaciente,width=50)
			self.Entry_UNombre.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[1])
			self.Entry_UNombre.grid(row=2,column=1,columnspan=3,pady=10)

			etiqueta_apellidoP=Label(self.ventana_UpdatePaciente,text='Ap. Paterno: ',font=self.font_text,fg='#105B79')
			etiqueta_apellidoP.grid(row=3,column=0)
			self.Entry_UapellidoP=ttk.Entry(self.ventana_UpdatePaciente,width=50)
			self.Entry_UapellidoP.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[2])
			self.Entry_UapellidoP.grid(row=3,column=1,columnspan=3,pady=6)

			etiqueta_apellidoM=Label(self.ventana_UpdatePaciente,text='Ap. Materno: ',font=self.font_text,fg='#105B79')
			etiqueta_apellidoM.grid(row=4,column=0)
			self.Entry_UapellidoM=ttk.Entry(self.ventana_UpdatePaciente,width=50)
			self.Entry_UapellidoM.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[3])
			self.Entry_UapellidoM.grid(row=4,column=1,columnspan=3,pady=6)

			etiqueta_Telefono=Label(self.ventana_UpdatePaciente,text='Telefono: ',font=self.font_text,fg='#105B79')
			etiqueta_Telefono.grid(row=5,column=0,pady=6)
			self.Entry_UTelefono=ttk.Entry(self.ventana_UpdatePaciente,width=50)
			self.Entry_UTelefono.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[4])
			self.Entry_UTelefono.grid(row=5,column=1,columnspan=3,pady=6)

			etiqueta_Procedencia=Label(self.ventana_UpdatePaciente,text='Procedencia: ',font=self.font_text,fg='#105B79')
			etiqueta_Procedencia.grid(row=6,column=0,pady=6)
			self.Entry_UProcedencia=ttk.Entry(self.ventana_UpdatePaciente,width=50)
			self.Entry_UProcedencia.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[5])
			self.Entry_UProcedencia.grid(row=6,column=1,columnspan=3,pady=6)		

			self.btn_UGuardar=ttk.Button(self.ventana_UpdatePaciente,text='ACTUALIZAR')
			self.btn_UGuardar['command']=self.update_DatosGenerales
			self.btn_UGuardar.grid(row=10,column=2)	

			self.btn_UCancelar=ttk.Button(self.ventana_UpdatePaciente,text='CANCELAR')
			self.btn_UCancelar['command']=self.ventana_UpdatePaciente.destroy
			self.btn_UCancelar.grid(row=10,column=3)
	
	def update_DatosGenerales(self):
		dni=self.table_General.item(self.table_General.selection()[0],option='values')[0]
		nombre=self.Entry_UNombre.get()
		apellidoP=self.Entry_UapellidoP.get()
		apellidoM=self.Entry_UapellidoM.get()
		telefono=self.Entry_UTelefono.get()
		procedencia=self.Entry_UProcedencia.get()
		try:
			self.obj_ConsultaTriaje.Update_Pacientes(dni,nombre,apellidoP,apellidoM,telefono,procedencia)
			messagebox.showinfo('Alerta','Se Actualizó correctamente')
			self.ventana_UpdatePaciente.destroy()
			self.TopVisualizar.destroy()
		except Exception as e:
			messagebox.showerror('Error',f'error al insertar {e}') 
		
		

