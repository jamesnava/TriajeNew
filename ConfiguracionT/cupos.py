from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
import Consulta_Galen
import Consulta_Triaje
import calendar


class TCupos(object):
	def __init__(self,contenedorPincipal,usuario,height,width):
		self.obj_QueryGalen=Consulta_Galen.queryGalen()
		self.obj_QueryTriaje=Consulta_Triaje.queryTriaje()
		self.usuario=usuario
		self.height=height
		self.width=width
		self.FramePrincipal=contenedorPincipal
		self.letra_leyenda=('Candara',16,'bold italic')
	def Contenedor(self):
		
		self.Frame_Top=Frame(self.FramePrincipal,width=self.width-int(self.width*0.18),height=300,highlightthickness=1,bg='#828682')
		self.Frame_Top.place(x=int(self.width*0.18),y=0)
		self.Frame_Top.grid_propagate(False)

		self.Lista_Especialidad=Listbox(self.Frame_Top,height=15,width=40,selectmode="multiple")
		self.Lista_Especialidad.grid(row=0,column=1,rowspan=6,pady=5,padx=5)

		label=Label(self.Frame_Top,text="Cantidad de Cupos",bg='#828682')
		label.grid(row=1,column=2,padx=5,pady=5)
		cantidad_cupos=Entry(self.Frame_Top)
		cantidad_cupos.grid(row=2,column=2,padx=5,pady=5)

		button_guardadConfiguracion=Button(self.Frame_Top,text="Guardar")
		button_guardadConfiguracion.grid(row=3,column=2,padx=5,pady=5)
		button_guardadConfiguracion['command']=lambda:self.Conf_Guardar(cantidad_cupos)

		self.Frame_Cuerpo=Frame(self.FramePrincipal,width=self.width-int(self.width*0.18),height=int(self.height)-400,highlightthickness=1,bg='#828682')
		self.Frame_Cuerpo.place(x=int(self.width*0.18),y=300)
		self.Frame_Cuerpo.grid_propagate(False)

		Etiqueta=Label(self.Frame_Cuerpo,text='Actualizar Campos',bg='#828682')
		Etiqueta.grid(row=0,column=1,padx=10,pady=10)

		self.EntryId_Cupos=Entry(self.Frame_Cuerpo,state='readonly')
		self.EntryId_Cupos.grid(row=1,column=1,padx=10,pady=10)

		self.Entry_Cupos=Entry(self.Frame_Cuerpo)
		self.Entry_Cupos.grid(row=2,column=1,padx=10,pady=10)

		button_Update=Button(self.Frame_Cuerpo,text='Guardar')
		button_Update.grid(row=3,column=1,padx=10,pady=10)
		button_Update['command']=self.Update_Cupos

		self.Frame_Programacion=Frame(self.FramePrincipal,width=int(self.width*0.18),height=int(self.height*0.95),bg='#828682')		
		self.Frame_Programacion.grid_propagate(False)
		self.Frame_Programacion.place(x=0,y=0)

		date=datetime.datetime.now()		
		self.calendario=Calendar(self.Frame_Programacion,selectmode='day',year=date.year,month=date.month,day=date.day)
		self.calendario.bind('<<CalendarSelected>>',self.calendar_event)
		self.calendario.grid(row=0,column=0,columnspan=3)

		self.Lista_Menu=Listbox(self.Frame_Programacion,height=28,width=40,selectforeground='#ffffff',selectbackground="#00aa00",selectborderwidth=2,cursor='hand2')
		self.llenar_Menu()
		self.Lista_Menu.bind('<<ListboxSelect>>',self.Vista_Cupos)
		self.Lista_Menu.grid(row=1,column=0,columnspan=3)
		scroll_bar=Scrollbar(self.Frame_Programacion)
		scroll_bar.grid(row=1,column=4)
		self.Lista_Menu.configure(yscrollcommand=scroll_bar.set)
		scroll_bar.configure(command=self.Lista_Menu.yview)

		self.frame_Leyenda=Frame(self.FramePrincipal,width=self.width,height=int(self.height*0.1),bg='black')
		#agregando Widgets Leyenda
		etiqueta_Leyenda=Label(self.frame_Leyenda,text='Leyenda',fg='white',bg='black',font=self.letra_leyenda)
		etiqueta_Leyenda.grid(row=0,column=0,padx=5)			

		styl = ttk.Style()
		styl.configure('white.TSeparator', background='white')

		s1=ttk.Separator(self.frame_Leyenda,orient='vertical')
		s1.grid(row=0,column=1,rowspan=2)		

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
		etiqueta_Usuario=Label(self.frame_Leyenda,text=f'{self.usuario}',fg='white',bg='black',font=self.letra_leyenda)
		etiqueta_Usuario.grid(row=0,column=35)	
		self.frame_Leyenda.place(x=0,y=int(self.height*0.84))		

	def calendar_event(self,event):		
		self.llenar_Menu()

	def llenar_Menu(self):

		try:
			self.Lista_Menu.delete(0,'end')
			rows=self.obj_QueryGalen.query_Programacion(self.calendario.selection_get())
			for val in rows:
				self.Lista_Menu.insert(0,str(val.IdServicio)+':'+str(val.IdTurno)+'-'+str(val.IdMedico)+'_'+val.Nombre)
		except Exceptions as e:
			messagebox.showinfo('Alerta',f'Error {e}')

		#llenando las especialidades
		
		try:
			year=self.calendario.selection_get().year
			month=self.calendario.selection_get().month
		
			_,num_days=calendar.monthrange(year,month)
			self.Lista_Especialidad.delete(0,'end')

			rows=self.obj_QueryGalen.query_ProgramacionEspecialidad(f'{year}-{month}-01',f'{year}-{month}-{num_days}')
			for val in rows:
				self.Lista_Especialidad.insert(0,str(val.IdEspecialidad)+'_'+str(val.especialidad))
		except Exceptions as e:
			messagebox.showinfo('Alerta',f'Error {e}')


	def Vista_Cupos(self,event):		
		try:
			data_lista=self.Lista_Menu.get(self.Lista_Menu.curselection()[0])
			self.turno_codi=data_lista[data_lista.find(':')+1:data_lista.find('-')]
			self.IdMedico=data_lista[data_lista.find('-')+1:data_lista.find('_')]
			codigo_servicio=data_lista[:data_lista.find(':')]						
			self.servicio=data_lista[data_lista.find('_')+1:]						
			letra=('Arial',18,'bold')			
			medico=self.obj_QueryGalen.consulta_Medico_Responsable(self.servicio,self.calendario.selection_get(),self.IdMedico,self.turno_codi)	
			for val in medico:
				self.Medico_Datos=val.Nombres+" "+val.ApellidoPaterno+" "+val.ApellidoMaterno
				self.turno=val.Descripcion

			#rows=self.obj_QueryTriaje.query_Cupo(self.calendario.selection_get(),self.servicio,self.Medico_Datos,self.turno)		
						
			self.etiqueta_Turno1.configure(text=f'{self.turno}')
			self.etiqueta_Medico.configure(text=f'Medico : {self.Medico_Datos}')
			self.etiqueta_servicio.configure(text=f'Consultorio : {self.servicio}')
			rows_CantidadCupos=self.obj_QueryTriaje.ConsultaConfCupos(self.IdMedico,codigo_servicio,self.turno,self.calendario.selection_get())
			#llenando campo
			if rows_CantidadCupos:
				self.Entry_Cupos.delete(0,'end')
				self.EntryId_Cupos.configure(state='normal')
				self.EntryId_Cupos.delete(0,'end')
				self.Entry_Cupos.insert('end',rows_CantidadCupos[0].Cantidad)
				self.EntryId_Cupos.insert('end',rows_CantidadCupos[0].Id_Cupos)
				self.EntryId_Cupos.configure(state='readonly')
			else:
				self.Entry_Cupos.delete(0,'end')
				self.EntryId_Cupos.configure(state='normal')
				self.EntryId_Cupos.delete(0,'end')
				self.EntryId_Cupos.configure(state='readonly')

		except Exception as e:
			print(e)

	def Conf_Guardar(self,etiquetaCupos):
		cupos=etiquetaCupos.get()
		try: 
			int(cupos)
			for i in self.Lista_Especialidad.curselection():
				idespecialidad=self.Lista_Especialidad.get(i)[:self.Lista_Especialidad.get(i).find("_")]
				year=self.calendario.selection_get().year
				month=self.calendario.selection_get().month		
				_,num_days=calendar.monthrange(year,month)
				servicios=self.obj_QueryGalen.query_ProgramacionServicios(f'{year}-{month}-01',f'{year}-{month}-{num_days}',idespecialidad)
				for val in servicios:
					cod_servicio=val.IdServicio
					turno=val.Descripcion
					idMedico=val.IdMedico
					fecha=val.fecha
					rows_consulta=self.obj_QueryTriaje.ConsultaConfCupos(idMedico,cod_servicio,turno,fecha)
					if not rows_consulta:
						Now=datetime.datetime.now()
						fechaNow=Now.date()
						ff=datetime.datetime.strptime(str(fecha), "%Y-%m-%d").date()
						if fechaNow<=ff:
							self.obj_QueryTriaje.InsertarCupos([cod_servicio,turno,idMedico,fecha,cupos])

			messagebox.showinfo('Notificacion','Se generó correctamente!!')
			etiquetaCupos.delete(0,'end')
		except Exception as e:
			messagebox.showerror("Error",f"no se pudo Generar {e}")

	def Update_Cupos(self):
		self.EntryId_Cupos.configure(state='normal')
		idcupos=0
		idcupos=self.EntryId_Cupos.get()
		self.EntryId_Cupos.configure(state='readonly')
		cupos=self.Entry_Cupos.get()
		#recuperando datos
		data_lista=self.Lista_Menu.get(self.Lista_Menu.curselection()[0])		
		rows_turnos=self.obj_QueryGalen.query_TipoTurnos(data_lista[data_lista.find(':')+1:data_lista.find('-')])
		turno=rows_turnos[0].Descripcion

		IdMedico=data_lista[data_lista.find('-')+1:data_lista.find('_')]
		codigo_servicio=data_lista[:data_lista.find(':')]
		fecha=self.calendario.selection_get()

		Now=datetime.datetime.now()
		fechaNow=Now.date()
		ff=datetime.datetime.strptime(str(fecha), "%Y-%m-%d").date()
		if fechaNow<=ff:
			if len(idcupos)>0:
				try:
					year=self.calendario.selection_get().year
					month=self.calendario.selection_get().month		
					_,num_days=calendar.monthrange(year,month)
					rows_medico=self.obj_QueryGalen.datos_MedicoDNI(IdMedico)

					rows_cupos_Agendados=self.obj_QueryTriaje.ConsultaCountCuposXdia(rows_medico[0].DNI,codigo_servicio,turno,1,fecha)
					
					agendados=rows_cupos_Agendados[0].cantidad
					if int(agendados)<int(cupos):
						datos={'Cantidad':cupos}
						self.obj_QueryTriaje.Update_DataTables('CUPOS',datos,'Id_Cupos',idcupos)
						messagebox.showinfo('Notificación','Se actualizó correctamente')
					else:
						messagebox.showerror('Error!!','No se puede actualizar la cantidad de cupos asignados es menor a los agendados')
				except Exception as e:
					messagebox.showerror('Error',f'No pudo Actualizarse {e}')
			
			else:
				try:
					self.obj_QueryTriaje.InsertarCupos([codigo_servicio,turno,IdMedico,fecha,cupos])
					messagebox.showinfo('Notificación','Se insertó correctamente')
				except Exception as e:
					messagebox.showerror('Error', f'No pudo insertase {e} !!')
		else:
			messagebox.showerror('Error','No es posible!!')
			

			
		


			
