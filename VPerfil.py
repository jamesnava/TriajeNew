from tkinter import *
from tkinter import ttk
from Consulta_Triaje import queryTriaje

class Perfiles(object):

	def __init__(self):
		self.obj_Consulta=queryTriaje()

	def Frame_perfiles(self,frame,width,height):
		self.Frame_Perfil=Frame(frame,width=width,height=height,background='#949BAA')
		self.Frame_Perfil.grid(row=1,column=1)
		self.Frame_Perfil.grid_propagate(False)

		style=ttk.Style()
		style.theme_use("default")
		style.configure("Treeview",background="silver",foreground="black",rowheight=25,fieldbackground="silver")
		style.map('Treeview',background=[('selected','green')])
		self.table_Perfiles=ttk.Treeview(self.Frame_Perfil,columns=('#1','#2'),show='headings',height=5)		
		self.table_Perfiles.heading("#1",text="CODIGO")
		self.table_Perfiles.column("#1",width=100,anchor="center")
		self.table_Perfiles.heading("#2",text="DESCRIPCION")
		self.table_Perfiles.column("#2",width=200,anchor="center")
		self.table_Perfiles.grid(row=0,column=1)
		self.table_Perfiles.bind("<Button-3>",self.EventTreeView)
		self.llenarTabla()

		marcoUsuario=LabelFrame(self.Frame_Perfil,text="Configuracion",borderwidth=2, relief="solid",bg="#949BAA")
		marcoUsuario.grid(row=1,column=1)
		
		self.checkPerfil=BooleanVar()
		Check=Checkbutton(marcoUsuario,text="Perfiles",variable=self.checkPerfil)
		Check.grid(row=1,column=1,padx=5,pady=5)

		self.checkAddUser=BooleanVar()
		Check=Checkbutton(marcoUsuario,text="Crea Usuario",variable=self.checkAddUser)
		Check.grid(row=1,column=2,padx=5,pady=5)

		self.CheckReportUser=BooleanVar()
		Check=Checkbutton(marcoUsuario,text="Reporte Usuario",variable=self.CheckReportUser)
		Check.grid(row=1,column=3,padx=5,pady=5)

		marcoTriaje=LabelFrame(self.Frame_Perfil,text='Triaje',borderwidth=2, relief="solid",width=int(width*0.5),height=int(height*0.4),bg="#949BAA")
		marcoTriaje.grid(row=2,column=1)
		
		self.checkReporteTriaje=BooleanVar()
		check=Checkbutton(marcoTriaje,text="Reporte Triaje",variable=self.checkReporteTriaje)
		check.grid(row=1,column=1,pady=5,padx=5)

		self.checkAgendarTriaje=BooleanVar()
		check=Checkbutton(marcoTriaje,text="Agendar Cita",variable=self.checkAgendarTriaje)
		check.grid(row=1,column=2,pady=5,padx=5)

		self.checkSearchTriaje=BooleanVar()
		check=Checkbutton(marcoTriaje,text="Buscar Atención",variable=self.checkSearchTriaje)
		check.grid(row=1,column=3,pady=5,padx=5)

		self.checkIncidenciasTriajeT=BooleanVar()
		checkI=Checkbutton(marcoTriaje,text="Incidencias",variable=self.checkIncidenciasTriajeT)
		checkI.grid(row=2,column=1,pady=5,padx=5)

		self.checkWhatsApp=BooleanVar()
		check=Checkbutton(marcoTriaje,text="Envio de Mensajes",variable=self.checkWhatsApp)
		check.grid(row=2,column=2,pady=5,padx=5)

		self.checkCantidadCupos=BooleanVar()
		check=Checkbutton(marcoTriaje,text='Confg. Cant. Cupos',variable=self.checkCantidadCupos)
		check.grid(row=2,column=3,pady=5,padx=5)

		marcoHis=LabelFrame(self.Frame_Perfil,text="His",borderwidth=2, relief="solid",width=int(width*0.5),height=int(height*0.4),bg="#949BAA")
		marcoHis.grid(row=3,column=1)

		self.produccionhis=BooleanVar()
		check=Checkbutton(marcoHis,text="Produccion His",variable=self.produccionhis)
		check.grid(row=1,column=1,pady=5,padx=5)

		self.ReporteHis=BooleanVar()
		check=Checkbutton(marcoHis,text="Reporte His",variable=self.ReporteHis)
		check.grid(row=1,column=2,pady=5,padx=5)

		self.dataHis=BooleanVar()
		check=Checkbutton(marcoHis,text="Data His",variable=self.dataHis)
		check.grid(row=1,column=3,pady=5,padx=5)

		marcoAlojamiento=LabelFrame(self.Frame_Perfil,text="Alojamiento",borderwidth=2, relief="solid",width=int(width*0.5),height=int(height*0.4),bg="#949BAA")
		marcoAlojamiento.grid(row=4,column=1)

		self.Alojamiento=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Alojamiento Conjunto",variable=self.Alojamiento)
		check.grid(row=1,column=1,pady=5,padx=5)

		self.Airn=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Airn",variable=self.Airn)
		check.grid(row=1,column=2,pady=5,padx=5)

		self.ReporteNacido=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Reporte",variable=self.ReporteNacido)
		check.grid(row=1,column=3,pady=5,padx=5)

		self.tamizaje=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Tamizaje",variable=self.tamizaje)
		check.grid(row=1,column=4,pady=5,padx=5)

		marcoAlojamiento=LabelFrame(self.Frame_Perfil,text="Neonatología",borderwidth=2, relief="solid",width=int(width*0.5),height=int(height*0.4),bg="#949BAA")
		marcoAlojamiento.grid(row=5,column=1)

		self.DatosGeneralesNeo=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Datos Generales Neonatología",variable=self.DatosGeneralesNeo)
		check.grid(row=1,column=1,pady=5,padx=5)

		self.IntermedioNeo=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Intermedios",variable=self.IntermedioNeo)
		check.grid(row=1,column=2,pady=5,padx=5)

		self.PatologicosNeo=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Patologicos",variable=self.PatologicosNeo)
		check.grid(row=1,column=3,pady=5,padx=5)

		self.RecuperacionNeo=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Recuperacion",variable=self.RecuperacionNeo)
		check.grid(row=2,column=1,pady=5,padx=5)

		self.Ucinneo=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Ucin",variable=self.Ucinneo)
		check.grid(row=2,column=2,pady=5,padx=5)

		marcoAlojamiento=LabelFrame(self.Frame_Perfil,text="Personal",borderwidth=2, relief="solid",width=int(width*0.5),height=int(height*0.4),bg="#949BAA")
		marcoAlojamiento.grid(row=6,column=1)

		self.IPaciente=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Insertar Paciente",variable=self.IPaciente)
		check.grid(row=1,column=1,pady=5,padx=5)

		self.ListarPaciente=BooleanVar()
		check=Checkbutton(marcoAlojamiento,text="Listar Paciente",variable=self.ListarPaciente)
		check.grid(row=1,column=2,pady=5,padx=5)

		marcoEstadistica=LabelFrame(self.Frame_Perfil,text="Estadisticas",borderwidth=2, relief="solid",width=int(width*0.5),height=int(height*0.4),bg="#949BAA")
		marcoEstadistica.grid(row=7,column=1)

		self.EstadisticaTriaje=BooleanVar()
		check=Checkbutton(marcoEstadistica,text="Estadisticas Triaje",variable=self.EstadisticaTriaje)
		check.grid(row=1,column=1,pady=5,padx=5)

	

		addbutton=ttk.Button(self.Frame_Perfil,text="Aceptar",cursor="hand2")
		addbutton.grid(row=8,column=1,pady=10,padx=10)
		addbutton['command']=self.recuperarCheck

	def EventTreeView(self,event):
		self.VentanaPerfil=Toplevel()
		self.VentanaPerfil.geometry("250x100")
		self.VentanaPerfil.title("Insertar Nuevo Perfil")
		self.VentanaPerfil.grab_set()

		label=Label(self.VentanaPerfil,text="Perfil")
		label.grid(row=1,column=1,pady=10,padx=10)
		self.entryPerfil=ttk.Entry(self.VentanaPerfil)
		self.entryPerfil.grid(row=1,column=2,columnspan=2,pady=10,padx=10)

		addButton=ttk.Button(self.VentanaPerfil,text="Aceptar")
		addButton['command']=self.InsertPerfil
		addButton.grid(row=2,column=2,pady=10,padx=10)

	def InsertPerfil(self):
		valor=self.entryPerfil.get()
		self.obj_Consulta.InsertarPerfil(valor)
		self.VentanaPerfil.destroy()

	def llenarTabla(self):
		rows=self.obj_Consulta.consultaPefil()
		for data in rows:
			self.table_Perfiles.insert('','end',values=(data.idRol,data.nombre))

	def recuperarCheck(self):

		data={'PUser':int(self.checkPerfil.get()),'AddUser':int(self.checkAddUser.get()),'ReportUser':int(self.CheckReportUser.get()),
		'ReportCitas':int(self.checkReporteTriaje.get()),'AddCitas':int(self.checkAgendarTriaje.get()),'SearchCita':int(self.checkSearchTriaje.get()),
		'IncidenciaCita':int(self.checkIncidenciasTriajeT.get()),'WhatsAppCita':int(self.checkWhatsApp.get()),'ProduccionHis':int(self.produccionhis.get()),
		'MReporteHis':int(self.ReporteHis.get()),'MDataHis':int(self.dataHis.get()),'AtencionAirn':int(self.Airn.get()),'NacidoAlojamiento':int(self.Alojamiento.get()),'ReporteNacidos':int(self.ReporteNacido.get()),
		'DatosGeneralesNeo':int(self.DatosGeneralesNeo.get()),'IntermediosNeo':int(self.IntermedioNeo.get()),'PatologicosNeo':int(self.PatologicosNeo.get())
		,'RecuperacionNeo':int(self.RecuperacionNeo.get()),'UcinNeo':int(self.Ucinneo.get()),'PacienteInsertar':int(self.IPaciente.get()),'PacienteListar':int(self.ListarPaciente.get()),'Tamizaje':int(self.tamizaje.get()),
		'EstadisticaTriaje':int(self.EstadisticaTriaje.get()),'Configurar_CantidadCupos':int(self.checkCantidadCupos.get())}
		
		
		if self.table_Perfiles.selection():
			IdRol=self.table_Perfiles.item(self.table_Perfiles.selection()[0],option='values')[0]

			if not self.obj_Consulta.ExisteAsignacion(IdRol):
				for clave in data:
					self.obj_Consulta.InsertarAsignaciones(IdRol,clave,data[clave])
			else:
				if self.obj_Consulta.DeleteAsignacion(IdRol):
					for clave in data:
						self.obj_Consulta.InsertarAsignaciones(IdRol,clave,data[clave])


		


