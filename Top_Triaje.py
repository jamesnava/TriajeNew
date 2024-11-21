from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import Consulta_Galen
import Consulta_Triaje

class Triaje(object):
	def __init__(self):
		self.font_text=('Candara',12,'bold')
		self.obj_ConsultaGalen=Consulta_Galen.queryGalen()
		self.obj_ConsultaTriaje=Consulta_Triaje.queryTriaje()
		self.controlador=False
		self.ventana_Triaje=None
		self.btnAceptarphoto = PhotoImage(file ="img/aceptarbtn.png")
		self.btnCancelphoto = PhotoImage(file ="img/btncancelar.png")

	def Top_Agregar(self,cupo,servicio,medico,usuario,fecha_Atencion,turno,tipocupo,cod_servicio,dni_medico):
		self.turno=turno
		self.usuario=usuario
		self.etiqueta_Cupo=cupo		
		self.ventana_Triaje=Toplevel()
		self.ventana_Triaje.geometry('750x450+0+100')
		#self.ventana_Triaje.attributes('-topmost',True)
		self.ventana_Triaje.iconbitmap('img/cita.ico')
		self.ventana_Triaje.title('Agregar Cita')

		etiqueta_nombre=Label(self.ventana_Triaje,text='Dni: ',font=self.font_text,fg='#105B79')
		etiqueta_nombre.grid(row=1,column=0,pady=10)
		self.Entry_Dni=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_Dni.bind('<Return>',lambda event,cupo=cupo,servicio=servicio,medico=medico,fecha_Atencion=fecha_Atencion:self.search_Paciente(event,cupo,servicio,medico,fecha_Atencion))
		self.Entry_Dni.bind('<Button-1>',self.borrado_widget)
		self.Entry_Dni.grid(row=1,column=1,pady=10)

		etiqueta_nombre=Label(self.ventana_Triaje,text='Nombre: ',font=self.font_text,fg='#105B79')
		etiqueta_nombre.grid(row=2,column=0,pady=10)
		self.Entry_Nombre=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_Nombre.grid(row=2,column=1,pady=10)

		etiqueta_apellidoP=Label(self.ventana_Triaje,text='Ap. Paterno: ',font=self.font_text,fg='#105B79')
		etiqueta_apellidoP.grid(row=3,column=0)
		self.Entry_apellidoP=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_apellidoP.grid(row=3,column=1,pady=6)

		etiqueta_apellidoM=Label(self.ventana_Triaje,text='Ap. Materno: ',font=self.font_text,fg='#105B79')
		etiqueta_apellidoM.grid(row=4,column=0)
		self.Entry_apellidoM=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_apellidoM.grid(row=4,column=1,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='Registrador: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=5,column=0,pady=6)
		self.Entry_Usuario=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_Usuario.grid(row=5,column=1,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='Nro Cupo: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=6,column=0,pady=6)
		self.Entry_NroCupo=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_NroCupo.grid(row=6,column=1,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='Continuador: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=7,column=0,pady=6)

		self.current_var=StringVar()
		self.Combo_Conti=ttk.Combobox(self.ventana_Triaje,textvariable=self.current_var,state='readonly',width=28)		
		self.Combo_Conti["values"]=["SI","NO"]
		self.Combo_Conti.current(0)
		self.Combo_Conti.grid(row=7,column=1,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='Historia: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=8,column=0,pady=6)
		self.Entry_HCL=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_HCL.grid(row=8,column=1,pady=6)

		#segunda columna
		etiqueta_usuario=Label(self.ventana_Triaje,text='FF.TTO: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=1,column=3,pady=6)
		self.Combo_fftto=ttk.Combobox(self.ventana_Triaje,state='readonly',width=28)		
		self.Combo_fftto.bind('<<ComboboxSelected>>',self.evento_SeleccionCombo)		
		self.Combo_fftto.grid(row=1,column=4,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='Nro Referencia: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=2,column=3,pady=6)
		self.Entry_NroReferencia=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_NroReferencia.grid(row=2,column=4,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='FUA: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=3,column=3,pady=6)
		self.Combo_FUA=ttk.Combobox(self.ventana_Triaje,state='readonly',width=28)
		self.Combo_FUA['values']=['SI','NO']
		self.Combo_FUA.current(1)
		self.Combo_FUA.grid(row=3,column=4,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='Telefono: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=4,column=3,pady=6)
		self.Entry_Telefono=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_Telefono.grid(row=4,column=4,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='Medico: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=5,column=3,pady=6)
		self.Entry_Medico=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_Medico.grid(row=5,column=4,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='Consultorio: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=6,column=3,pady=6)
		self.Entry_Consultorio=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_Consultorio.grid(row=6,column=4,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='Fecha A: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=7,column=3,pady=6)
		self.Entry_Fecha=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_Fecha.grid(row=7,column=4,pady=6)

		etiqueta_usuario=Label(self.ventana_Triaje,text='Establecimiento: ',font=self.font_text,fg='#105B79')
		etiqueta_usuario.grid(row=8,column=3,pady=6)
		self.Entry_Puesto=ttk.Entry(self.ventana_Triaje,width=30)
		self.Entry_Puesto['state']="readonly"
		self.Entry_Puesto.grid(row=8,column=4,pady=6)

		self.btn_searchEstablecimiento=ttk.Button(self.ventana_Triaje,text='...')
		self.btn_searchEstablecimiento['command']=self.Top_searchEstablecimiento
		self.btn_searchEstablecimiento.grid(row=8,column=5,padx=5)

		
		self.btn_Guardar=Button(self.ventana_Triaje,image=self.btnAceptarphoto,borderwidth=0,cursor='hand2')
		self.btn_Guardar['command']=lambda:self.registrar_cita(tipocupo,cod_servicio,dni_medico)
		self.btn_Guardar.grid(row=10,column=1)		

		self.btn_Cancelar=Button(self.ventana_Triaje,image=self.btnCancelphoto,borderwidth=0,cursor='hand2')
		self.btn_Cancelar['command']=self.ventana_Triaje.destroy
		self.btn_Cancelar.grid(row=10,column=3)		
		self.ventana_Triaje.grab_set()	
		
	def search_Paciente(self,event,label,servicio,medico,fecha_Atencion):

		try:
			
			dni=self.Entry_Dni.get()
			if len(dni)!=0:
				consulta_citas=self.obj_ConsultaTriaje.query_PacienteCuposLast(dni)

				for valoresConsulta in consulta_citas:
					messagebox.showinfo('Agendas',f'''Tiene Atenciones Pendientes en:\nConsultorio: {valoresConsulta.Especialidad}\nFecha Ate: {valoresConsulta.Fecha_Atencion}\nCupo : {valoresConsulta.Nro_Cupo}''')

				self.controlador=True
				rows=self.obj_ConsultaGalen.query_Paciente(dni)
				rows_Triaje=self.obj_ConsultaTriaje.query_Paciente(dni)
				ident=True
				if len(rows)!=0:
					self.Entry_Nombre.insert(0,rows[0][1])
					self.Entry_Nombre.configure(state='readonly')
					self.Entry_apellidoP.insert(0,rows[0][2])
					self.Entry_apellidoP.configure(state='readonly')
					self.Entry_apellidoM.insert(0,rows[0][3])
					self.Entry_apellidoM.configure(state='readonly')
					self.Entry_NroCupo.insert(0,label.cget('text'))
					self.Entry_NroCupo.configure(state='readonly')
					self.Entry_Medico.insert(0,medico)
					self.Entry_Medico.configure(state='readonly')
					self.Entry_Consultorio.insert(0,servicio)
					self.Entry_Consultorio.configure(state='readonly')
					self.Entry_Usuario.insert(0,self.usuario)
					self.Entry_Usuario.configure(state='readonly')
					self.Entry_Fecha.insert(0,fecha_Atencion)
					self.Entry_Fecha.configure(state='readonly')
					self.Entry_HCL.insert(0,rows[0][21])
					self.Entry_HCL.configure(state='readonly')
					
					self.llenar_comboFinanciamiento()					
					ident=False
				elif len(rows_Triaje)!=0 and ident:
					self.controlador=True					
					self.Entry_Nombre.insert(0,rows_Triaje[0][1])
					self.Entry_Nombre.configure(state='readonly')
					self.Entry_apellidoP.insert(0,rows_Triaje[0][2])
					self.Entry_apellidoP.configure(state='readonly')
					self.Entry_apellidoM.insert(0,rows_Triaje[0][3])
					self.Entry_apellidoM.configure(state='readonly')
					self.Entry_Telefono.insert(0,rows_Triaje[0][4])					
					self.Entry_NroCupo.insert(0,label.cget('text'))
					self.Entry_NroCupo.configure(state='readonly')	
					self.Entry_Medico.insert(0,medico)
					self.Entry_Medico.configure(state='readonly')
					self.Entry_Consultorio.insert(0,servicio)
					self.Entry_Consultorio.configure(state='readonly')
					self.Entry_Usuario.insert(0,self.usuario)
					self.Entry_Usuario.configure(state='readonly')
					self.Entry_Fecha.insert(0,fecha_Atencion)
					self.Entry_Fecha.configure(state='readonly')
										
					self.llenar_comboFinanciamiento()									
				else:
					messagebox.showinfo('Alerta','Paciente Nuevo, Registre en la sección de Pacientes')
					self.Entry_Dni.delete(0,'end')
			else:
				messagebox.showinfo('Notificación','Ingrese el numero DNI del paciente')
		except Exception as e:
			raise e

	def borrado_widget(self,event):
		self.Activar_widget()
		self.controlador=False
		self.Entry_Dni.delete(0,'end')
		self.Entry_Nombre.delete(0,'end')
		self.Entry_apellidoP.delete(0,'end')
		self.Entry_apellidoM.delete(0,'end')		
		self.Entry_Puesto.delete(0,'end')
		self.Entry_Medico.delete(0,'end')
		self.Entry_Usuario.delete(0,'end')
		self.Entry_NroCupo.delete(0,'end')
		self.Entry_NroReferencia.delete(0,'end')
		self.Entry_Consultorio.delete(0,'end')
		self.Entry_Telefono.delete(0,'end')
		self.Entry_Fecha.delete(0,'end')
		self.Entry_HCL.delete(0,'end')
		self.Entry_Puesto.configure(state="readonly")
	def borrado_widget1(self):
		self.Activar_widget()
		self.controlador=False
		self.Entry_Dni.delete(0,'end')
		self.Entry_Nombre.delete(0,'end')
		self.Entry_apellidoP.delete(0,'end')
		self.Entry_apellidoM.delete(0,'end')		
		self.Entry_Puesto.delete(0,'end')
		self.Entry_Medico.delete(0,'end')
		self.Entry_Usuario.delete(0,'end')
		self.Entry_NroCupo.delete(0,'end')
		self.Entry_NroReferencia.delete(0,'end')
		self.Entry_Consultorio.delete(0,'end')
		self.Entry_Telefono.delete(0,'end')
		self.Entry_Fecha.delete(0,'end')
		self.Entry_NroReferencia.delete(0,'end')
		self.Entry_HCL.delete(0,'end')
	def Activar_widget(self):
		self.Entry_Nombre.configure(state='NORMAL')
		self.Entry_apellidoP.configure(state='NORMAL')
		self.Entry_apellidoM.configure(state='NORMAL')		
		self.Entry_Puesto.configure(state='NORMAL')
		self.Entry_Medico.configure(state='NORMAL')
		self.Entry_Usuario.configure(state='NORMAL')
		self.Entry_Usuario.configure(state='NORMAL')
		self.Entry_NroReferencia.configure(state='NORMAL')
		self.Entry_Telefono.configure(state='NORMAL')
		self.Entry_Fecha.configure(state='NORMAL')
		self.Entry_Consultorio.configure(state='NORMAL')
		self.Entry_NroCupo.configure(state='NORMAL')
		self.Entry_HCL.configure(state='NORMAL')
		self.Entry_NroReferencia.configure(state='NORMAL')

	def registrar_cita(self,tipocupo,idservicio,dni_medico):

		nro_Referencia="0"
		puesto=""
		telefono="0"
		#obteniendo datos del usuario
		id_user=0
		rows=self.obj_ConsultaTriaje.query_UserName(self.usuario)
		for val in rows:
			id_user=val.Id_Usuario
		#recuperando datos
		self.Activar_widget()
		dni=self.Entry_Dni.get()
		nro_cupo=self.Entry_NroCupo.get()
		nro_Referencia=self.Entry_NroReferencia.get()
		medico=self.Entry_Medico.get()
		consultorio=self.Entry_Consultorio.get()
		fecha_A=self.Entry_Fecha.get()
		telefono=self.Entry_Telefono.get()
		self.Entry_Puesto["state"]="normal"
		establecimiento=self.Entry_Puesto.get()
		usuario=self.Entry_Usuario.get()
		continuador=self.Combo_Conti.get()
		Historia=self.Entry_HCL.get()
		FUA=self.Combo_FUA.get()
		#obteniendo id de financiamiento
		fftto=self.Combo_fftto.get()		
		if len(nro_Referencia)==0:
			nro_Referencia='0'
		if len(telefono)==0:
			telefono='0'
		
		lista_fuente=self.obj_ConsultaTriaje.consulta_FuenteId(fftto)		
		for val in lista_fuente:
			id_fuente=val.idFuente

		if self.controlador and len(consultorio)!=0:
			
			rows=self.obj_ConsultaTriaje.query_AgendadoXUsuario(fecha_A,consultorio,dni)
			if len(rows)==0:
				try:
					cup=int(self.etiqueta_Cupo.cget('text'))

					#comprobando si el cupo esta ocupado
					rowsExist=self.obj_ConsultaTriaje.query_CupoOcupado(cup,medico,consultorio,self.turno,fecha_A)
					if rowsExist[0].NRO:
						messagebox.showerror("Error","El cupo ya fué asignada, seleccione otro")
						self.ventana_Triaje.destroy()

					else:
						if cup<=30 and (id_fuente==1 or id_fuente==2):
							self.obj_ConsultaTriaje.Insert_Cita(id_user,dni,id_fuente,nro_cupo,nro_Referencia,medico,consultorio,fecha_A,telefono,establecimiento,continuador,FUA,Historia,self.turno,tipocupo,idservicio,dni_medico)							
							self.borrado_widget1()
							messagebox.showinfo('Notificación','se guardó de manera exitosa')
							if tipocupo==1:
								self.etiqueta_Cupo.configure(bg='red')
							else:
								self.etiqueta_Cupo.configure(bg='#340563')
								
						
						elif (cup>30 and cup<37) and id_fuente==3:
							self.obj_ConsultaTriaje.Insert_Cita(id_user,dni,id_fuente,nro_cupo,nro_Referencia,medico,consultorio,fecha_A,telefono,establecimiento,continuador,FUA,Historia,self.turno,tipocupo,idservicio,dni_medico)
							self.borrado_widget1()
							messagebox.showinfo('Notificación','se guardó de manera exitosa')
							self.etiqueta_Cupo.configure(fg='red')
						else:
							messagebox.showinfo('Alerta','Verifique que la fuente de finaciamiento corresponda, e intentelo otra vez!')					

						self.ventana_Triaje.destroy()
				except Exception as e:
					print(e)
				
			else:
				messagebox.showinfo('Notificación','El Paciente ya tiene una cita')
		else:
			messagebox.showinfo('Notificación','Llene los campos')
			
	def Top_searchEstablecimiento(self):
		self.TopGeneral=Toplevel(self.ventana_Triaje)
		self.TopGeneral.title('Establecimientos')
		self.TopGeneral.iconbitmap('img/centro.ico')
		self.TopGeneral.geometry("720x400+350+50")
		self.TopGeneral.focus_set()	
		self.TopGeneral.grab_set()
		self.TopGeneral.resizable(0,0)	

		label_title=Label(self.TopGeneral,text='Buscar')
		label_title.place(x=20,y=20)
		self.Entry_buscar_General=Entry(self.TopGeneral,width=30)
		self.Entry_buscar_General.focus()
		self.Entry_buscar_General.place(x=80,y=20)
		self.Entry_buscar_General.bind('<Key>',self.buscar_Establecimientos)		

		#tabla...
		self.table_General=ttk.Treeview(self.TopGeneral,columns=('#1','#2','#3','#4'),show='headings')		
		self.table_General.heading("#1",text="Establecimiento")
		self.table_General.column("#1",width=200,anchor="center")
		self.table_General.heading("#2",text="Distrito")
		self.table_General.column("#2",width=100,anchor="center")
		self.table_General.heading("#3",text="Provincia")
		self.table_General.column("#3",width=100,anchor="center")								
		self.table_General.place(x=10,y=70,width=700,height=290)
		self.table_General.bind('<<TreeviewSelect>>',self.itemTable_selected)			
		#botones de accion
		self.btn_TPG_Close=ttk.Button(self.TopGeneral,text='Cerrar')
		self.btn_TPG_Close.place(x=280,y=365)
		self.btn_TPG_Close['command']=lambda :self.TopGeneral.destroy()
	def buscar_Establecimientos(self,event):
		parametro=''
		self.borrar_tabla()
		if len(self.Entry_buscar_General.get())!=0:
			parametro=parametro+self.Entry_buscar_General.get()
			rows=self.obj_ConsultaGalen.query_Establecimiento(parametro)
			for valores in rows:
				self.table_General.insert('','end',values=(valores.Establecimiento,valores.Distrito,valores.Provincia))
				
	def itemTable_selected(self,event):
		if len(self.table_General.focus())!=0:
			self.Entry_Puesto.delete(0,'end')
			self.Entry_Puesto['state']="normal"
			self.Entry_Puesto.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
			self.Entry_Puesto['state']="readonly"	
			self.TopGeneral.destroy()

	def borrar_tabla(self):
		for item in self.table_General.get_children():
			self.table_General.delete(item)
	def evento_SeleccionCombo(self,event):
		valor=self.Combo_fftto.get()
		if valor=='SIS':
			self.Entry_NroReferencia.configure(state='NORMAL')
		else:
			self.Entry_NroReferencia.configure(state='readonly')

	def llenar_comboFinanciamiento(self):
		lista=[]
		rows=self.obj_ConsultaTriaje.consulta_Fuente()
		for val in rows:
			lista.append(val.fuente)
		self.Combo_fftto['values']=lista
		self.Combo_fftto.current(0)

	def search_Citas(self):
		self.ventana_Triaje_Buscar=Toplevel()
		self.ventana_Triaje_Buscar.geometry('1200x400+10+100')	
		self.ventana_Triaje_Buscar.iconbitmap('img/cita.ico')
		self.ventana_Triaje_Buscar.title('ATENCIONES')
		self.ventana_Triaje_Buscar.resizable(0,0)

		etiqueta_nombre=Label(self.ventana_Triaje_Buscar,text='DNI:',font=self.font_text,fg='#105B79')
		etiqueta_nombre.grid(row=1,column=0,pady=10)
		self.Entry_dniPaciente=ttk.Entry(self.ventana_Triaje_Buscar,width=30)
		self.Entry_dniPaciente.bind('<Return>',lambda event:self.buscar_Paciente(event))		
		self.Entry_dniPaciente.grid(row=1,column=1,pady=10)		
		self.ventana_Triaje_Buscar.grab_set()	

		self.table_Historial=ttk.Treeview(self.ventana_Triaje_Buscar,columns=('#1','#2','#3','#4','#5','#6','#7','#8'),show='headings')		
		self.table_Historial.heading("#1",text="PACIENTE")
		self.table_Historial.column("#1",width=300,anchor="center",stretch='NO')
		self.table_Historial.heading("#2",text="CONSULTORIO")
		self.table_Historial.column("#2",width=100,anchor="center",stretch='NO')
		self.table_Historial.heading("#3",text="NRO CUPO")
		self.table_Historial.column("#3",width=100,anchor="center",stretch='NO')
		self.table_Historial.heading("#4",text="MEDICO")
		self.table_Historial.column("#4",width=150,anchor="center",stretch='NO')		
		self.table_Historial.heading("#5",text="TURNO")
		self.table_Historial.column("#5",width=150,anchor="center",stretch='NO')
		self.table_Historial.heading("#6",text="FECHA")
		self.table_Historial.column("#6",width=100,anchor="center",stretch='NO')
		self.table_Historial.heading("#7",text="Regis. Por")
		self.table_Historial.column("#7",width=150,anchor="center",stretch='NO')
		self.table_Historial.heading("#8",text="Fec. Reg.")
		self.table_Historial.column("#8",width=150,anchor="center",stretch='NO')										
		self.table_Historial.place(x=10,y=70,width=1500,height=290)
		
	def buscar_Paciente(self,event):
		#dni=''
		dni=self.Entry_dniPaciente.get()				
		rows=self.obj_ConsultaTriaje.query_Atenciones(dni)
		for item in self.table_Historial.get_children():
			self.table_Historial.delete(item)
		for valores in rows:			
			nombres=''
			dni_paciente=valores.dni
			rowsG=self.obj_ConsultaGalen.query_DatosLIKEPaciente(dni)			
			for valor in rowsG:
				nombres=valor.PrimerNombre+' '+valor.ApellidoPaterno+' '+valor.ApellidoMaterno
			self.table_Historial.insert('','end',values=(nombres,valores.Especialidad,valores.Nro_Cupo,valores.Medico,valores.Turno,valores.Fecha_Atencion,valores.Usuario,str(valores.FechaR)[:16]))
		