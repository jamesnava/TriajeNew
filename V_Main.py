from tkinter import *
import datetime
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import tkinter.font
from ttkthemes import ThemedTk
import GUI_User
import Consulta_Galen
import Consulta_Triaje
import Top_Triaje
import Top_Paciente
import Top_Reporte
import Impresion
import os
import Incidencias
import His_Main
from HisReporteGeneral import ReporteHis
from alerta import Alerta
#import threading
import time
from Nacidos.ReporteAirn import Reporte
from ModifyIcon import modificar_Icon
from VPerfil import Perfiles
import calendar

class Ventana_Principal(object):
	
	def __init__(self,root,usuario,nivel,dni,idrol,iduser):
		self.Usuario=usuario
		self.iduser=iduser
		self.nivel=nivel
		self.dni=dni
		self.letra_leyenda=('Candara',16,'bold italic')
		self.root=root
		addressIcon="img/menue/"
		##creando punteros a las consultas
		self.obj_QueryGalen=Consulta_Galen.queryGalen()
		self.obj_QueryTriaje=Consulta_Triaje.queryTriaje()		
		self.obj_Impresion=Impresion.Reporte()
		self.obj_ReporteAirn=Reporte()
		##fin de la creancion de punteros
		height=0
		
		#self.ventana=Tk()
		self.ventana=Toplevel()
		self.ventana.title('Sistema de produccion HSRA')		
		self.ventana.iconbitmap('img/doctor.ico')		
		self.height=self.ventana.winfo_screenheight()
		self.width=self.ventana.winfo_screenwidth()		
		self.ventana.geometry("%dx%d" % (self.width,self.height))
		self.ventana.protocol("WM_DELETE_WINDOW", root.destroy)
		
		#frame principal
		self.Frame_Principal=Frame(self.ventana,bg='#828682',width=self.width,height=self.height)
		self.Frame_Principal.pack()
		#agregando menu
		self.Barra_Menu=Menu(self.ventana)
		self.ventana['menu']=self.Barra_Menu
		#creando menu
		self.M_Archivo=Menu(self.Barra_Menu,tearoff=False)
		self.M_Archivo.add_command(label='Minimizar',command=self.ventana.iconify)
		self.M_Archivo.add_command(label='Cerrar',command=root.destroy)
		self.M_Archivo.add_separator()		
		self.Barra_Menu.add_cascade(label='Archivo',menu=self.M_Archivo)

		#menu configuracion			
		self.M_Usuario=Menu(self.Barra_Menu,tearoff=False)
		self.M_Triaje=Menu(self.Barra_Menu,tearoff=False)
		self.M_ProduccionHis=Menu(self.Barra_Menu,tearoff=False)
		self.M_Nacidos=Menu(self.Barra_Menu,tearoff=False)
		self.M_Neonatologia=Menu(self.Barra_Menu,tearoff=False)
		self.M_Paciente=Menu(self.Barra_Menu,tearoff=False)
		self.M_Estadistica=Menu(self.Barra_Menu,tearoff=False)

		valorRows=self.obj_QueryTriaje.ConsultaAsignacion(idrol)
		for val in valorRows:			
			metodo=getattr(self,val.Descripcion)
			metodo()

		self.Barra_Menu.add_cascade(label='Configuracion',menu=self.M_Usuario)					
		self.Barra_Menu.add_cascade(label='Triaje',menu=self.M_Triaje)			
		self.Barra_Menu.add_cascade(label='His',menu=self.M_ProduccionHis)			
		self.Barra_Menu.add_cascade(label='Nacidos',menu=self.M_Nacidos)			
		self.Barra_Menu.add_cascade(label='Neonatologia',menu=self.M_Neonatologia)			
		self.Barra_Menu.add_cascade(label='Pacientes',menu=self.M_Paciente)				
		self.Barra_Menu.add_cascade(label='Estadisticas',menu=self.M_Estadistica)
		#menu ayuda
		self.M_Usuario=Menu(self.Barra_Menu,tearoff=False)
		self.M_Usuario.add_command(label='Acerca de...',command=lambda:self.mensaje_Info('INFORMACION'))
		self.M_Usuario.add_command(label='Version',command=lambda:self.mensaje_Info('VERSION'))
		self.Barra_Menu.add_cascade(label='Ayuda',menu=self.M_Usuario)
		#self.ventana.mainloop()
		self.obj_Alert=Alerta()
		####alerta###			
		self.ventana.after(30,self.obj_Alert.Ventana_Alert)
	#########menues##################
	
	def PUser(self):		
		addressIcon="img/menue/"
		self.iconoPerfil=modificar_Icon(addressIcon+"perfil.png")			
		self.M_Usuario.add_command(label='Crear Perfiles',command=self.Frame_Perfiles,image=self.iconoPerfil,compound="left")

	def AddUser(self):
		addressIcon="img/menue/"
		self.icono=modificar_Icon(addressIcon+"addUser.png")			
		self.M_Usuario.add_command(label='Agregar Usuario',command=self.Desk_User,image=self.icono,compound="left")

	def ReportUser(self):
		addressIcon="img/menue/"
		self.IcLUser=modificar_Icon(addressIcon+"ListUser.png")
		self.M_Usuario.add_command(label='Reporte Usuario',command=self.Reporte_Usuarios,image=self.IcLUser,compound="left")

	def Configurar_CantidadCupos(self):
		addressIcon="img/menue/"
		self.NCupos=modificar_Icon(addressIcon+"cupos.png")		
		self.M_Usuario.add_command(label='Cantidad Cupos',command=self.Frame_ConfCupos,image=self.NCupos,compound="left")

	def ReportCitas(self):
		addressIcon="img/menue/"
		self.IcListCita=modificar_Icon(addressIcon+"ListCita.png")
		self.M_Triaje.add_command(label='Reporte Citas',command=self.Reporte_Cita,image=self.IcListCita,compound="left")

	def AddCitas(self):
		addressIcon="img/menue/"
		self.IcCita=modificar_Icon(addressIcon+"addCita.png")
		self.M_Triaje.add_command(label='Agendar Cita',command=self.Frame_Triaje,image=self.IcCita,compound="left")

	def SearchCita(self):
		Objeto_Triaje=Top_Triaje.Triaje()
		addressIcon="img/menue/"
		self.IcSearchCita=modificar_Icon(addressIcon+"searchCita.png")
		self.M_Triaje.add_command(label='Buscar Atención',command=Objeto_Triaje.search_Citas,image=self.IcSearchCita,compound="left")

	def IncidenciaCita(self):
		addressIcon="img/menue/"
		self.IcIncidencia=modificar_Icon(addressIcon+"Incidencia.png")
		self.M_Triaje.add_command(label='Incidencias',command=self.Incidencias,image=self.IcIncidencia,compound="left")

	def WhatsAppCita(self):
		addressIcon="img/menue/"
		self.IcWhat=modificar_Icon(addressIcon+"whatsapp.png")
		self.M_Triaje.add_command(label='Enviar Msg WhatsApp',command="",image=self.IcWhat,compound="left")

	def ProduccionHis(self):
		addressIcon="img/menue/"
		self.hisPro=modificar_Icon(addressIcon+"hisPro.png")
		self.M_ProduccionHis.add_command(label='Produccion His',command=self.Frame_ProduccionHIS,image=self.hisPro,compound="left")

	def MReporteHis(self):
		addressIcon="img/menue/"
		self.IcHis=modificar_Icon(addressIcon+"ListCita.png")
		self.M_ProduccionHis.add_command(label='Reporte His',command=self.ReporteHis,image=self.IcHis,compound="left")

	def MDataHis(self):
		addressIcon="img/menue/"
		self.IHisdata=modificar_Icon(addressIcon+"data.png")
		self.M_ProduccionHis.add_command(label='Interconsulta',command=self.DataHis,image=self.IHisdata,compound='left')

		
	def AtencionAirn(self):
		addressIcon="img/menue/"
		self.IcAIRN=modificar_Icon(addressIcon+"airn.png")
		self.M_Nacidos.add_command(label='AIRN',command=self.AirnNacidos,image=self.IcAIRN,compound="left")

	def NacidoAlojamiento(self):
		addressIcon="img/menue/"
		self.IcAlojamiento=modificar_Icon(addressIcon+"alojamiento.png")
		self.M_Nacidos.add_command(label='Alojamiento Conjunto',command=self.Alojamiento,image=self.IcAlojamiento,compound="left")

	def Tamizaje(self):
		#addressIcon="img/menue/"
		#self.IcAlojamiento=modificar_Icon(addressIcon+"alojamiento.png")
		self.M_Nacidos.add_command(label='Tamizaje',command=self.tamizaje,compound="left")

	def ReporteNacidos(self):
		addressIcon="img/menue/"
		self.IcNacido=modificar_Icon(addressIcon+"ListCita.png")
		self.M_Nacidos.add_command(label='Reporte',command=self.obj_ReporteAirn.TopReporte,image=self.IcNacido,compound="left")

	def DatosGeneralesNeo(self):
		self.M_Neonatologia.add_command(label='DatosGenerales',command=self.Frame_DatosGenerales)

	def IntermediosNeo(self):
		self.M_Neonatologia.add_command(label='Intermedios',command=lambda :self.Frame_NeoServicios(2))

	def PatologicosNeo(self):
		self.M_Neonatologia.add_command(label='Patologicos',command=lambda :self.Frame_NeoServicios(4))

	def RecuperacionNeo(self):
		self.M_Neonatologia.add_command(label='Recuperacion Nutri.',command=lambda :self.Frame_NeoServicios(5))

	def UcinNeo(self):
		self.M_Neonatologia.add_command(label='Ucin',command=lambda :self.Frame_NeoServicios(3))

	def PacienteInsertar(self):
		self.M_Paciente.add_command(label='Insertar',command=self.Agregar_Pacientes)

	def PacienteListar(self):
		self.M_Paciente.add_command(label='Listar pacientes',command=self.Listar_Pacientes)

	def EstadisticaTriaje(self):
		self.M_Estadistica.add_command(label='Estadisticas Triaje',command=self.Estadistica_Triaje)

	#########fin menues##############

	##APARTADO PERFILES##
	def Frame_Perfiles(self):		
		self.Frame_Perfiles=Frame(self.Frame_Principal,width=self.width,height=self.height,bg="#828682")
		self.Frame_Perfiles.place(x=0,y=0)
		self.Frame_Perfiles.pack_propagate(False)
		obj_perfil=Perfiles()
		obj_perfil.Frame_perfiles(self.Frame_Perfiles,self.width,self.height)

	#APARTADO DE CONFIGURACION DE CUPOS
	def Frame_ConfCupos(self):
		from ConfiguracionT.cupos import TCupos
		obj_cupos=TCupos(self.Frame_Principal,self.Usuario,self.height,self.width)
		obj_cupos.Contenedor()

	#APARTADO NEONATOLOGIA
	def Frame_DatosGenerales(self):		
		self.Frame_Intermedio=Frame(self.Frame_Principal,width=self.width,height=self.height,bg="#828682")
		self.Frame_Intermedio.place(x=0,y=0)
		self.Frame_Intermedio.pack_propagate(False)
		from Neonatologia import Neonatologia
		obj_Neo=Neonatologia.DATOSGENERALES(self.Usuario,self.dni)
		obj_Neo.Top_AddPaciente()		

	def Frame_NeoServicios(self,servicio):
		
		self.Frame_Intermedio=Frame(self.Frame_Principal,width=self.width,height=self.height,bg="#828682")
		self.Frame_Intermedio.place(x=0,y=0)
		self.Frame_Intermedio.pack_propagate(False)
		
		from Neonatologia import Servicios		
		obj_Neo=Servicios.Servicio(self.Usuario,self.dni,servicio)
		obj_Neo.Frame_Servicios(self.Frame_Intermedio,self.width,self.height)			

	#FIN NEONATOLOGIA
	def AirnNacidos(self):
		try:
			self.Frame_AIRN=Frame(self.Frame_Principal,width=self.width,height=self.height,bg="#828682")
			self.Frame_AIRN.place(x=0,y=0)
			self.Frame_AIRN.pack_propagate(False)
			from Nacidos import Madre
			obj_AIRN=Madre.MadreN(self.Frame_AIRN,self.width,self.height,self.Usuario)
			obj_AIRN.Frame_Madre(self.iduser)
		except Exception as e:
			messagebox.showerror("Notificación",e)
		

	def Alojamiento(self):
		
		self.Frame_ALOJAMIENTO=Frame(self.Frame_Principal,width=self.width,height=self.height,bg="#828682")
		self.Frame_ALOJAMIENTO.place(x=0,y=0)
		self.Frame_ALOJAMIENTO.pack_propagate(False)
		from Nacidos import Madre
		obj_Alojamiento=Madre.MadreN(self.Frame_ALOJAMIENTO,self.width,self.height,self.Usuario)
		obj_Alojamiento.Frame_Alojamiento(self.Frame_ALOJAMIENTO,self.width,self.height)

	def tamizaje(self):		
		self.Frame_Tamizaje=Frame(self.Frame_Principal,width=self.width,height=self.height,bg="#828682")
		self.Frame_Tamizaje.place(x=0,y=0)
		self.Frame_Tamizaje.pack_propagate(False)
		from Nacidos import Tamizaje
		obj_Alojamiento=Tamizaje.Tamizaje(self.Frame_Tamizaje,self.width,self.height)
		obj_Alojamiento.Frame_Tamizaje(self.Frame_Tamizaje,self.width,self.height)

	def DataHis(self):
		from His.datos import DataHis
		self.Frame_HisData=Frame(self.Frame_Principal,width=self.width,height=self.height,bg="#828682")
		self.Frame_HisData.place(x=0,y=0)
		self.Frame_HisData.pack_propagate(False)
		obj_dataHis=DataHis(self.dni)
		obj_dataHis.FrameDataHis(self.Frame_HisData,self.width,self.height)
		

	def ReporteHis(self):
		
		self.Frame_HisReport=Frame(self.Frame_Principal,width=self.width,height=self.height,bg="#828682")
		self.Frame_HisReport.place(x=0,y=0)
		self.Frame_HisReport.pack_propagate(False)		
		obj_HISReporte=ReporteHis(self.dni)
		obj_HISReporte.Frame_Reporte(self.Frame_HisReport,self.width,self.height)

	def mensaje_Info(self,iden):
		
		if iden=='INFORMACION':
			strinfo=f"""Sistema de citas de consultorio externo y Digitacion HIS,desarrollado por la Unidad de Estadística e Informática, a traves de la oficina de Desarrollo y Programacion del HOSPITAL SUB REGIONAL DE ANDAHUAYLAS... Todos los derechos resevados© Andahuaylas 2022 by Jaime Navarro Crúz"""
			messagebox.showinfo('Notificación',strinfo)
		elif iden=='VERSION':
			messagebox.showinfo('Notificación',f"""SISTEMA DE CITAS DE CONSULTORIO EXTERNO Y PRODUCCION HIS.\nversion 1.7""")

	
	def Desk_User(self):		
		obj_usuario=GUI_User.Usuario()
		obj_usuario.Top_Agregar(self.ventana)

	def Reporte_Usuarios(self):		
		obj_usuario=GUI_User.Usuario()
		obj_usuario.top_ListaUsuario()

	def Incidencias(self):
		
		self.Frame_incidencias=Frame(self.Frame_Principal,width=self.width,height=self.height,bg="#828682")
		self.Frame_incidencias.place(x=0,y=0)
		self.Frame_incidencias.pack_propagate(False)
		obj_incidencia=Incidencias.IncidenciasV(self.Usuario)
		obj_incidencia.Incidencias(self.Frame_incidencias,self.width,self.height)

	def Estadistica_Triaje(self):
		from Estadisticas import ETriaje
		objTriaje=ETriaje.Triaje_Estadisticas(self.width,self.height,self.Usuario,self.Frame_Principal,self.ventana)
		objTriaje.FramePrincipal()	


	def Frame_ProduccionHIS(self):
		
		self.Frame_His=Frame(self.Frame_Principal,width=self.width,height=self.height,bg="#828682")
		self.Frame_His.place(x=0,y=0)
		self.Frame_His.pack_propagate(False)
		obj_HISMAIN=His_Main.HisV(self.Usuario,self.dni)
		obj_HISMAIN.frame_His(self.Frame_His,self.width,self.height)
		
	def Frame_Triaje(self):
		
		self.F_Triaje=Frame(self.Frame_Principal,width=self.width,height=self.height,bg='#828682')
		self.F_Triaje.place(x=0,y=0)
		#AGRENDO LA SEPARACION DEL FRAME
		self.Frame_Programacion=Frame(self.F_Triaje,width=int(self.width*0.16),height=int(self.height*0.95),bg='white')		
		self.Frame_Programacion.place(x=0,y=0)

		date=datetime.datetime.now()		
		self.calendario=Calendar(self.Frame_Programacion,selectmode='day',year=date.year,month=date.month,day=date.day)
		self.calendario.bind('<<CalendarSelected>>',self.calendar_event)
		self.calendario.grid(row=0,column=1,columnspan=3)

		#Agrego lo programado
		self.Lista_Menu=Listbox(self.Frame_Programacion,height=28,width=40,selectforeground='#ffffff',selectbackground="#00aa00",selectborderwidth=2,cursor='hand2')
		self.llenar_Menu()
		self.Lista_Menu.bind('<<ListboxSelect>>',self.Generate_Cupos)
		self.Lista_Menu.grid(row=1,column=0,columnspan=3)
		scroll_bar=Scrollbar(self.Frame_Programacion)
		scroll_bar.grid(row=1,column=4)
		self.Lista_Menu.configure(yscrollcommand=scroll_bar.set)
		scroll_bar.configure(command=self.Lista_Menu.yview)
		#AGREGO PANEL PRINCIPAL		

		self.Frame_TriajeP=Frame(self.F_Triaje,width=int(self.width*0.80),height=int(self.height*0.65),bg='#828682',relief="solid",bd=1)
		
		self.Frame_TriajeP.place(x=int(self.width*0.16)+10,y=0)
		self.Frame_TriajeP.grid_propagate(False)
		
		#Agrego programacion
		#self.ConsultorioP=Frame(self.F_Triaje,width=int(self.width*0.80),height=int(self.height*0.16),bg='#828682',relief="solid",bd=1)		
		#self.ConsultorioP.place(x=int(self.width*0.16)+10,y=int(self.height*0.66))
		#self.ConsultorioP.grid_propagate(False)			
		
		#menu agregar y eliminar
		self.menu_right=Menu(self.Frame_TriajeP,tearoff=0)
		self.menu_right.add_command(label='Atencion Normal',command=lambda:self.evento_agregar(1))
		self.menu_right.add_command(label='Cupo Adicional',command=lambda:self.evento_agregar(2))

		self.menu_FechaAnterior=Menu(self.Frame_TriajeP,tearoff=0)
		#self.menuFechaAnterior.add_command(label='Eliminar',command=self.evento_EliminarCupo)
		self.menu_FechaAnterior.add_command(label='Consultar',command=self.evento_ConsultaCupo)
		self.menu_FechaAnterior.add_command(label='Imprimir',command=self.evento_ImprimirCupo)

		#menu anulado
		self.menu_Anulado=Menu(self.Frame_TriajeP,tearoff=0)
		#self.menu_Anulado.add_command(label='Anular',command=self.evento_EliminarCupo)
		self.menu_Anulado.add_command(label='Consultar',command=self.evento_ConsultaCupo)
		self.menu_Anulado.add_command(label='Imprimir',command=self.evento_ImprimirCupo)


		#:::::::::::::::
		self.menu_Fechaposterior=Menu(self.Frame_TriajeP,tearoff=0)
		self.menu_Fechaposterior.add_command(label='Anular',command=self.evento_EliminarCupo)
		self.menu_Fechaposterior.add_command(label='Consultar',command=self.evento_ConsultaCupo)
		self.menu_Fechaposterior.add_command(label='Imprimir',command=self.evento_ImprimirCupo)

		# leyenda::::::::::::::::::::::::::::::
		self.frame_Leyenda=Frame(self.F_Triaje,width=self.width,height=int(self.height*0.1),bg='black')
		#agregando Widgets Leyenda
		etiqueta_Leyenda=Label(self.frame_Leyenda,text='Leyenda',fg='white',bg='black',font=self.letra_leyenda)
		etiqueta_Leyenda.grid(row=0,column=0,padx=5)
		styl = ttk.Style()
		styl.configure('white.TSeparator', background='white')

		etiqueta_Leyenda=Label(self.frame_Leyenda,text='SALUDPOL',fg='#9D8F06',bg='black',font=self.letra_leyenda)
		etiqueta_Leyenda.grid(row=1,column=9,padx=5)
		styl = ttk.Style()		

		etiqueta_Leyenda=Label(self.frame_Leyenda,text='ANULADO',fg='#080E66',font=self.letra_leyenda)		
		etiqueta_Leyenda.grid(row=1,column=10,padx=5)
		styl = ttk.Style()		

		styl = ttk.Style()
		styl.configure('white.TSeparator', background='white')

		s1=ttk.Separator(self.frame_Leyenda,orient='vertical')
		s1.grid(row=0,column=1,rowspan=2)

		etiqueta_Leyenda=Label(self.frame_Leyenda,text='Agendado',fg='red',bg='black',font=self.letra_leyenda)
		etiqueta_Leyenda.grid(row=0,column=2,padx=5)
		
		etiqueta_Leyenda=Label(self.frame_Leyenda,text='Libre',fg='green',bg='black',font=self.letra_leyenda)
		etiqueta_Leyenda.grid(row=1,column=2,padx=5)

		etiqueta_Leyenda=Label(self.frame_Leyenda,text='Adicional',fg='#340563',bg='black',font=self.letra_leyenda)
		etiqueta_Leyenda.grid(row=1,column=3,padx=5)

		s1=ttk.Separator(self.frame_Leyenda,orient='vertical',style='white.TSeparator',takefocus=1)
		s1.grid(row=0,column=7,rowspan=2,sticky='NS')		
		self.etiqueta_Medico=Label(self.frame_Leyenda,text='Medico',fg='white',bg='black',font=self.letra_leyenda)
		self.etiqueta_Medico.grid(row=0,column=9,columnspan=4,padx=5)

		s1=ttk.Separator(self.frame_Leyenda,orient='vertical',style='white.TSeparator',takefocus=1)
		s1.grid(row=0,column=17,rowspan=2,sticky='NS')
		self.etiqueta_servicio=Label(self.frame_Leyenda,text='Servicio',fg='white',bg='black',font=self.letra_leyenda)
		self.etiqueta_servicio.grid(row=0,column=18)


		s1=ttk.Separator(self.frame_Leyenda,orient='vertical',style='white.TSeparator',takefocus=1)
		s1.grid(row=0,column=25,rowspan=2,sticky='NS')
		etiqueta_Turno=Label(self.frame_Leyenda,text='Turno :',fg='white',bg='black',font=self.letra_leyenda)
		etiqueta_Turno.grid(row=0,column=26)
		self.etiqueta_Turno1=Label(self.frame_Leyenda,text='',fg='white',bg='black',font=self.letra_leyenda)
		self.etiqueta_Turno1.grid(row=0,column=28)

		
		s1=ttk.Separator(self.frame_Leyenda,orient='vertical',style='white.TSeparator',takefocus=1)
		s1.grid(row=0,column=33,rowspan=2,sticky='NS')
		etiqueta_Usuario=Label(self.frame_Leyenda,text='Usuario :',fg='white',bg='black',font=self.letra_leyenda)
		etiqueta_Usuario.grid(row=0,column=34)
		etiqueta_Usuario=Label(self.frame_Leyenda,text=f'{self.Usuario}',fg='white',bg='black',font=self.letra_leyenda)
		etiqueta_Usuario.grid(row=0,column=35)	
		self.frame_Leyenda.place(x=0,y=int(self.height*0.84))

	def evento_clickRight(self,event):
		
		try:
			
			if len(self.Lista_Menu.curselection())!=0:
				self.cupo_=event.widget.cget('text')			
				consultorio_Total=self.Lista_Menu.get(self.Lista_Menu.curselection()[0])
				consultorio=consultorio_Total[consultorio_Total.find('_')+1:]				
				#consultar si el cupo esta agendado			
				rows=self.obj_QueryTriaje.query_CupoNumber(self.calendario.selection_get(),consultorio,self.cupo_,self.turno,self.Dni_Medico)
				controlador=0

				for v in rows:
					controlador=v.Id_Etriaje
				if len(rows)==1:					
					date=datetime.date.today()
					if self.calendario.selection_get()<date:							
						if controlador==1:
							self.menu_FechaAnterior.tk_popup(event.x_root,event.y_root)
						else:
							self.menu_Anulado.tk_popup(event.x_root,event.y_root)

					else:
						if controlador==1:
							
							self.menu_Fechaposterior.tk_popup(event.x_root,event.y_root)
						else:
							self.menu_Anulado.tk_popup(event.x_root,event.y_root)
										

				elif len(rows)==0:
					self.menu_right.tk_popup(event.x_root,event.y_root)
			else:
				messagebox.showinfo('Alerta','Seleccione un consultorio!')

		finally:
			self.menu_right.grab_release()

	def evento_agregar(self,Tipocupo):		
		lambda event:self.Generate_Cupos(event)
		date=datetime.date.today()
		obj_TopTriaje=None
		datos_M=self.obj_QueryGalen.query_Programacion(self.calendario.selection_get())		
		consulta_datos_Medico=self.obj_QueryGalen.datos_EmpleadosConsultorioExt(self.Dni_Medico.strip())
		
		rows_cupos_count=self.obj_QueryTriaje.ConsultaConfCupos(consulta_datos_Medico[0].IdMedico,self.idservicio,self.turno,self.calendario.selection_get())
		if Tipocupo==1:
			if rows_cupos_count:
				year=self.calendario.selection_get().year
				month=self.calendario.selection_get().month
				_,num_days=calendar.monthrange(year,month)
				rows_cupos_Agendados=self.obj_QueryTriaje.ConsultaCountCuposXdia(self.Dni_Medico.strip(),self.idservicio,self.turno,1,self.calendario.selection_get())
		
				#terminar aqui				
				Totalcupos=rows_cupos_count[0].Cantidad
				AgendadosCupos=rows_cupos_Agendados[0].cantidad							
				if int(AgendadosCupos)<int(Totalcupos):
					if self.calendario.selection_get()>=date:									
						obj_TopTriaje=Top_Triaje.Triaje()
						obj_TopTriaje.Top_Agregar(globals()['self.cupo%s'%self.cupo_],self.servicio,self.Medico_Datos,self.Usuario,self.calendario.selection_get(),self.turno,Tipocupo,self.idservicio,self.Dni_Medico)		
					else:
						messagebox.showinfo('Alerta','No se puede programar para esta fecha!')
				else:
					messagebox.showerror('Error!!','No hay cupos disponibles!!')
			
			else:
				messagebox.showerror('Error','Debe configurar la cantidad de cupos a atender!!')
		else:
			if self.calendario.selection_get()>=date:									
				obj_TopTriaje=Top_Triaje.Triaje()
				obj_TopTriaje.Top_Agregar(globals()['self.cupo%s'%self.cupo_],self.servicio,self.Medico_Datos,self.Usuario,self.calendario.selection_get(),self.turno,Tipocupo,self.idservicio,self.Dni_Medico)		
			else:
				messagebox.showinfo('Alerta','No se puede programar para esta fecha!')



	def evento_EliminarCupo(self):		
		result=messagebox.askquestion('Alerta','Estas seguro de que desea anular el cupo\n recuerda que una vez anulada no podrá revertirse')
		if result=='yes':
			consultorio_Total=self.Lista_Menu.get(self.Lista_Menu.curselection()[0])
			consultorio=consultorio_Total[consultorio_Total.find('_')+1:]
			
			ventana_Anular=Toplevel()
			ventana_Anular.geometry("400x200")
			ventana_Anular.grab_set()
			ventana_Anular.title("Anulacion del cupo")
			label=Label(ventana_Anular,text="Motivo")
			label.grid(row=1,column=1,pady=10)
			motivo=Text(ventana_Anular,width=30,height=5)
			motivo.grid(row=1,column=2,columnspan=2,pady=10)

			btn_grabar=ttk.Button(ventana_Anular,text="Grabar")
			btn_grabar['command']=lambda: self.evento_Anular(ventana_Anular,motivo,self.cupo_,self.calendario.selection_get(),consultorio,self.Medico_Datos,self.turno)
			btn_grabar.grid(row=2,column=2,pady=10)

			btn_cancelar=ttk.Button(ventana_Anular,text="Cancelar")
			btn_cancelar.configure(command=ventana_Anular.destroy)
			btn_cancelar.grid(row=2,column=3,pady=10)
	def evento_ImprimirCupo(self):		
		consultorio_Total=self.Lista_Menu.get(self.Lista_Menu.curselection()[0])
		consultorio=consultorio_Total[:consultorio_Total.find(':')]
			
		rows=self.obj_QueryTriaje.query_DataTriaje(self.calendario.selection_get(),consultorio,self.cupo_,self.Dni_Medico,self.turno)
		for val in rows:
			dni=val.dni
			fuente=val.fuente
			cupo=val.Nro_Cupo
			medico=val.Medico
			consultorio=val.Especialidad
			nro_Referencia=val.Nro_Referencia
			establecimiento=val.P_C
			Historia=val.Historia
			fecha_A=val.Fecha_Atencion
			turno=val.Turno
			usuario=val.Usuario
			fechaR=str(val.FechaR)[:16]
			estado=val.estado
		self.obj_Impresion.imprimir_Cupo(dni,fuente,cupo,medico,consultorio,nro_Referencia,fecha_A,Historia,establecimiento,turno,usuario,fechaR,estado)
		os.startfile('cupo.pdf','print')

	def evento_ConsultaCupo(self):		
		consultorio_Total=self.Lista_Menu.get(self.Lista_Menu.curselection()[0])
		consultorio=consultorio_Total[:int(consultorio_Total.find(':'))]		
		rows=self.obj_QueryTriaje.query_DataTriaje(self.calendario.selection_get(),consultorio,self.cupo_,self.Dni_Medico,self.turno)		
		for val in rows:
			dni=val.dni
			fuente=val.fuente
			cupo=val.Nro_Cupo
			medico=val.Medico
			consultorio=val.Especialidad
			nro_Referencia=val.Nro_Referencia
			establecimiento=val.P_C
			Historia=val.Historia
			fecha_A=val.Fecha_Atencion
			turno=val.Turno
			usuario=val.Usuario
			fechaR=str(val.FechaR)[:16]
			estado=val.estado

		self.obj_Impresion.imprimir_Cupo(dni,fuente,cupo,medico,consultorio,nro_Referencia,fecha_A,Historia,establecimiento,turno,usuario,fechaR,estado)
		obj_TopReporte=Top_Reporte.Reporte()
		obj_TopReporte.top_ConsultaCupo()

	def llenar_Menu(self):

		try:
			self.Lista_Menu.delete(0,'end')
			rows=self.obj_QueryGalen.query_Programacion(self.calendario.selection_get())
			for val in rows:
				self.Lista_Menu.insert(0,str(val.IdServicio)+':'+str(val.IdTurno)+'-'+str(val.IdMedico)+'_'+val.Nombre)
		except Exceptions as e:
			messagebox.showinfo('Alerta',f'Error {e}')

	def calendar_event(self,event):		
		self.llenar_Menu()

	def Generate_Cupos(self,event):
		from Util import ProgramacionEspecialidad				
		try:
			data_lista=self.Lista_Menu.get(self.Lista_Menu.curselection()[0])
			self.idservicio=data_lista[:data_lista.find(':')]
			self.turno_codi=data_lista[data_lista.find(':')+1:data_lista.find('-')]
			self.IdMedico=data_lista[data_lista.find('-')+1:data_lista.find('_')]						
			self.servicio=data_lista[data_lista.find('_')+1:]

			#rol
			#obj_programacion=ProgramacionEspecialidad.ProgEspecialidad(self.ConsultorioP,self.width,self.height)
			#obj_programacion.Programacion(self.calendario.selection_get(),self.idservicio)

			letra=('Arial',18,'bold')			
			medico=self.obj_QueryGalen.consulta_Medico_Responsable(self.servicio,self.calendario.selection_get(),self.IdMedico,self.turno_codi)	
			
			for val in medico:
				self.Medico_Datos=val.Nombres+" "+val.ApellidoPaterno+" "+val.ApellidoMaterno
				self.turno=val.Descripcion
				self.Dni_Medico=val.DNI.strip()

			rows=self.obj_QueryTriaje.query_Cupo(self.calendario.selection_get(),self.servicio,self.Dni_Medico,self.turno)
			lista_cupos=[]
			lista_anulados=[]
			lista_adicionales=[]
			for valores in rows:
				lista_cupos.append(valores.Nro_Cupo)
				if valores.Id_Etriaje==2:
					lista_anulados.append(valores.Nro_Cupo)
				elif valores.ID_TIPOA==2:
					lista_adicionales.append(valores.Nro_Cupo)
			
			Nro_Cupo=1		
			for i in range(4):
				for j in range(9):
					if Nro_Cupo in lista_cupos:
						if  Nro_Cupo in lista_anulados:
							globals()['self.cupo%s'%Nro_Cupo]=Label(self.Frame_TriajeP,text=Nro_Cupo, width=7,height=4,bg='#080E66',fg='white',borderwidth=2,relief="ridge",font=letra)
							globals()['self.cupo%s'%Nro_Cupo].bind('<Button-3>',self.evento_clickRight)
							globals()['self.cupo%s'%Nro_Cupo].grid(row=i,column=j, padx=7,pady=7)
										
						elif Nro_Cupo in lista_adicionales:
							globals()['self.cupo%s'%Nro_Cupo]=Label(self.Frame_TriajeP,text=Nro_Cupo, width=7,height=4,bg='#340563',fg='white',borderwidth=2,relief="ridge",font=letra)
							globals()['self.cupo%s'%Nro_Cupo].bind('<Button-3>',self.evento_clickRight)
							globals()['self.cupo%s'%Nro_Cupo].grid(row=i,column=j, padx=7,pady=7)

						else:
							if Nro_Cupo<=30:
								globals()['self.cupo%s'%Nro_Cupo]=Label(self.Frame_TriajeP,text=Nro_Cupo, width=7,height=4,bg='red',fg='white',borderwidth=2,relief="ridge",font=letra)
								globals()['self.cupo%s'%Nro_Cupo].bind('<Button-3>',self.evento_clickRight)
								globals()['self.cupo%s'%Nro_Cupo].grid(row=i,column=j, padx=7,pady=7)							
							elif Nro_Cupo>30:
								globals()['self.cupo%s'%Nro_Cupo]=Label(self.Frame_TriajeP,text=Nro_Cupo, width=7,height=4,bg='#128385',fg='red',borderwidth=2,relief="ridge",font=letra)
								globals()['self.cupo%s'%Nro_Cupo].bind('<Button-3>',self.evento_clickRight)
								globals()['self.cupo%s'%Nro_Cupo].grid(row=i,column=j, padx=7,pady=7)
					else:
						if Nro_Cupo<=30:
							globals()['self.cupo%s'%Nro_Cupo]=Label(self.Frame_TriajeP,text=Nro_Cupo, width=7,height=4,bg='#185522',fg='white',borderwidth=2,relief="ridge",font=letra)
							globals()['self.cupo%s'%Nro_Cupo].bind('<Button-3>',self.evento_clickRight)
							globals()['self.cupo%s'%Nro_Cupo].grid(row=i,column=j, padx=7,pady=7)						
						elif Nro_Cupo>30:
							globals()['self.cupo%s'%Nro_Cupo]=Label(self.Frame_TriajeP,text=Nro_Cupo, width=7,height=4,bg='#9D8F06',fg='white',relief="ridge",borderwidth=2,font=letra)
							globals()['self.cupo%s'%Nro_Cupo].bind('<Button-3>',self.evento_clickRight)
							globals()['self.cupo%s'%Nro_Cupo].grid(row=i,column=j, padx=7,pady=7)
					Nro_Cupo+=1	
			self.etiqueta_Turno1.configure(text=f'{self.turno}')
			self.etiqueta_Medico.configure(text=f'Medico : {self.Medico_Datos}')
			self.etiqueta_servicio.configure(text=f'Consultorio : {self.servicio}')
		except Exception as e:
			print(e)	

	def Reporte_Cita(self):		
		obj_Reporte=Top_Reporte.Reporte()		
		obj_Reporte.Top_Reporte()
	def Agregar_Pacientes(self):		
		obj_TopPaciente=Top_Paciente.Paciente()
		obj_TopPaciente.Top_Agregar()

	def Listar_Pacientes(self):		
		obj_TopPaciente=Top_Paciente.Paciente()
		obj_TopPaciente.paciente_Visualizacion()

	def evento_Anular(self,ventana,etiquetaMotivo,cupo,fecha,consultorio,medico,turno):
		motivo=etiquetaMotivo.get(1.0, "end-1c")
		if len(motivo)>=10:
			id_Tanulado=self.obj_QueryTriaje.Anular_Cita(cupo,fecha,consultorio,medico,turno)			
			globals()['self.cupo%s'%self.cupo_].configure(bg='#080E66')
			self.obj_QueryTriaje.insertar_MotivoAnulacion(self.Usuario,motivo,id_Tanulado[0])
			messagebox.showinfo("Alerta","El cupo numero {} se anuló".format(cupo))
			ventana.destroy()
		else:
			messagebox.showinfo('Notificación','Ingrese al menos 10 caracteres en el campo motivo de anulación')
	