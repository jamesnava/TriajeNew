from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tktimepicker import SpinTimePickerModern, SpinTimePickerOld
from tktimepicker import constants
from Util import util
from Consulta_Galen import queryGalen
from Neonatologia.consultaNeonatologia import Consulta
from tkcalendar import DateEntry
from Consulta_Triaje import queryTriaje

class DATOSGENERALES():
	
	def __init__(self,usuario,dni):
		self.usuario=usuario
		self.dni=dni
		self.obj_Galen=queryGalen()
		self.obj_ConsultaNeo=Consulta()	

	def Top_AddPaciente(self):
		self.dniMadre=None
		self.hclRecienN=None
		self.TopDatos=Toplevel()
		self.TopDatos.geometry("900x500")
		self.TopDatos.title("Ingresar Datos Generales")
		self.TopDatos.grab_set()
		self.TopDatos.resizable(0,0)

		TabControl=ttk.Notebook(self.TopDatos)

		#tabs
		TabMadre=ttk.Frame(TabControl)
		TabNacido=ttk.Frame(TabControl)

		#agregando
		TabControl.add(TabMadre,text='Datos de la Madre')
		TabControl.add(TabNacido,text='Datos del RN')

		#agregando
		TabControl.pack(expand=1,fill='both')

		#datos de ingreso de la madre
		label=Label(TabMadre,text="DNI")
		label.grid(row=1,column=1,pady=5)
		self.entry_DNIMADRE=ttk.Entry(TabMadre)
		self.entry_DNIMADRE.grid(row=1,column=2,padx=10,pady=5)
		self.entry_DNIMADRE.bind("<Return>",lambda event:self.event_Entry(event,'MADRE') )

		label=Label(TabMadre,text="DATOS")
		label.grid(row=1,column=3,pady=5)
		self.entry_DatosMadre=ttk.Entry(TabMadre,width=30,state="readonly")
		self.entry_DatosMadre.grid(row=1,column=4,padx=10,pady=5)

		label=Label(TabMadre,text="Edad G.")
		label.grid(row=2,column=1,pady=5)
		self.entry_EdadGestacional=ttk.Entry(TabMadre)
		self.entry_EdadGestacional.bind("<KeyRelease>",lambda event:util.validarEntero(event,self.entry_EdadGestacional))
		self.entry_EdadGestacional.grid(row=2,column=2,padx=10,pady=5)

		label=Label(TabMadre,text="Direccion")
		label.grid(row=2,column=3,pady=5)
		self.entry_Direccion=ttk.Entry(TabMadre,width=30)		
		self.entry_Direccion.grid(row=2,column=4,padx=10,pady=5)

		label=Label(TabMadre,text="Tipo de Parto")
		label.grid(row=2,column=5,pady=5)
		self.comboParto=ttk.Combobox(TabMadre,values=['EUTOCICO','CESARIA','DISTOCICO'])		
		self.comboParto.grid(row=2,column=6,padx=10,pady=5)
		
		#Tab RN
		labelframeRN=LabelFrame(TabNacido,text='Datos de Recien Nacidos',padx=98)
		labelframeRN.grid(row=0,column=0)
		label=Label(labelframeRN,text="HCL")
		label.grid(row=1,column=1,pady=5)
		self.entry_HCLRN=ttk.Entry(labelframeRN)
		self.entry_HCLRN.grid(row=1,column=2,pady=5,padx=10)
		self.entry_HCLRN.bind("<Return>",lambda event:self.event_Entry(event,'NACIDO') )

		label=Label(labelframeRN,text="Datos")
		label.grid(row=1,column=3,pady=5,padx=5)
		self.entry_DatosRN=ttk.Entry(labelframeRN,width=30)
		self.entry_DatosRN.grid(row=1,column=4,pady=5,padx=10)

		label=Label(labelframeRN,text="L. Nacimiento")
		label.grid(row=1,column=5,pady=5,padx=5)
		self.combo_LugarNacimiento=ttk.Combobox(labelframeRN,values=['Hospital','PS','CS','Trayectoria','Domicilio','Otro'])
		self.combo_LugarNacimiento.grid(row=1,column=6,pady=5,padx=10)
		self.combo_LugarNacimiento.current(0)
		

		labelframeIngreso=LabelFrame(TabNacido,text='Datos de Ingreso',padx=98)
		labelframeIngreso.grid(row=1,column=0)

		label=Label(labelframeIngreso,text="Fecha",font=('Arial',10,'bold'))
		label.grid(row=1,column=1,pady=10)	
		self.fechaAltaA=DateEntry(labelframeIngreso,selectmode='day',date_pattern='yyyy-MM-dd',width=30)
		self.fechaAltaA.grid(row=1,column=2,pady=10,padx=10)

		label=Label(labelframeIngreso,text="Hora",font=('Arial',10,'bold'))
		label.grid(row=1,column=3,pady=10)
		self.time_Ingreso=SpinTimePickerModern(labelframeIngreso)
		self.time_Ingreso.addAll(constants.HOURS24)
		self.time_Ingreso.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
		self.time_Ingreso.configure_separator(bg="#404040",fg="#fff")
		self.time_Ingreso.grid(row=1,column=4,pady=5,padx=10)		

		label=Label(labelframeIngreso,text="Peso",font=('Arial',10,'bold'))
		label.grid(row=1,column=5,pady=10)
		self.entry_Peso=ttk.Entry(labelframeIngreso,width=30)
		self.entry_Peso.grid(row=1,column=6,pady=10)
		
		
		label=Label(labelframeIngreso,text="Destino",font=('Arial',10,'bold'))
		label.grid(row=2,column=1,pady=10)
		self.Destino=ttk.Combobox(labelframeIngreso,state='readonly')
		rows=self.obj_ConsultaNeo.QueryTabla('DESTINO')
		util.llenar_combo(self.Destino,rows,['ID_DESTINO','NOMBRE_DESTINO'])
		self.Destino.grid(row=2,column=2,pady=10)
		self.Destino.current(0)

		label=Label(labelframeIngreso,text="Dr. Resp.",font=('Arial',10,'bold'))
		label.grid(row=2,column=3,pady=10)
		self.entry_DRRESPONSABLE=ttk.Entry(labelframeIngreso,width=30,state='readonly')
		self.entry_DRRESPONSABLE.grid(row=2,column=4,pady=10)
		self.entry_DRRESPONSABLE.bind("<Return>",lambda event:util.Top_searchPersonal(event,self.entry_DRRESPONSABLE))

		label=Label(labelframeIngreso,text="Diágnosticos")
		label.grid(row=3,column=4,pady=5)


		style=ttk.Style()
		style.theme_use("default")
		style.configure("Treeview",background="silver",foreground="black",rowheight=25,fieldbackground="silver")
		style.map('Treeview',background=[('selected','green')])
		self.table_Dx=ttk.Treeview(labelframeIngreso,columns=('#1','#2'),show='headings',height=5)
		self.table_Dx.heading("#1",text="CODIGO")
		self.table_Dx.column("#1",width=100,anchor="w",stretch='NO')
		self.table_Dx.heading("#2",text="DESCRIPCION")
		self.table_Dx.column("#2",width=400,anchor="w",stretch='NO')							
		self.table_Dx.grid(row=4,column=0,pady=2,columnspan=7)
		self.table_Dx.bind("<Button-3>",lambda event:self.EventMenu(event,self.table_Dx,self.menu))
		self.menu=Menu(labelframeIngreso,tearoff=0)
		self.menu.add_command(label="Ingresar Dx",command=self.Top_searchCie)
		self.menu.add_command(label="Quitar Dx",command=lambda :util.borrar_seleccionado(self.table_Dx))


		buttonAdd=ttk.Button(self.TopDatos,text="Guardar")
		buttonAdd.pack()
		buttonAdd['command']=self.insert_DatosPaciente

	def Search_Personal(self,event,identificador):
		self.personall=None
		if identificador=="DOCTOR":
			self.personall="DOCTOR"
			self.Top_searchPersonal()
		elif identificador=="OBSTETRA":
			self.personall="OBSTETRA"
			self.Top_searchPersonal()
		elif identificador=="ENFERMERA":
			self.personall="ENFERMERA"
			self.Top_searchPersonal()
		elif identificador=="MEDICOA":
			self.personall="MEDICOA"
			self.Top_searchPersonal()
		elif identificador=="DOCTORINTERCONSULTA":
			self.personall="DOCTORINTERCONSULTA"
			self.Top_searchPersonal()
		elif identificador=="OBSERVACIONALOJAMIENTO":
			self.personall="OBSERVACIONALOJAMIENTO"
			self.Top_searchPersonal()

	def Top_searchPersonal11(self):
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
		self.table_General.heading("#1",text="DNI")
		self.table_General.column("#1",width=100,anchor="center")
		self.table_General.heading("#2",text="Nombres")
		self.table_General.column("#2",width=400,anchor="center")										
		self.table_General.place(x=10,y=70)
		self.table_General.bind('<<TreeviewSelect>>',self.itemTable_selected)			
		#botones de accion
		self.btn_TPG_Close=ttk.Button(self.TopGeneral,text='Cerrar')
		self.btn_TPG_Close.place(x=280,y=365)
		self.btn_TPG_Close['command']=lambda :self.TopGeneral.destroy()

	def itemTable_selected(self,event):
		if len(self.table_General.focus())!=0:
			if self.personall=="DOCTOR":				
				self.Entry_Medico['state']="normal"
				self.Entry_Medico.delete(0,'end')
				self.Entry_Medico.insert('end',self.table_General.item(self.table_General.selection()[0],option='values')[0])
				self.Entry_Medico['state']="readonly"	
				self.TopGeneral.destroy()
			

	def EventMenu(self,event,table,menu):
		item=table.identify_row(event.y)
		table.selection_set(item)
		menu.post(event.x_root,event.y_root)

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
			obj_query=queryTriaje()
			rows=obj_query.query_cie10(parametro)			
			for valores in rows:
				self.table_CIE.insert('','end',values=(valores.CODCIE,valores.NOMBRE))
	

	def insert_DatosPaciente(self):
		#recuperando datos de la madre
		dnimadre=self.dniMadre if not self.dniMadre==None else ""
		historiaNacido=self.hclRecienN if not self.hclRecienN==None else ""	

		edadgestacional=self.entry_EdadGestacional.get()
		direccion=self.entry_Direccion.get()		
		datosTabla=util.get_Treeview(self.table_Dx,[0,1])

		camposxvalidar={'Dni Madre':dnimadre,'Edad Gestacional':edadgestacional,'Lugar Namiento':self.combo_LugarNacimiento.get(),
		'DRRESPONSABLE':self.entry_DRRESPONSABLE.get(),'Peso':self.entry_Peso.get(),'Diagnostico':datosTabla}
		
		if util.validarCampos(camposxvalidar):
			######ingresando datos de la madre########						
			IdMadre=self.obj_ConsultaNeo.get_id('MADRE','IDMADRE')[0].ID+1
			datos=(IdMadre,dnimadre,edadgestacional,self.usuario,1)

			campos=['IDMADRE','DNI','EGESTACIONAL','usuario','CONTROLADOR']
			nro=self.obj_ConsultaNeo.insertDataTable('MADRE',campos,datos)
			
			if nro:
				#ingresando rnneo
				lnacimiento=self.combo_LugarNacimiento.get()
				IdRN=self.obj_ConsultaNeo.get_id('RNNEO','ID_INGRESO')[0].ID+1 if not self.obj_ConsultaNeo.get_id('RNNEO','ID_INGRESO')[0].ID == None else 1

				datosRN=(IdRN,IdMadre,historiaNacido,lnacimiento)
				camposRN=['ID_INGRESO','IDMADRE','HC','LNACIMIENTO']
				nroRN=self.obj_ConsultaNeo.insertDataTable('RNNEO',camposRN,datosRN)
				#########datos ingreso##################

				Id_datosIngreso=self.obj_ConsultaNeo.get_id('DATOS_INGRESO ','Id_DATOSINGRESO')[0].ID+1 if not self.obj_ConsultaNeo.get_id('DATOS_INGRESO ','Id_DATOSINGRESO')[0].ID == None else 1
				destino=self.Destino.get()
				Fecha=self.fechaAltaA.get_date()
				horaI="{}:{}".format(*self.time_Ingreso.time())
				responsableDR=self.entry_DRRESPONSABLE.get().strip()
				peso=self.entry_Peso.get()

				datosIngreso=(Id_datosIngreso,IdRN,destino[:destino.find("_")],str(Fecha),horaI,responsableDR,peso,1,0)
				camposIngreso=['Id_DATOSINGRESO','ID_INGRESO','ID_DESTINO','FECHA','HORA','M_RESPONSABLE','PESO','ESTADO','Id_Asociado']
				nroIngreso=self.obj_ConsultaNeo.insertDataTable('DATOS_INGRESO',camposIngreso,datosIngreso)

				######ingresando los diagnosticos#############
				for val in datosTabla:
					camposDx=['CODCIE','Id_DATOSINGRESO','DESCRIPCION']
					datosDx=(val[0],Id_datosIngreso,val[1])
					self.obj_ConsultaNeo.insertDataTable('DXNEO',camposDx,datosDx)
				messagebox.showinfo("Notificación","Se insertó correctamente!")
				self.TopDatos.destroy()				
		
			
	def event_Entry(self,event,manejador):
		
		if manejador=='MADRE':
			dni=self.entry_DNIMADRE.get()
			rows=self.obj_Galen.query_datosPaciente(dni)

			if len(rows)>0:
				self.dniMadre=dni
				nombresmadres=rows[0].PrimerNombre+" "+rows[0].ApellidoPaterno+" "+rows[0].ApellidoMaterno
				self.entry_DatosMadre.configure(state='normal')
				self.entry_DatosMadre.delete(0,'end')
				self.entry_DatosMadre.insert("end",nombresmadres)
				self.entry_DatosMadre.configure(state='readonly')

		else:
			hclRN=self.entry_HCLRN.get()
			rows=self.obj_Galen.query_PacienteXHCL(hclRN)
			if len(rows)>0:
				self.hclRecienN=hclRN
				nombresNacido=rows[0].PrimerNombre+" "+rows[0].ApellidoPaterno+" "+rows[0].ApellidoMaterno
				self.entry_DatosRN.configure(state='normal')
				self.entry_DatosRN.delete(0,'end')
				self.entry_DatosRN.insert("end",nombresNacido)
				self.entry_DatosRN.configure(state='readonly')
	

