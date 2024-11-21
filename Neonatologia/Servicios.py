from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Consulta_Galen import queryGalen
from Neonatologia.consultaNeonatologia import Consulta
from tktimepicker import SpinTimePickerModern, SpinTimePickerOld
from tktimepicker import constants
from tkcalendar import DateEntry
from datetime import datetime,date
from Util import util



class Servicio():
	
	def __init__(self,usuario,dni,servicio):
		self.usuario=usuario
		self.servicio=servicio		
		self.dni=dni
		self.obj_Galen=queryGalen()
		self.obj_ConsultaNeo=Consulta()
		self.timeDate=datetime.now().strftime("%H:%M:%S")

	def Frame_Servicios(self,frame,width,height):
		#consultando servicio
		descrip_servicio=self.obj_ConsultaNeo.get_IdentificadorTable('DESTINO','ID_DESTINO',self.servicio,'NOMBRE_DESTINO')[0].NOMBRE_DESTINO
		#fin de la consulta
		frameM=Frame(frame,width=width,height=height,bg="#828682")
		frameM.place(x=0,y=0)
		frameM.pack_propagate(False)
		letra_leyenda=('Candara',16,'bold italic')	


		label=Label(frameM,text=f"Pacientes Ingresados al servicio de {descrip_servicio}",fg="#131D52",bg="#828682",font=('Candara',16,'bold italic'))
		label.grid(row=3,column=2,columnspan=20,pady=10)		
		

		style=ttk.Style()
		style.theme_use("default")
		style.configure("Treeview",background="silver",foreground="black",rowheight=25,fieldbackground="silver")
		style.map('Treeview',background=[('selected','green')])
		self.table_IngresosRecepcionados=ttk.Treeview(frameM,columns=('#1','#2','#3','#4','#5','#6'),show='headings')
		self.table_IngresosRecepcionados.heading("#1",text="DNI MADRE")
		self.table_IngresosRecepcionados.column("#1",width=80,anchor="w",stretch='NO')
		self.table_IngresosRecepcionados.heading("#2",text="DATOS MADRE")
		self.table_IngresosRecepcionados.column("#2",width=250,anchor="w",stretch='NO')
		self.table_IngresosRecepcionados.heading("#3",text="HCL NACIDO")
		self.table_IngresosRecepcionados.column("#3",width=80,anchor="w",stretch='NO')
		self.table_IngresosRecepcionados.heading("#4",text="DATOS NACIDO")
		self.table_IngresosRecepcionados.column("#4",width=250,anchor="w",stretch='NO')
		self.table_IngresosRecepcionados.heading("#5",text="ESTADO INGRESO")
		self.table_IngresosRecepcionados.column("#5",width=100,anchor="w",stretch='NO')
		self.table_IngresosRecepcionados.heading("#6",text="ID")
		self.table_IngresosRecepcionados.column("#6",width=0,anchor="w",stretch='NO')							
		self.table_IngresosRecepcionados.grid(row=4,column=2,padx=10,pady=2,columnspan=20)

		self.llenar_Tabla()		

		self.btnIngreso=ttk.Button(frameM,text="Recepcionar")
		self.btnIngreso.grid(row=5,column=9,pady=10)
		self.btnIngreso['command']=self.Top_DatosIngreso

		self.btnEliminar=ttk.Button(frameM,text='Revertir')
		self.btnEliminar.grid(row=5,column=10,padx=5)
		self.btnEliminar['command']=self.Revertir_Transferencia	

		label=Label(frameM,text="Pacientes por dar de Alta",fg="#131D52",font=('Candara',16,'bold italic'))
		label.grid(row=6,column=2,columnspan=20,pady=10)		

		self.table_PacientesAlta=ttk.Treeview(frameM,columns=('#1','#2','#3','#4','#5','#6'),show='headings')
		self.table_PacientesAlta.heading("#1",text="DNI MADRE")
		self.table_PacientesAlta.column("#1",width=80,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#2",text="DATOS MADRE")
		self.table_PacientesAlta.column("#2",width=250,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#3",text="HCL NACIDO")
		self.table_PacientesAlta.column("#3",width=80,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#4",text="DATOS NACIDO")
		self.table_PacientesAlta.column("#4",width=250,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#5",text="CODIGO")
		self.table_PacientesAlta.column("#5",width=100,anchor="w",stretch='NO')
		self.table_PacientesAlta.heading("#6",text="CODRN")
		self.table_PacientesAlta.column("#6",width=0,anchor="w",stretch='NO')						
		self.table_PacientesAlta.grid(row=6,column=2,padx=10,pady=2,columnspan=20)
				
		self.llenar_TablaAlta()

		from Neonatologia import VistaServicios
		obj_Vista=VistaServicios.Vista()
		
		self.menu=Menu(frameM,tearoff=0)
		self.menu.add_command(label="detalle...",command=lambda:obj_Vista.TopDetalle(self.table_PacientesAlta))

		self.table_PacientesAlta.bind("<Button-3>",lambda event:self.EventMenu(event,self.table_PacientesAlta,self.menu))

		self.btnAlta=ttk.Button(frameM,text="Alta")
		self.btnAlta.grid(row=7,column=9,pady=10)
		self.btnAlta['command']=self.Top_DatosAlta
	
	def EventMenu(self,event,table,menu):
		item=table.identify_row(event.y)
		table.selection_set(item)
		menu.post(event.x_root,event.y_root)

	def Revertir_Transferencia(self):
		if self.table_IngresosRecepcionados.selection():
			if messagebox.askquestion(message="¿Estas seguro que desea eliminar?",title="Eliminar"):
				Id_ingreso=util.get_dataTable(self.table_IngresosRecepcionados,5)
				codigoAnterior=self.obj_ConsultaNeo.get_IdentificadorTable('DATOS_INGRESO','Id_DATOSINGRESO',Id_ingreso,'Id_Asociado')[0].Id_Asociado
				'''eliminando...'''
				self.obj_ConsultaNeo.DeleteItemTable('DXNEO','Id_DATOSINGRESO',Id_ingreso)
				self.obj_ConsultaNeo.DeleteItemTable('DATOS_INGRESO','Id_DATOSINGRESO',Id_ingreso)

				#actualizando...
				parametros={'ESTADO':0}		
				self.obj_ConsultaNeo.Update_DataTables('DATOS_INGRESO',parametros,'Id_DATOSINGRESO',codigoAnterior)
				messagebox.showinfo('Alerta!!','Se eliminó correctamente!!')
				self.llenar_Tabla()
		else:
			messagebox.showerror('Error!!','Seleccione un Item!!')

	def llenar_Tabla(self):
		util.borra_Table(self.table_IngresosRecepcionados)						
		rows=self.obj_ConsultaNeo.consulta_Ingresos(self.servicio) if self.servicio else []
		for valor in rows:
			rowsDatosMadre=self.obj_Galen.query_datosPaciente(valor.DNI)
			rowsDatosNacido=self.obj_Galen.query_PacienteXHCL(valor.HC)						
			datosnacido=rowsDatosNacido[0].PrimerNombre+" "+rowsDatosNacido[0].ApellidoPaterno+" "+rowsDatosNacido[0].ApellidoMaterno if rowsDatosNacido else ""
			datosmadre=rowsDatosMadre[0].PrimerNombre+" "+rowsDatosMadre[0].ApellidoPaterno+" "+rowsDatosMadre[0].ApellidoMaterno if rowsDatosMadre else ""
			self.table_IngresosRecepcionados.insert('','end',values=(valor.DNI,datosmadre,valor.HC,datosnacido,"",valor.Id_DATOSINGRESO))


	def llenar_TablaAlta(self):
		util.borra_Table(self.table_PacientesAlta)
		rows=self.obj_ConsultaNeo.consulta_XAlta(self.servicio) if self.servicio else []
	
		for valor in rows:
			rowsDatosMadre=self.obj_Galen.query_datosPaciente(valor.DNI)
			rowsDatosNacido=self.obj_Galen.query_PacienteXHCL(valor.HC)						
			datosnacido=rowsDatosNacido[0].PrimerNombre+" "+rowsDatosNacido[0].ApellidoPaterno+" "+rowsDatosNacido[0].ApellidoMaterno if rowsDatosNacido else ""
			datosmadre=rowsDatosMadre[0].PrimerNombre+" "+rowsDatosMadre[0].ApellidoPaterno+" "+rowsDatosMadre[0].ApellidoMaterno if rowsDatosMadre else ""
			self.table_PacientesAlta.insert('','end',values=(valor.DNI,datosmadre,valor.HC,datosnacido,valor.Id_DATOSINGRESO,valor.ID_INGRESO))

	def Top_DatosIngreso(self):
		if self.table_IngresosRecepcionados.selection():
			self.TopIngreso=Toplevel()
			self.TopIngreso.title("Datos de Ingreso")
			self.TopIngreso.geometry("500x300")
			self.TopIngreso.iconbitmap('img/ingreso.ico')
			self.TopIngreso.resizable(0,0)
			self.TopIngreso.grab_set()
		
			label=Label(self.TopIngreso,text="Fecha Ingreso")
			label.grid(row=1,column=1,pady=10)
			self.FechaIngreso=DateEntry(self.TopIngreso,selectmode='day',date_pattern='yyyy-MM-dd')
			self.FechaIngreso.grid(row=1,column=2,pady=10)

			label=Label(self.TopIngreso,text="Hora")
			label.grid(row=1,column=3,pady=10,padx=10)
			self.time_Ingreso=SpinTimePickerModern(self.TopIngreso)
			self.time_Ingreso.addAll(constants.HOURS24)
			self.time_Ingreso.setMins(str(self.timeDate).split(":")[1])
			self.time_Ingreso.set24Hrs(str(self.timeDate).split(":")[0])
			self.time_Ingreso.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
			self.time_Ingreso.configure_separator(bg="#404040",fg="#fff")
			self.time_Ingreso.grid(row=1,column=4,padx=10,pady=10)

			label=Label(self.TopIngreso,text="Peso")
			label.grid(row=2,column=1,pady=10)
			self.entry_PesoE=ttk.Spinbox(self.TopIngreso,from_=100,to=4000,increment=100)
			self.entry_PesoE.grid(row=2,column=2,pady=10)

			label=Label(self.TopIngreso,text="Medico Resp")
			label.grid(row=2,column=3,pady=10)
			self.entry_MedicoResponsableIngreso=ttk.Entry(self.TopIngreso)
			self.entry_MedicoResponsableIngreso.grid(row=2,column=4,pady=10)
			self.entry_MedicoResponsableIngreso.bind("<Return>",lambda event:self.Search_Personal(event,"DOCTOR"))

			label=Label(self.TopIngreso,text="Enf. Resp")
			label.grid(row=3,column=1,pady=10)
			self.entry_EnfermeraResponsableIngreso=ttk.Entry(self.TopIngreso)
			self.entry_EnfermeraResponsableIngreso.grid(row=3,column=2,pady=10)
			self.entry_EnfermeraResponsableIngreso.bind("<Return>",lambda event:self.Search_Personal(event,"ENFERMERA"))

			label=Label(self.TopIngreso,text="Tecnico Resp")
			label.grid(row=3,column=3,pady=10)
			self.entry_TecnicoResponsableIngreso=ttk.Entry(self.TopIngreso)
			self.entry_TecnicoResponsableIngreso.grid(row=3,column=4,pady=10)		

			buttonAdd=ttk.Button(self.TopIngreso,text="Aceptar")
			buttonAdd.grid(row=5,column=2,columnspan=2,pady=10)
			buttonAdd['command']=self.insert_DatosIngreso
		else:
			messagebox.showerror('Error!!','Seleccione un Item!!')


	def Search_Personal(self,event,identificador):
		self.personall=None
		if identificador=="DOCTOR":
			self.personall="DOCTOR"
			self.Top_searchPersonal()		
		elif identificador=="ENFERMERA":
			self.personall="ENFERMERA"
			self.Top_searchPersonal()
		elif identificador=="MEDICOA":
			self.personall="MEDICOA"
			self.Top_searchPersonal()
		elif identificador=="ENFERMERAA":
			self.personall="ENFERMERAA"
			self.Top_searchPersonal()
		
	def Top_searchPersonal(self):
		self.TopGeneral=Toplevel()
		self.TopGeneral.title('Datos Personales')
		self.TopGeneral.iconbitmap('img/centro.ico')
		self.TopGeneral.geometry("550x350+350+50")
		self.TopGeneral.focus_set()	
		self.TopGeneral.grab_set()
		self.TopGeneral.resizable(0,0)	

		label_title=Label(self.TopGeneral,text='Buscar')
		label_title.place(x=20,y=20)
		self.Entry_buscar_General=ttk.Entry(self.TopGeneral,width=30)
		self.Entry_buscar_General.focus()
		self.Entry_buscar_General.place(x=80,y=20)
		self.Entry_buscar_General.bind('<Key>',self.buscar_DatosPersonales)		

		#tabla...
		self.table_General=ttk.Treeview(self.TopGeneral,columns=('#1','#2'),show='headings')		
		self.table_General.heading("#1",text="CODIGO")
		self.table_General.column("#1",width=100,anchor="center")
		self.table_General.heading("#2",text="DATOS")
		self.table_General.column("#2",width=400,anchor="center")										
		self.table_General.place(x=10,y=70)
		self.table_General.bind('<<TreeviewSelect>>',self.itemTable_selected)			
		#botones de accion
		self.btn_TPG_Close=ttk.Button(self.TopGeneral,text='Cerrar')
		self.btn_TPG_Close.place(x=280,y=365)
		#self.btn_TPG_Close['command']=lambda :self.TopGeneral.destroy()

	def buscar_DatosPersonales(self,event):			
		self.obj_Galen=queryGalen()
		parametro=''
		util.borra_Table(self.table_General)
		if len(self.Entry_buscar_General.get())!=0:
			parametro=parametro+self.Entry_buscar_General.get()
			rows=self.obj_Galen.query_Empleado(parametro)
			for valores in rows:
				self.table_General.insert('','end',values=(valores.DNI,valores.Nombres+" "+valores.ApellidoPaterno+" "+valores.ApellidoMaterno))

	def itemTable_selected(self,event):
		if len(self.table_General.focus())!=0:
			if self.personall=="DOCTOR":				
				self.entry_MedicoResponsableIngreso['state']="normal"
				self.entry_MedicoResponsableIngreso.delete(0,'end')
				self.entry_MedicoResponsableIngreso.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.entry_MedicoResponsableIngreso['state']="readonly"	
				self.TopGeneral.destroy()

			if self.personall=="MEDICOA":				
				self.entry_MedicoResponsableEgreso['state']="normal"
				self.entry_MedicoResponsableEgreso.delete(0,'end')
				self.entry_MedicoResponsableEgreso.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.entry_MedicoResponsableEgreso['state']="readonly"	
				self.TopGeneral.destroy()	

			elif self.personall=="ENFERMERA":
				self.entry_EnfermeraResponsableIngreso['state']="normal"
				self.entry_EnfermeraResponsableIngreso.delete(0,'end')
				self.entry_EnfermeraResponsableIngreso.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.entry_EnfermeraResponsableIngreso['state']="readonly"	
				self.TopGeneral.destroy()

			elif self.personall=="ENFERMERAA":
				self.entry_EnfermeraResponsableEgreso['state']="normal"
				self.entry_EnfermeraResponsableEgreso.delete(0,'end')
				self.entry_EnfermeraResponsableEgreso.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.entry_EnfermeraResponsableEgreso['state']="readonly"	
				self.TopGeneral.destroy()			

	def insert_DatosIngreso(self):

		fecha=self.FechaIngreso.get_date()
		horaIngreso="{}:{}".format(*self.time_Ingreso.time())
		peso=self.entry_PesoE.get()
		self.entry_MedicoResponsableIngreso.configure(state='normal')
		medico=self.entry_MedicoResponsableIngreso.get().strip()

		self.entry_EnfermeraResponsableIngreso.configure(state='normal')
		enfermera=self.entry_EnfermeraResponsableIngreso.get().strip()

		tecnicaenf=self.entry_TecnicoResponsableIngreso.get()	
		
		idDatosIngreso=util.get_dataTable(self.table_IngresosRecepcionados,5)
		datos={'FECHA':f"'{fecha}'",'HORA':f"'{horaIngreso}'",'PESO':peso,'M_RESPONSABLE':f"'{medico}'",'ENF_RESPONSABLE':f"'{enfermera}'",'TEC_RESPONSABLE':f"'{tecnicaenf}'",'USUARIO':f"'{self.usuario}'",'ESTADO':1}

		nro=self.obj_ConsultaNeo.Update_DataTables('DATOS_INGRESO',datos,'Id_DATOSINGRESO',idDatosIngreso)		
		if nro:			
			messagebox.showinfo('Notificación','Ser insertó correctamente')
			self.llenar_Tabla()
			self.llenar_TablaAlta()
			self.TopIngreso.destroy()


	def Top_DatosAlta(self):		
		self.idIngresoA=self.table_PacientesAlta.item(self.table_PacientesAlta.selection()[0],option='values')[4]		
		self.TopEgreso=Toplevel()
		self.TopEgreso.title("Datos de Ingreso")
		self.TopEgreso.iconbitmap('img/alta.ico')
		self.TopEgreso.geometry("600x400")
		self.TopEgreso.grab_set()
		
		label=Label(self.TopEgreso,text="Fecha")
		label.grid(row=1,column=1,pady=10)
		self.FechaAlta=DateEntry(self.TopEgreso,selectmode='day',date_pattern='yyyy-MM-dd')
		self.FechaAlta.grid(row=1,column=2,pady=10)

		label=Label(self.TopEgreso,text="Hora")
		label.grid(row=1,column=3,pady=10,padx=10)
		self.time_Egreso=SpinTimePickerModern(self.TopEgreso)
		self.time_Egreso.addAll(constants.HOURS24)
		self.time_Egreso.setMins(str(self.timeDate).split(":")[1])
		self.time_Egreso.set24Hrs(str(self.timeDate).split(":")[0])
		self.time_Egreso.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
		self.time_Egreso.configure_separator(bg="#404040",fg="#fff")
		self.time_Egreso.grid(row=1,column=4,padx=10,pady=10)
		

		label=Label(self.TopEgreso,text="Medico Resp")
		label.grid(row=2,column=3,pady=10)
		self.entry_MedicoResponsableEgreso=ttk.Entry(self.TopEgreso)
		self.entry_MedicoResponsableEgreso.grid(row=2,column=4,pady=10)
		self.entry_MedicoResponsableEgreso.bind("<Return>",lambda event:self.Search_Personal(event,"MEDICOA"))

		label=Label(self.TopEgreso,text="Enf. Resp")
		label.grid(row=2,column=1,pady=10)
		self.entry_EnfermeraResponsableEgreso=ttk.Entry(self.TopEgreso)
		self.entry_EnfermeraResponsableEgreso.grid(row=2,column=2,pady=10)
		self.entry_EnfermeraResponsableEgreso.bind("<Return>",lambda event:self.Search_Personal(event,"ENFERMERAA"))		

		label=Label(self.TopEgreso,text="Destino.")
		label.grid(row=3,column=1,pady=10)
		self.ComboDestinoAlta=ttk.Combobox(self.TopEgreso)
		self.ComboDestinoAlta.grid(row=3,column=2,pady=10)
		self.llenar_ComboAlta()

		

		self.table_Dx=ttk.Treeview(self.TopEgreso,columns=('#1','#2'),show='headings',height=5)
		self.table_Dx.heading("#1",text="CODIGO")
		self.table_Dx.column("#1",width=100,anchor="w",stretch='NO')
		self.table_Dx.heading("#2",text="DESCRIPCION")
		self.table_Dx.column("#2",width=400,anchor="w",stretch='NO')							
		self.table_Dx.grid(row=6,column=0,pady=2,columnspan=7)
		self.table_Dx.bind("<Button-3>",lambda event:util.EventMenu(event,self.table_Dx,self.menu))
		self.menu=Menu(self.TopEgreso,tearoff=0)
		self.menu.add_command(label="Ingresar Dx",command=self.Top_searchCie)
		self.menu.add_command(label="Quitar Dx",command=lambda :util.borrar_seleccionado(self.table_Dx))

		buttonAdd=ttk.Button(self.TopEgreso,text="Aceptar")
		buttonAdd.grid(row=7,column=2,columnspan=2,pady=10)
		buttonAdd['command']=self.insert_Alta

	def Top_searchCie(self):
		self.TopCIE=Toplevel()
		self.TopCIE.title('Diagnosticos')
		self.TopCIE.geometry("720x400+350+50")
		#self.TopCIE.focus_set()	
		self.TopCIE.grab_set()
		self.TopCIE.resizable(0,0)	
		#self.TopCIE.iconbitmap('image/diagnostico.ico')

		label_title=Label(self.TopCIE,text='Buscar')
		label_title.place(x=20,y=20)
		self.Entry_buscar_General=ttk.Entry(self.TopCIE,width=30)
		self.Entry_buscar_General.focus()
		self.Entry_buscar_General.place(x=80,y=20)
		self.Entry_buscar_General.bind('<Key>',self.buscar_cie)		

		#tabla...
		self.table_CIE=ttk.Treeview(self.TopCIE,columns=('#1','#2'),show='headings')		
		self.table_CIE.heading("#1",text="CODIGO")
		self.table_CIE.column("#1",width=80,anchor="center")
		self.table_CIE.heading("#2",text="CIE")
		self.table_CIE.column("#2",width=200,anchor="center")										
		self.table_CIE.place(x=10,y=70,width=700,height=290)
		self.table_CIE.bind('<<TreeviewSelect>>',lambda event:util.itemTable_SelectedCIE(event,self.table_CIE,self.table_Dx,self.TopCIE))

	def buscar_cie(self,event):		
		util.borra_Table(self.table_CIE)
		parametro=''		
		if len(self.Entry_buscar_General.get())!=0:			
			parametro=parametro+self.Entry_buscar_General.get()			
			rows=self.obj_ConsultaNeo.query_cie10(parametro)			
			for valores in rows:
				self.table_CIE.insert('','end',values=(valores.CODCIE,valores.NOMBRE))

	def llenar_ComboAlta(self):
		rows=self.obj_ConsultaNeo.get_Destinos()
		datos=[]
		for val in rows:
			datos.append(str(val.ID_DESTINO)+"-"+val.NOMBRE_DESTINO)
		if len(datos):
			self.ComboDestinoAlta['values']=datos
			self.ComboDestinoAlta.current(0)

	

	def insert_Alta(self):		
		fechaA=self.FechaAlta.get_date()
		self.entry_MedicoResponsableEgreso.configure(state='normal')
		medico=self.entry_MedicoResponsableEgreso.get().strip()

		self.entry_EnfermeraResponsableEgreso.configure(state='normal')
		enfermera=self.entry_EnfermeraResponsableEgreso.get().strip()		
		
		destino=self.ComboDestinoAlta.get()[:self.ComboDestinoAlta.get().find("-")]

		horaEgreso="{}:{}".format(*self.time_Egreso.time())	

		diagnostico=util.get_Treeview(self.table_Dx,[0,1])

		codigoAnterior=util.get_dataTable(self.table_PacientesAlta,4)

		ID_INGRESO=util.get_dataTable(self.table_PacientesAlta,5)

		recup_destino=self.obj_ConsultaNeo.get_IdentificadorTable('DATOS_INGRESO','Id_DATOSINGRESO',codigoAnterior,'ID_DESTINO')[0].ID_DESTINO

		
		if not int(recup_destino)==int(destino):
			Validar={'Datos Medico':medico,'Datos Enfermera':enfermera,'Diagnosticos':diagnostico}
			if util.validarCampos(Validar):
				#actualizando		
				datos={'FECHAALTA':f"'{str(fechaA)}'",'MEDICOALTA':f"'{medico}'",'HORAALTA':f"'{str(horaEgreso)}'",'ESTADO':2}
				self.obj_ConsultaNeo.Update_DataTables('DATOS_INGRESO',datos,'Id_DATOSINGRESO',codigoAnterior)

				#insertando
				rows=self.obj_ConsultaNeo.get_id('DATOS_INGRESO','Id_DATOSINGRESO')
				idnuevo=(rows[0].ID if not rows[0].ID==None else 0)+1


				campos=['Id_DATOSINGRESO','ID_DESTINO','ESTADO','ID_INGRESO','Id_Asociado']
				valores=(idnuevo,destino,0,ID_INGRESO,codigoAnterior)

				n=self.obj_ConsultaNeo.insertDataTable('DATOS_INGRESO',campos,valores)

				#insertando diagnostico
				valoresDX=util.get_Treeview(self.table_Dx,[0,1])
				for val in valoresDX:			
					camposdx=['CODCIE','Id_DATOSINGRESO','DESCRIPCION']
					valoresdx=(val[0],idnuevo,val[1])
					self.obj_ConsultaNeo.insertDataTable('DXNEO',camposdx,valoresdx)

				if n:
					messagebox.showinfo('Success','Se insertó correctamente!!')			
					self.TopEgreso.destroy()
					self.llenar_TablaAlta()
					self.llenar_Tabla()
				else:
					messagebox.showerror("Alerta","No pudo insertarse")
		else:
			messagebox.showerror("Alerta",'No se puede Transferir al mismo servicio')

		