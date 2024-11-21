from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import Consulta_Galen
import Consulta_Triaje

class IncidenciasV(object):	

	def __init__(self,usuario):
		self.controlador=None		
		self.usuario=usuario
		self.letra=('Arial',14,'bold')
		self.obj_ConsultaTriaje=Consulta_Triaje.queryTriaje()
		self.obj_ConsultaGalen=Consulta_Galen.queryGalen()
		style=ttk.Style()
		style.theme_use("alt")
	def Incidencias(self,frame,width,height):		
		self.width,self.height=width,height
		self.left_Frame=Frame(frame,width=int(width*0.13),height=int(height*0.85),bg="#1F305D")
		self.left_Frame.place(x=5,y=10)
		self.main_Frame=Frame(frame,width=int(width*0.80),height=int(height*0.85),bg="#1F305D")
		self.main_Frame.place(x=int(width*0.15),y=10)
		self.Menu_Button()

	def Menu_Button(self):
		self.btn_Incidencias=ttk.Button(self.left_Frame,text='Insertar Incidencias',cursor="hand2")
		self.btn_Incidencias['command']=self.frame_Incidencias
		self.btn_Incidencias.place(x=5,y=20)		

		self.btn_Reporte=ttk.Button(self.left_Frame,text='Reporte Incidencias',cursor="hand2")
		self.btn_Reporte['command']=self.frame_ReporteIncidencias
		self.btn_Reporte.place(x=5,y=80)

	def frame_Incidencias(self):

		frameIncidencias=Frame(self.main_Frame,width=int(self.width*0.798),height=int(self.height*0.847),bg="#1F305D",highlightbackground="black", highlightthickness=2)
		frameIncidencias.place(x=0,y=0)

		label=Label(frameIncidencias,text="Dni :",font=self.letra,bg="#1F305D",fg="#fff")
		label.place(x=15,y=10)
		self.entry_dni=ttk.Entry(frameIncidencias,width=40)
		self.entry_dni.bind("<Return>",self.Insertar_Paciente)
		self.entry_dni.place(x=150,y=10)

		label=Label(frameIncidencias,text="Nombres :",font=self.letra,bg="#1F305D",fg="#fff")
		label.place(x=15,y=60)
		self.entry_Nombres=ttk.Entry(frameIncidencias,width=40)
		self.entry_Nombres.place(x=150,y=60)

		label=Label(frameIncidencias,text="Apellidos :",font=self.letra,bg="#1F305D",fg="#fff")
		label.place(x=15,y=110)
		self.entry_Apellidos=ttk.Entry(frameIncidencias,width=40)
		self.entry_Apellidos.place(x=150,y=110)

		label=Label(frameIncidencias,text="Fecha :",font=self.letra,bg="#1F305D",fg="#fff")
		label.place(x=15,y=160)
		self.date_fecha=DateEntry(frameIncidencias,selectmode='day')
		#self.date_fecha.bind("<<DateEntrySelected>>",self.dateEvent)
		self.date_fecha.place(x=150,y=160)		

		label=Label(frameIncidencias,text="Turno :",font=self.letra,bg="#1F305D",fg="#fff")
		label.place(x=450,y=10)
		self.Turno=ttk.Combobox(frameIncidencias,values=["Mañana","Tarde","Noche"],width=40)		
		self.Turno.current(0)
		self.Turno.place(x=570,y=10)		

		label=Label(frameIncidencias,text="Fuente :",font=self.letra,bg="#1F305D",fg="#fff")
		label.place(x=450,y=60)
		self.Fuente=ttk.Combobox(frameIncidencias,width=40)
		finaciamientos=[val.Descripcion for val in self.obj_ConsultaGalen.query_financiamiento()]		
		self.Fuente.configure(values=finaciamientos)
		self.Fuente.current(1)
		self.Fuente.place(x=570,y=60)


		label=Label(frameIncidencias,text="Procedencia :",font=self.letra,bg="#1F305D",fg="#fff")
		label.place(x=450,y=110)
		self.Entry_Procedencia=ttk.Entry(frameIncidencias,width=40)
		self.Entry_Procedencia.place(x=570,y=110)		

		label=Label(frameIncidencias,text="Especialidad :",font=self.letra,bg="#1F305D",fg="#fff")
		label.place(x=15,y=210)
		self.Especialidad=Listbox(frameIncidencias,width=40)
		datosEspecialidades=[val.Nombre for val in self.obj_ConsultaGalen.query_EspecialidadesCEXT()]

		for num,valor in enumerate(datosEspecialidades):
			self.Especialidad.insert(num,valor)

		self.Especialidad.selection_set(0)
		self.Especialidad.place(x=150,y=210)

		label=Label(frameIncidencias,text="Historia CL. :",font=self.letra,bg="#1F305D",fg="#fff")
		label.place(x=450,y=210)
		self.entry_HistoriaCL=ttk.Entry(frameIncidencias,width=40)
		self.entry_HistoriaCL.place(x=570,y=210)		

		label=Label(frameIncidencias,text="Motivo :",font=self.letra,bg="#1F305D",fg="#fff")
		label.place(x=10,y=400)
		self.Text_Motivo=Text(frameIncidencias,width=90,height=10)
		self.Text_Motivo.place(x=150,y=400)

		btn_Aceptar=ttk.Button(frameIncidencias,text="Aceptar")
		btn_Aceptar['command']=self.InsertarIncidentes
		btn_Aceptar.place(x=200,y=600)

		btn_Cancelar=ttk.Button(frameIncidencias,text="Cancelar")
		btn_Cancelar.place(x=450,y=600)

		self.valorCheck=IntVar()
		CheckNuevo=Checkbutton(frameIncidencias,variable=self.valorCheck,text='Nuevo',onvalue=1,offvalue=0)
		CheckNuevo.place(x=450,y=570)

	def Insertar_Paciente(self,event):
		try:
			dni=self.entry_dni.get()			
			if len(dni)==8:
				
				rows_Galen=self.obj_ConsultaGalen.query_Paciente(dni)
				rows_Triaje=self.obj_ConsultaTriaje.query_Paciente(dni)
				
				ident=True
				if len(rows_Galen)!=0:
					self.entry_Nombres.insert(0,rows_Galen[0].PrimerNombre)
					self.entry_Nombres['state']='readonly'
					self.entry_Apellidos.insert(0,"{}--{}".format(rows_Galen[0].ApellidoPaterno,rows_Galen[0].ApellidoMaterno))
					self.entry_Apellidos['state']='readonly'
					self.entry_HistoriaCL.insert(0,rows_Galen[0].NroHistoriaClinica)
					self.entry_HistoriaCL.configure(state='readonly')
					self.Entry_Procedencia.insert(0,rows_Galen[0].Nombre)
					self.Entry_Procedencia.configure(state="readonly")
					self.controlador=True

				elif len(rows_Triaje)!=0:
					self.entry_Nombres.insert(0,rows_Triaje[0].Nombre)
					self.entry_Nombres['state']='readonly'
					self.entry_Apellidos.insert(0,"{}--{}".format(rows_Triaje[0].Apellido_Paterno,rows_Triaje[0].Apellido_Materno))
					self.entry_Apellidos['state']='readonly'						
					self.Entry_Procedencia.insert(0,rows_Triaje[0].Procedencia)
					self.Entry_Procedencia.configure(state="readonly")
					self.controlador=True
				else:
					messagebox.showinfo('Notificación','Paciente Nuevo, Registre en la seccion de Pacientes')
					self.entry_dni.delete(0,'end')
		except Exception as e:
			messagebox.showerror("Alerta","Ingrese un DNI valido!!")


	def InsertarIncidentes(self):
		datos=[]
		hc_=' '
		procedencia_=' '
		valorCheck=self.valorCheck.get()
		dni_=self.entry_dni.get()
		hc_=self.entry_HistoriaCL.get()
		Especialidad=self.Especialidad.get(self.Especialidad.curselection())
		turno_=self.Turno.get()
		fuente_=self.Fuente.get()
		procedencia_=self.Entry_Procedencia.get()
		motivo_=self.Text_Motivo.get(1.0,"end")
		fecha=self.date_fecha.get_date()
		#recuperando id usuario.
		rows_usuario=self.obj_ConsultaTriaje.query_UserName(self.usuario)
		Id_user=rows_usuario[0].Id_Usuario

		#recuperando id fuente
		rows_fuente=self.obj_ConsultaTriaje.consulta_FuenteId(fuente_)
		Id_Fuente=rows_fuente[0].idFuente

		#recuperando incidencias...
		IDINCIDENCIAS=self.obj_ConsultaTriaje.getId_Incidencias()[0].IDINCIDENCIA
		idvalor=0
		if IDINCIDENCIAS!=None:
			idvalor=IDINCIDENCIAS+1

		datos=[idvalor,Id_user,dni_,hc_,Especialidad,turno_,Id_Fuente,procedencia_,motivo_,fecha]
		if valorCheck:
			
			nombres=self.entry_Nombres.get()
			apellidos=self.entry_Apellidos.get()
			apellidoPaterno=apellidos[:apellidos.find(" ")]
			ApellidoMaterno=apellidos[apellidos.find(" ")+1:]
			datos_paciente={'dni':dni_,'nombres':nombres,'apellidoP':apellidoPaterno,'apellidoM':ApellidoMaterno,'telefono':' ','procedencia':procedencia_}
			
			rows_count=self.obj_ConsultaTriaje.Insert_Paciente(datos_paciente)
			if rows_count==1:
				
				if len(datos)==10:
					nro=self.obj_ConsultaTriaje.insert_Incidencias(datos)
					if nro==1:
						messagebox.showinfo("Alerta","Se insertó correctamente!!")
						self.borrarCampos()
						#self.frame_ReporteIncidencias()
				else:
					messagebox.error("Error","Ingrese todos los campos!!")
			else:
				messagebox.showinfo("Alerta","No pudo Insertarse, el paciente, inserte en el apartado Paciente!")
			
		else:			
			if self.controlador:
				if len(datos)==10:
					nro=self.obj_ConsultaTriaje.insert_Incidencias(datos)
					if nro==1:
						messagebox.showinfo("Alerta","Se insertó correctamente!!")
						self.borrarCampos()						
				else:
					messagebox.showinfo("Alerta","Ingrese todos los campos!")
			else:
				messagebox.showinfo("Alerta","Datos no encontrados, marque la casilla de nuevo paciente!!")
	def borrarCampos(self):
		self.entry_dni.delete(0,"end")
		self.entry_Nombres.configure(state="normal")
		self.entry_Nombres.delete(0,"end")
		self.entry_HistoriaCL.configure(state="normal")
		self.entry_HistoriaCL.delete(0,"end")
		self.Entry_Procedencia.configure(state="normal")
		self.Entry_Procedencia.delete(0,"end")
		self.Text_Motivo.delete("1.0","end")

	def frame_ReporteIncidencias(self):
		frameIncidenciasReporte=Frame(self.main_Frame,width=int(self.width*0.798),height=int(self.height*0.847),bg="#1F305D",highlightbackground="black", highlightthickness=2)
		frameIncidenciasReporte.place(x=0,y=0)

		label=Label(frameIncidenciasReporte,text="Desde :",font=self.letra,bg='#1F305D',fg='#fff')
		label.place(x=10,y=20)
		self.fecha_Inicio=DateEntry(frameIncidenciasReporte,selectmode='day')
		self.fecha_Inicio.place(x=100,y=20)

		label=Label(frameIncidenciasReporte,text="Hasta :",font=self.letra,bg='#1F305D',fg='#fff')
		label.place(x=250,y=20)
		self.fecha_Fin=DateEntry(frameIncidenciasReporte,selectmode='day')
		self.fecha_Fin.bind("<<DateEntrySelected>>",self.dateEvent)
		self.fecha_Fin.place(x=350,y=20)
		#check
		self.CheckReport=IntVar()
		CheckNuevo=Checkbutton(frameIncidenciasReporte,variable=self.CheckReport,text='Buscar',onvalue=1,offvalue=0)
		CheckNuevo['command']=self.eventCheck
		CheckNuevo.place(x=500,y=25)

		self.Entry_SearchReport=ttk.Entry(frameIncidenciasReporte)
		self.Entry_SearchReport.place(x=600,y=20)
		self.Entry_SearchReport.bind("<Key>",self.searchEventReport)
		self.Entry_SearchReport['state']='readonly'


		#Tabla...
		style=ttk.Style()
		style.theme_use("default")
		style.configure("Treeview",background="silver",foreground="black",rowheight=25,fieldbackground="silver")
		style.map('Treeview',background=[('selected','green')])
		self.table_General=ttk.Treeview(frameIncidenciasReporte,columns=('#1','#2','#3','#4','#5','#6'),show='headings')
		self.table_General.heading("#1",text="")
		self.table_General.column("#1",width=0,stretch='no')		
		self.table_General.heading("#2",text="Dni")
		self.table_General.column("#2",width=100,anchor="center")
		self.table_General.heading("#3",text="Nombres")
		self.table_General.column("#3",width=int(self.width*0.10),anchor="center")
		self.table_General.heading("#4",text="Apellidos")
		self.table_General.column("#4",width=int(self.width*0.10),anchor="center")		
		self.table_General.heading("#5",text="Especialidad")
		self.table_General.column("#5",width=int(self.width*0.19),anchor="center")
		self.table_General.heading("#6",text="Fecha")
		self.table_General.column("#6",width=int(self.width*0.05),anchor="center")									
		self.table_General.place(x=10,y=70,width=int(self.width*0.7),height=290)


		label=Label(frameIncidenciasReporte,text="Reporte General",fg='#fff',bg='#1F305D',cursor='hand2',font=("Comic Sans MS", 12, "italic"))
		label.place(x=400,y=400)
		label.bind("<Button-1>",lambda event:self.GenerarGeporteNoAtendidos(event,'GENERAL'))

		label=Label(frameIncidenciasReporte,text="Reporte filtrado",fg='#fff',bg='#1F305D',cursor='hand2',font=("Comic Sans MS", 12, "italic"))
		label.place(x=600,y=400)
		label.bind("<Button-1>",lambda event:self.GenerarGeporteNoAtendidos(event,'FILTRADO'))
	

	def GenerarGeporteNoAtendidos(self,event,indicador):
		fechaI=self.fecha_Inicio.get_date()
		fecha_fin=self.fecha_Fin.get_date()
		from reporteIncidencias import Reporte
		obj_reporte=Reporte()
		rows=obj_reporte.Genera_RDatos(fechaI,fecha_fin,indicador)

	def dateEvent(self,event):
		if not self.CheckReport.get():
			self.borrar_tabla()
			fecha_inicio=self.fecha_Inicio.get_date()
			fecha_fin=self.fecha_Fin.get_date()
			rows=self.obj_ConsultaTriaje.query_IncidenciaFechas(fecha_inicio,fecha_fin)
			
			for val in rows:
				dni_paciente=val.Dni_Paciente
				rows_Galen=self.obj_ConsultaGalen.query_Paciente(dni_paciente)
				rows_Triaje=self.obj_ConsultaTriaje.query_Paciente(dni_paciente)
				nombres=''
				apellidoP=''
				apellidoM=''
				for valG in rows_Galen:
					nombres=valG.PrimerNombre
					apellidoP=valG.ApellidoPaterno
					apellidoM=valG.ApellidoMaterno
				for valT in rows_Triaje:
					nombres=valT.Nombre
					apellidoP=valT.Apellido_Paterno
					apellidoM=valT.Apellido_Materno
				self.table_General.insert('','end',values=(val.Id_Incidencia,dni_paciente,nombres,apellidoP+" "+apellidoM,val.Especialidad,val.Fecha))


	def searchEventReport(self,event):
		param=''
		param=param+self.Entry_SearchReport.get()		
		rows=self.obj_ConsultaTriaje.query_IncidenciasLike(param)
		self.borrar_tabla()
		for val in rows:
			dni_paciente=val.Dni_Paciente
			rows_Galen=self.obj_ConsultaGalen.query_Paciente(dni_paciente)
			rows_Triaje=self.obj_ConsultaTriaje.query_Paciente(dni_paciente)
			nombres=''
			apellidoP=''
			apellidoM=''
			for valG in rows_Galen:
				nombres=valG.PrimerNombre
				apellidoP=valG.ApellidoPaterno
				apellidoM=valG.ApellidoMaterno
			for valT in rows_Triaje:
				nombres=valT.Nombre
				apellidoP=valT.Apellido_Paterno
				apellidoM=valT.Apellido_Materno
			self.table_General.insert('','end',values=(val.Id_Incidencia,dni_paciente,nombres,apellidoP+" "+apellidoM,val.Especialidad,val.Fecha))

	def borrar_tabla(self):
		for item in self.table_General.get_children():
			self.table_General.delete(item)

	def eventCheck(self):
		if self.CheckReport.get()==1:			
			self.Entry_SearchReport.configure(state='normal')
			self.Entry_SearchReport.delete(0,'end')
			self.borrar_tabla()
		else:
			
			self.Entry_SearchReport.configure(state='normal')
			self.Entry_SearchReport.delete(0,'end')
			self.Entry_SearchReport.configure(state='readonly')
			self.borrar_tabla()


	
	