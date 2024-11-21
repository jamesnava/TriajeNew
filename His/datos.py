from tkinter import *
from tkinter import ttk,filedialog
from tkcalendar import DateEntry
from Consulta_Galen import queryGalen
from Consulta_Triaje import queryTriaje
from tkinter import messagebox
from Util import util
import reporte

class DataHis:
	def __init__(self,dniusurio):
		self.DniUsuario=dniusurio
		self.obj_ConsultaTriaje=queryTriaje()
		self.obj_ConsultaGalen=queryGalen()

	def FrameDataHis(self,frame,width,heigh):
		frame.grid_propagate(False)
		#menu
		self.menu=Menu(frame,tearoff=0)
		self.menu.add_command(label="Ingresar Una interconsulta",command=self.TopInterconsulta)
		self.menu.add_command(label="Actualizar",command=self.TopActualizarInterconsulta)
		self.menu.add_command(label='Eliminar',command=self.EliminarInterconsulta)

		etiqueta=Label(frame,text="Fecha Atencion")
		etiqueta.grid(row=1,column=1,padx=4)
		self.fechaAtencion_G=DateEntry(frame,selectmode='day',date_pattern='dd/mm/yyyy')
		self.fechaAtencion_G.grid(row=1,column=2,padx=4)
		self.fechaAtencion_G.bind("<<DateEntrySelected>>",self.LlenarTablaInterconsulta)

		label=Label(frame,text="Buscar ")
		label.grid(row=1,column=3,pady=10,padx=4)

		txtBuscar=Entry(frame)
		txtBuscar.grid(row=1,column=4,pady=10,padx=4)

		self.table=ttk.Treeview(frame,columns=('#1','#2','#3','#4','#5','#6','#7'),show='headings')
		self.table.heading("#1",text="id")
		self.table.column("#1",width=0,anchor="center")		
		self.table.heading("#2",text="DNI")
		self.table.column("#2",width=60,anchor="center")
		self.table.heading("#3",text="NOMBRES")
		self.table.column("#3",width=200,anchor="center")
		self.table.heading("#4",text="APELLIDOS")
		self.table.column("#4",width=200,anchor="center")
		self.table.heading("#5",text="FECHA INGRESO")
		self.table.column("#5",width=100,anchor="center")		
		self.table.heading("#6",text="FECHA REGISTRO")
		self.table.column("#6",width=100,anchor="center")
		self.table.heading("#7",text="REGISTRADO POR")
		self.table.column("#7",width=100,anchor="center")
		self.table.grid(row=2,column=1,columnspan=4)
		#self.table.bind("<Button-3>",lambda event:)
		self.table.bind("<Button-3>",self.EventoSeleccion)					
		#self.table.place(x=10,y=70,width=1200,height=550)

		label=Label(frame,text='Generar Reporte',cursor='hand2',bg="#828682",fg='#131F75',font=("Helvetica", 16))
		label.bind("<Button-1>",self.Reporte_Produccion)
		label.grid(row=3,column=2,pady=10)

		self.checkVariable=BooleanVar()
		checkHospitalizacion=ttk.Checkbutton(frame,text="Hospitalizacion",variable=self.checkVariable)
		checkHospitalizacion.grid(row=3,column=4,pady=10)

	def Reporte_Produccion(self,event):
		obj_report=reporte.Reporte()
		hospitalizacion=self.checkVariable.get()
		try:
			file_Address=filedialog.asksaveasfile(mode="w",defaultextension=".xlsx")
			#print(self.dniUser,file_Address,self.calendarioHis.selection_get())

			aux=obj_report.Genera_RDatos(self.DniUsuario,file_Address,self.fechaAtencion_G.get_date())
			
			if aux:
				messagebox.showinfo("Alerta","Se generó el archivo correctamente")
			else:
				messagebox.showinfo("Alerta","No pudo generarse")
		except Exception as e:
			messagebox.showinfo("Alerta",f"No pudo generarse el Archivo {e}")


	def EventoSeleccion(self,event):
		item=self.table.identify_row(event.y)
		self.table.selection_set(item)
		self.menu.post(event.x_root,event.y_root)

	def EliminarInterconsulta(self):
		confirmacion=messagebox.askokcancel("Confirmacion","Estás seguro de que quieres Eliminar?")
		if confirmacion:
			ID=self.table.item(self.table.selection()[0],"values")[0]
			nro=self.obj_ConsultaTriaje.query_DeleteHis(ID)
			if nro:
				messagebox.showinfo("Notificación",'Se eliminó correctamente')

	def TopInterconsulta(self):		
		self.TopHis=Toplevel(bg="#074E86")
		self.TopHis.geometry("1100x600")
		self.TopHis.title("Insertar datos His")
		self.TopHis.grab_set()			
		font1=('Comic Sans MS',12,'bold')
		self.validador=0	
		style=ttk.Style()
		style.configure("MyEntry.TEntry",padding=4,foreground="#0000ff")

		etiqueta=Label(self.TopHis,text="DNI PACIENTE :",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=0)
		self.dni_p=StringVar()	

		self.entry_DniPaciente=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry",textvariable=self.dni_p)		
		self.entry_DniPaciente.grid(row=1,column=1,columnspan=3,pady=5)
		self.entry_DniPaciente.bind("<Return>",lambda event:self.search_Paciente(event,self.dni_p.get()))
		
		etiqueta=Label(self.TopHis,text="NOMBRES :",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=4)	

		self.entry_NombrePaciente=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry")
		self.entry_NombrePaciente.grid(row=1,column=5,columnspan=3,pady=5)
		
		etiqueta=Label(self.TopHis,text="APELLIDOS :",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=2,column=0)	

		self.entry_ApellidosPaciente=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry")
		self.entry_ApellidosPaciente.grid(row=2,column=1,columnspan=3,pady=5)	

		etiqueta=Label(self.TopHis,text="HISTORIA CL. :",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=2,column=4)	

		self.entry_HistoriaPaciente=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry")
		self.entry_HistoriaPaciente.grid(row=2,column=5,columnspan=3,pady=5)

		etiqueta=Label(self.TopHis,text="Especialidad:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=3,column=1)	
		self.campoLista=ttk.Combobox(self.TopHis,state='readonly')
		self.campoLista.grid(row=3,column=2)

		etiqueta=Label(self.TopHis,text="Fecha Atencion:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=3,column=3,padx=4)
		self.fechaAtencion=DateEntry(self.TopHis,selectmode='day',date_pattern='dd/mm/yyyy')
		self.fechaAtencion.grid(row=3,column=4,padx=4)
		

		marco_perimetro=LabelFrame(self.TopHis,text="Perimetro y cefálico abdominal",font=("Helvetica",11,"italic"),bg='#074E86',fg='#8E9192')
		marco_perimetro.grid(row=6,column=0,columnspan=5,padx=5)

		etiqueta=Label(marco_perimetro,text="PC:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=1)
		self.entry_PC=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
		self.entry_PC.grid(row=1,column=2,columnspan=2,pady=5)

		etiqueta=Label(marco_perimetro,text="Pab:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=4)
		self.entry_Pab=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
		self.entry_Pab.grid(row=1,column=5,columnspan=2,pady=5)


		marco_perimetro=LabelFrame(self.TopHis,text="Evaluacion Antrometrica Hemoglobina",font=("Helvetica",11,"italic"),bg='#074E86',fg='#8E9192')
		marco_perimetro.grid(row=7,column=0,columnspan=9,padx=5)

		etiqueta=Label(marco_perimetro,text="Peso:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=1)
		self.entry_peso=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
		self.entry_peso.grid(row=1,column=2,columnspan=2,pady=5)

		etiqueta=Label(marco_perimetro,text="Talla:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=4)
		self.entry_talla=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
		self.entry_talla.grid(row=1,column=5,columnspan=2,pady=5)

		etiqueta=Label(marco_perimetro,text="Hb:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=7)
		self.entry_Hb=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
		self.entry_Hb.grid(row=1,column=8,columnspan=2,pady=5)

		etiqueta=Label(self.TopHis,text="Establecimiento:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=8,column=0)
		self.entry_Establecimiento=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry")		
		self.entry_Establecimiento.grid(row=8,column=1,columnspan=2,pady=5)

		etiqueta=Label(self.TopHis,text="Servicio:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=8,column=4)
		self.entry_Servicio=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry")		
		self.entry_Servicio.grid(row=8,column=5,columnspan=2,pady=5)

		marco_perimetro=LabelFrame(self.TopHis,text="Diagnosticos",font=("Helvetica",11,"italic"),bg='#074E86',fg='#8E9192')
		marco_perimetro.grid(row=9,column=0,columnspan=12,padx=5)

		etiqueta=Label(marco_perimetro,text="CIE:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=1)
		self.entry_CIE=ttk.Entry(marco_perimetro,width=20,style="MyEntry.TEntry")
		#self.entry_CIE.bind("<Return>",self.fill_DX)
		self.entry_CIE.configure(state='readonly')
		self.entry_CIE.grid(row=1,column=2,columnspan=2,pady=5)

		etiqueta=Label(marco_perimetro,text="Descripcion:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=4)
		self.entry_Descripcion=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
		self.entry_Descripcion.grid(row=1,column=5,columnspan=2,pady=5)
		self.entry_Descripcion.bind("<Return>",self.Top_searchCie)

		self.combobox_var=StringVar()
		etiqueta=Label(marco_perimetro,text="Tipo Dx:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=7)
		self.entry_tipoDX=ttk.Combobox(marco_perimetro,values=['P','D','R'])		
		self.entry_tipoDX.current(0)
		self.entry_tipoDX.grid(row=1,column=8,columnspan=2,pady=5)

		etiqueta=Label(marco_perimetro,text="LAB:",font=font1,bg='#074E86',fg='#fff')
		etiqueta.grid(row=1,column=10)
		self.entry_LAB=ttk.Entry(marco_perimetro,width=10,style="MyEntry.TEntry")
		self.entry_LAB.grid(row=1,column=11,columnspan=2,pady=5)

		btn_addDX=ttk.Button(marco_perimetro,width=15,text="Agregar")
		btn_addDX['command']=self.Insertar_diagnosticos
		btn_addDX.grid(row=2,column=4)

		btn_quitDX=ttk.Button(marco_perimetro,width=15,text="Quitar")
		btn_quitDX["command"]=self.delete_tableSelected
		btn_quitDX.grid(row=2,column=6)

		style=ttk.Style()
		style.theme_use("default")
		style.configure("Treeview",background="silver",foreground="black",rowheight=25,fieldbackground="silver")
		style.map('Treeview',background=[('selected','green')])

		self.table_datos=ttk.Treeview(marco_perimetro,height=5,columns=('#1','#2','#3','#4'),show='headings')	

		self.table_datos.heading("#1",text="CIE10")
		self.table_datos.column("#1",width=100,anchor="w",stretch='NO')	
		self.table_datos.heading("#2",text="DESCRIPCION")
		self.table_datos.column("#2",width=300,anchor="w",stretch='NO')
		self.table_datos.heading("#3",text="TIPO DX")
		self.table_datos.column("#3",width=200,anchor="w",stretch='NO')
		self.table_datos.heading("#4",text="LAB")
		self.table_datos.column("#4",width=100,anchor="w",stretch='NO')				
		self.table_datos.grid(row=3,column=0,columnspan=20) 
		self.table_datos.configure(height=5)		

		btn_addDatos=ttk.Button(self.TopHis,width=15,text="Agregar")
		btn_addDatos["command"]=self.insertData
		btn_addDatos.grid(row=15,column=2,pady=5)

		btn_cancleDatos=ttk.Button(self.TopHis,width=15,text="Cancelar")
		btn_cancleDatos["command"]=self.TopHis.destroy		
		btn_cancleDatos.grid(row=15,column=4,pady=5)

	def TopActualizarInterconsulta(self):		
		if self.table.selection():
			idAccion=self.table.item(self.table.selection())["values"][0]
			rows=self.obj_ConsultaTriaje.query_SelectTable('HIS_DETA','ID_DETA',idAccion)
			dni=rows[0][1]

			rowsG=self.obj_ConsultaGalen.query_DatosPaciente(dni)
			
			self.TopHisA=Toplevel(bg="#074E86")
			self.TopHisA.geometry("800x500")
			self.TopHisA.title("Actualizar datos His")
			self.TopHisA.resizable(0,0)
			self.TopHisA.grab_set()			
			font1=('Comic Sans MS',12,'bold')
			#self.validador=0	
			style=ttk.Style()
			style.configure("MyEntry.TEntry",padding=4,foreground="#0000ff")

			etiqueta=Label(self.TopHisA,text="DNI PACIENTE :",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=1,column=0)			
			self.dni_p=StringVar()	

			self.entry_DniPaciente=ttk.Entry(self.TopHisA,width=30,style="MyEntry.TEntry",textvariable=self.dni_p)					
			self.entry_DniPaciente.grid(row=1,column=1,columnspan=3,pady=5)			
			self.entry_DniPaciente.insert("end",dni)
			self.entry_DniPaciente['state']='readonly'

			etiqueta=Label(self.TopHisA,text="NOMBRES :",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=1,column=4)	

			self.entry_NombrePaciente=ttk.Entry(self.TopHisA,width=30,style="MyEntry.TEntry")
			self.entry_NombrePaciente.grid(row=1,column=5,columnspan=3,pady=5)
			self.entry_NombrePaciente.insert("end",rowsG[0][0])
			self.entry_NombrePaciente['state']='readonly'
		
			etiqueta=Label(self.TopHisA,text="APELLIDOS :",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=2,column=0)	

			self.entry_ApellidosPaciente=ttk.Entry(self.TopHisA,width=30,style="MyEntry.TEntry")
			self.entry_ApellidosPaciente.grid(row=2,column=1,columnspan=3,pady=5)
			self.entry_ApellidosPaciente.insert("end",rowsG[0][2]+" "+rowsG[0][3])
			self.entry_ApellidosPaciente['state']='readonly'			
		

			marco_perimetro=LabelFrame(self.TopHisA,text="Perimetro y cefálico abdominal",font=("Helvetica",11,"italic"),bg='#074E86',fg='#8E9192')
			marco_perimetro.grid(row=6,column=0,columnspan=5,padx=5)

			etiqueta=Label(marco_perimetro,text="PC:",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=1,column=1)
			self.entry_PC=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
			self.entry_PC.grid(row=1,column=2,columnspan=2,pady=5)
			self.entry_PC.insert("end",rows[0][6])

			etiqueta=Label(marco_perimetro,text="Pab:",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=1,column=4)
			self.entry_Pab=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
			self.entry_Pab.grid(row=1,column=5,columnspan=2,pady=5)
			self.entry_Pab.insert("end",rows[0][2])


			marco_perimetro=LabelFrame(self.TopHisA,text="Evaluacion Antrometrica Hemoglobina",font=("Helvetica",11,"italic"),bg='#074E86',fg='#8E9192')
			marco_perimetro.grid(row=7,column=0,columnspan=9,padx=5)

			etiqueta=Label(marco_perimetro,text="Peso:",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=1,column=1)
			self.entry_peso=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
			self.entry_peso.grid(row=1,column=2,columnspan=2,pady=5)
			self.entry_peso.insert("end",rows[0][3])

			etiqueta=Label(marco_perimetro,text="Talla:",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=1,column=4)
			self.entry_talla=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
			self.entry_talla.grid(row=1,column=5,columnspan=2,pady=5)
			self.entry_talla.insert("end",rows[0][4])

			etiqueta=Label(marco_perimetro,text="Hb:",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=1,column=7)
			self.entry_Hb=ttk.Entry(marco_perimetro,width=30,style="MyEntry.TEntry")
			self.entry_Hb.grid(row=1,column=8,columnspan=2,pady=5)
			self.entry_Hb.insert("end",rows[0][5])

			

			marco_perimetro=LabelFrame(self.TopHisA,text="Diagnosticos",font=("Helvetica",11,"italic"),bg='#074E86',fg='#8E9192')
			marco_perimetro.grid(row=9,column=0,columnspan=12,padx=5)		

			

			style=ttk.Style()
			style.theme_use("default")
			style.configure("Treeview",background="silver",foreground="black",rowheight=25,fieldbackground="silver")
			style.map('Treeview',background=[('selected','green')])

			self.table_datos=ttk.Treeview(marco_perimetro,height=5,columns=('#1','#2','#3','#4','#5'),show='headings')	

			self.table_datos.heading("#1",text="ID")
			self.table_datos.column("#1",width=10,anchor="w",stretch="NO")
			self.table_datos.heading("#2",text="CIE10")
			self.table_datos.column("#2",width=100,anchor="w",stretch='NO')	
			self.table_datos.heading("#3",text="DESCRIPCION")
			self.table_datos.column("#3",width=300,anchor="w",stretch='NO')
			self.table_datos.heading("#4",text="TIPO DX")
			self.table_datos.column("#4",width=200,anchor="w",stretch='NO')
			self.table_datos.heading("#5",text="LAB")
			self.table_datos.column("#5",width=100,anchor="w",stretch='NO')				
			self.table_datos.grid(row=3,column=0,columnspan=20) 
			self.table_datos.configure(height=5)

			rowsDiagnosticos=self.obj_ConsultaTriaje.query_SelectTable('DIAGNOSTICOS','ID_DETA',idAccion)		
			util.llenar_Table(self.table_datos,rowsDiagnosticos,['Id_Diagnostico','CODCIE','Descripcion','TipDx','Lab'])
			self.table_datos.bind("<Double-Button-1>",self.top_EditarCie)

			btn_addDatos=ttk.Button(self.TopHisA,width=15,text="Actualizar")
			btn_addDatos["command"]=lambda:self.UpdateInterconsulta(idAccion)
			btn_addDatos.grid(row=15,column=2,pady=5)

			btn_cancleDatos=ttk.Button(self.TopHisA,width=15,text="Cancelar")
			btn_cancleDatos["command"]=self.TopHisA.destroy		
			btn_cancleDatos.grid(row=15,column=4,pady=5)
		else:
			messagebox.showerror("Alerta","Seleecion un Item")

	def UpdateInterconsulta(self,idHis):
		pc=self.entry_PC.get()
		pab=self.entry_Pab.get()
		peso=self.entry_peso.get()
		talla=self.entry_talla.get()
		hb=self.entry_Hb.get()
		

		for child in self.table_datos.get_children():
			iddiag,descripcion,tipoDx=self.table_datos.item(child)["values"][0],self.table_datos.item(child)["values"][2],self.table_datos.item(child)["values"][3]
			lab,codcie=self.table_datos.item(child)["values"][4],self.table_datos.item(child)["values"][1]
			self.obj_ConsultaTriaje.Update_diagnostico([iddiag,descripcion,tipoDx,lab,codcie])

		self.obj_ConsultaTriaje.Update_DetalleHis(idHis,pc,pab,peso,talla,hb)
		messagebox.showinfo("Notificación","Success!")
		self.TopHisA.destroy()	

	def top_EditarCie(self,event):
		self.top_EditarC=Toplevel()
		self.top_EditarC.title("Buscar Diagnostico")
		self.top_EditarC.iconbitmap('img/buscar.ico')
		self.top_EditarC.geometry("700x100")
		self.top_EditarC.resizable(0,0)
		self.top_EditarC.grab_set()

		itemTable=self.table_datos.selection()[0]
		id_diagnostico=self.table_datos.item(self.table_datos.selection()[0])['values'][0]
	

		label=Label(self.top_EditarC,text="CIE")
		label.grid(row=1,column=1)
		self.cie_entryEditar=ttk.Entry(self.top_EditarC,width=15)
		self.cie_entryEditar.bind("<Return>",self.fill_DXv2)
		self.cie_entryEditar.grid(row=1,column=2)

		label=Label(self.top_EditarC,text="Descripcion")
		label.grid(row=1,column=3)
		self.Descripcion_entryEditar=ttk.Entry(self.top_EditarC,width=30)
		self.Descripcion_entryEditar.grid(row=1,column=4)

		label=Label(self.top_EditarC,text="Tipo")
		label.grid(row=1,column=5)
		self.Tipo_entryEditar=ttk.Combobox(self.top_EditarC,width=15,values=["P","D","R"])
		self.Tipo_entryEditar.current(0)
		self.Tipo_entryEditar.grid(row=1,column=6)

		label=Label(self.top_EditarC,text="Lab")
		label.grid(row=1,column=7)
		self.Lab_entryEditar=ttk.Entry(self.top_EditarC,width=15)
		self.Lab_entryEditar.grid(row=1,column=8)

		button_GrabarDX=ttk.Button(self.top_EditarC,text="Aceptar")
		button_GrabarDX["command"]=lambda:self.insert_TablaEditar(itemTable,id_diagnostico)

		button_GrabarDX.grid(row=2,column=4,pady=5)

	def insert_TablaEditar(self,itemTable,id_diagnostico):
		codigo_cie=self.cie_entryEditar.get()
		descripcionDX=self.Descripcion_entryEditar.get()
		tipoDx=self.Tipo_entryEditar.get()
		lab=self.Lab_entryEditar.get()

		self.table_datos.insert('','end',values=(id_diagnostico,codigo_cie,descripcionDX,tipoDx,lab))
		self.top_EditarC.destroy()
		#self.Top_Editar.grab_set()
		self.table_datos.delete(itemTable)

	def fill_DXv2(self,event):
		param=self.cie_entryEditar.get()
		rows=self.obj_ConsultaTriaje.query_cie10Param(param)

		try:
			self.Descripcion_entryEditar.delete(0,'end')
			self.Descripcion_entryEditar.insert(0,rows[0].NOMBRE)
		except Exception as e:
			messagebox.showerror("Alerta","Datos no Encontrados")			
			self.top_EditarC.destroy()
			self.Top_Editar.grab_set()	

	def llenarCampoEspecialidad(self,combo,dniUser):
		obj_consulta=queryGalen()
		rows=obj_consulta.query_EspecialidadMedico(dniUser)
		lista=[]
		for val in rows:
			lista.append(str(val.IdEspecialidad)+"_"+str(val.Nombre))
		combo.configure(values=lista)
		combo.current(0)

	def search_Paciente(self,event,dni):
		obj_consulta=queryGalen()

		rows=obj_consulta.query_Hospitalizados(dni)
		
		if len(rows):
			rows_Distrito=obj_consulta.query_IdDistritoProcedencia(dni)
			if rows_Distrito[0].NRO:
				for val in rows:
					self.entry_NombrePaciente.insert("end",val.PrimerNombre)
					self.entry_ApellidosPaciente.insert("end",val.ApellidoPaterno+" "+val.ApellidoMaterno)
					self.entry_HistoriaPaciente.insert("end",val.NroHistoriaClinica)
					self.entry_DniPaciente.configure(state='readonly')
					self.entry_NombrePaciente.configure(state="readonly")
					self.entry_ApellidosPaciente.configure(state='readonly')
					self.entry_HistoriaPaciente.configure(state='readonly')
					self.llenarCampoEspecialidad(self.campoLista,self.DniUsuario)
					self.validador=1
			else:
				messagebox.showerror("Error!",f'Actualizar el Distrito de Procedencia del paciente para continuar')

	def Top_searchCie(self,event):
		self.TopCIE=Toplevel(self.TopHis)
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
		self.table_CIE.bind('<<TreeviewSelect>>',self.itemTable_selected)

	def buscar_cie(self,event):
		for item in self.table_CIE.get_children():
			self.table_CIE.delete(item)

		parametro=''		
		if len(self.Entry_buscar_General.get())!=0:
			parametro=parametro+self.Entry_buscar_General.get()
			rows=self.obj_ConsultaTriaje.query_cie10(parametro)

			for valores in rows:
				self.table_CIE.insert('','end',values=(valores.CODCIE,valores.NOMBRE))

	def borrar_tabla(self):
		for item in self.table_CIE.get_children():
			self.table_CIE.delete(item)

	def itemTable_selected(self,event):
		if len(self.table_CIE.focus())!=0:
			self.entry_CIE.configure(state='normal')
			self.entry_CIE.delete(0,'end')
			self.entry_CIE.insert(0,self.table_CIE.item(self.table_CIE.selection()[0],option='values')[0])
			self.entry_Descripcion.delete(0,'end')
			self.entry_Descripcion.insert(0,self.table_CIE.item(self.table_CIE.selection()[0],option='values')[1])
			self.entry_LAB.delete(0,"end")			
			self.entry_CIE.configure(state='readonly')
		self.TopCIE.destroy()

	def Insertar_diagnosticos(self):
		codigo_cie=self.entry_CIE.get()
		descripcion=self.entry_Descripcion.get()
		tipo=self.entry_tipoDX.get()
		lab=self.entry_LAB.get()
		tabladatos=self.diagnosticos_data()
		aux=False
		if codigo_cie:
			if len(tabladatos)>0:			
				for i in range(len(tabladatos)):
					if tabladatos[i][0]==codigo_cie:
						aux=True
						break
			if not aux:
				self.table_datos.insert("",'end',values=(codigo_cie,descripcion,tipo,lab))
			else:
				messagebox.showerror("Alerta","el diagnostico ya existe!!")
		else:
			messagebox.showerror("Error","Ingrese un Diágnostico")
		self.entry_CIE.configure(state='normal')
		self.entry_CIE.delete(0,'end')
		self.entry_CIE.configure(state='readonly')
		self.entry_Descripcion.delete(0,'end')
		self.entry_LAB.delete(0,"end")

	def diagnosticos_data(self):
		diagnosticos=[]
		for item in self.table_datos.get_children():
			valores=self.table_datos.item(item)["values"]
			diagnosticos.append(valores)
		return diagnosticos

	def delete_tableSelected(self):
		try:
			selected_item = self.table_datos.selection()[0]
			self.table_datos.delete(selected_item)	
		except Exception as e:
			messagebox.showinfo("Alerta","Seleccione un Item")

	def insertData(self):
		#recuperando valores

		dni_p=self.dni_p.get()				
		pab_p=self.entry_Pab.get()		
		peso_p=self.entry_peso.get()
		talla_p=self.entry_talla.get()
		hb_p=self.entry_Hb.get()
		pc_p=self.entry_PC.get()
		idespecialidad=self.campoLista.get()[:self.campoLista.get().find("_")]
		fechaAtencion=self.fechaAtencion.get_date()
		fechaAtencion=fechaAtencion.strftime("%d-%m-%Y")

		establecimiento=self.entry_Establecimiento.get()
		servicio=self.entry_Servicio.get()
		#Recuperando servicios
		datos=[dni_p,pab_p,peso_p,talla_p,hb_p,pc_p,idespecialidad,fechaAtencion,self.DniUsuario]
		
		idrows=self.obj_ConsultaTriaje.query_idMAXHIS_DETA()
		id_deta=0
		if idrows[0].codigo!=None:
			id_deta=idrows[0].codigo+1
		else:
			id_deta=1		
		try:
			#comprobar la existencia
			rows_diagnosticos=self.diagnosticos_data()
			if len(rows_diagnosticos)>0:
				if self.validador:				
					self.obj_ConsultaTriaje.insert_HISDETA(id_deta,datos,'IC',establecimiento,servicio)
					for i in range(len(rows_diagnosticos)):
						rows_DIAGNOSTICO=self.obj_ConsultaTriaje.query_idMAX_DIAGNOSTICOS()
						if rows_DIAGNOSTICO[0].codigo!=None:
							id_diag=rows_DIAGNOSTICO[0].codigo+1
						else:
							id_diag=1			
						self.obj_ConsultaTriaje.insert_DIAGNOSTICOS(id_diag,id_deta,rows_diagnosticos[i])
					self.TopHis.destroy()
									
					messagebox.showinfo("Alerta","Se insertó correctamente")
				else:
					messagebox.showerror("Error!!","El Paciente No tiene atencion alguna en el establecimiento")
			else:
				messagebox.showerror("Alerta","Al menos inserte un diagnostico")
		except Exception as e:
			messagebox.showerror("error!!",e)

	def LlenarTablaInterconsulta(self,event):
		obj_consulta=queryGalen()
		fechaAtencion=self.fechaAtencion_G.get_date()
		fechaAtencion=fechaAtencion.strftime("%d-%m-%Y")
		rows=self.obj_ConsultaTriaje.His_Interconsultas(fechaAtencion,self.DniUsuario)
		
		self.borrar_tabla()		
		for valores in rows:
			rowsDatos=obj_consulta.query_DatosPaciente(valores.DNI_PAC)
			self.table.insert('','end',values=(valores.ID_DETA,valores.DNI_PAC,rowsDatos[0].PrimerNombre,rowsDatos[0].ApellidoPaterno+" "+rowsDatos[0].ApellidoMaterno,valores.FechaIngreso,valores.FechaR,valores.DNI_USER))

	def borrar_tabla(self):
		for item in self.table.get_children():
			self.table.delete(item)





