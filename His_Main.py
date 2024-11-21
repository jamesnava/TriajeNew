from tkinter import *
from tkcalendar import Calendar
from tkinter import ttk,filedialog
import datetime
from datetime import date,timedelta
from Consulta_Galen import queryGalen
from tkinter import messagebox
from Operaciones import operaciones
from Consulta_Triaje import queryTriaje
#from ghrap import grafica
import reporte



class HisV(object):

	def __init__(self,usuario,dniuser):
		self.usuario=usuario
		self.dniUser=dniuser
		self.obj_ConsultaGalen=queryGalen()
		self.obj_ConsultaTriaje=queryTriaje()
		self.obj_operaciones=operaciones()
		self.TopHis=None
		

	def frame_His(self,frame,ancho,alto):
		self.frame=frame
		self.ancho=ancho
		self.alto=alto

		self.FrameLeft=Frame(frame,width=240,height=int(alto*0.8))
		self.FrameLeft.place(x=10,y=10)
		self.FrameLeft.grid_propagate(False)
		date=datetime.datetime.now()

		self.calendarioHis=Calendar(self.FrameLeft,selectmode='day',year=date.year,month=date.month,day=date.day)
		self.calendarioHis.bind('<<CalendarSelected>>',lambda event:self.Llenar_Atenciones(event,frame,ancho,alto))
		self.calendarioHis.grid(row=0,column=1,columnspan=3)

		self.Lista_Menu=Listbox(self.FrameLeft,height=int(alto*0.03),width=37,selectforeground='#ffffff',selectbackground="#00aa00",selectborderwidth=2,cursor='hand2')
		#self.llenar_Menu()
		self.Lista_Menu.bind('<<ListboxSelect>>',self.frameDerecha)
		self.Lista_Menu.grid(row=1,column=0,columnspan=3)
		scroll_bar=Scrollbar(self.FrameLeft)
		scroll_bar.grid(row=1,column=4)
		self.Lista_Menu.configure(yscrollcommand=scroll_bar.set)
		scroll_bar.configure(command=self.Lista_Menu.yview)

		self.FrameRight=Frame(frame,width=int(ancho*0.85),height=int(alto*0.8),bg='#D1DAE2')
		self.FrameRight.place(x=270,y=10)
		self.FrameRight.grid_propagate(False)

		self.FrameBottom=Frame(frame,width=int(ancho*0.99),height=int(alto*0.09),bg='#D1DAE2')
		self.FrameBottom.place(x=10,y=int(alto*0.82))
		self.FrameBottom.grid_propagate(False)		
	

	def frameBottomWidget(self,n,todos,digitados):
		if n:			
			framegraph=Frame(self.FrameBottom,width=100,height=100)
			framegraph.grid(row=0,column=0,columnspan=2)
			framegraph.grid_propagate(False)
			#grafica(framegraph,todos,digitados,self.alto*0.09)
			rowsP=self.obj_ConsultaTriaje.query_Paciente(self.dniUser)
			
			label=Label(self.FrameBottom,text=f"Medico Responsable:{rowsP[0].Nombre} {rowsP[0].Apellido_Paterno} {rowsP[0].Apellido_Materno}",bg='#D1DAE2',font=("Helvetica",13,"italic"),fg="#000")
			label.grid(row=0,column=3,columnspan=2,padx=15)

			label=Label(self.FrameBottom,text="Reporte",bg='#D1DAE2',font=("Helvetica",11,"italic"),fg="blue",cursor='hand2')
			label.bind("<Button-1>",self.Reporte_Produccion)
			label.grid(row=0,column=6,columnspan=2,padx=15)
		else:
			self.FrameBottom=Frame(self.frame,width=int(self.ancho*0.99),height=int(self.alto*0.09),bg='#D1DAE2')
			self.FrameBottom.place(x=10,y=int(self.alto*0.82))
			self.FrameBottom.grid_propagate(False)

	def Reporte_Produccion(self,event):
		obj_report=reporte.Reporte()
		try:
			file_Address=filedialog.asksaveasfile(mode="w",defaultextension=".xlsx")
			#print(self.dniUser,file_Address,self.calendarioHis.selection_get())
			aux=obj_report.Genera_RDatos(self.dniUser,file_Address,self.calendarioHis.selection_get())
			if aux:
				messagebox.showinfo("Alerta","Se generó el archivo correctamente")
			else:
				messagebox.showinfo("Alerta","No pudo generarse")
		except Exception as e:
			messagebox.showinfo("Alerta",f"No pudo generarse el Archivo {e}")

	def frameDerecha(self,event):
		
		rows=self.obj_ConsultaTriaje.consultaRegistroPaciente(self.Lista_Menu.get(self.Lista_Menu.curselection())[:8],self.IdEspecialidad,self.calendarioHis.selection_get())		
				
		insertButton=ttk.Button(self.FrameRight,text="Insertar Datos")
		insertButton.grid(row=0,column=0,pady=10,padx=10)		
		if not rows:
			if date.today()-timedelta(days=5)<=self.calendarioHis.selection_get():
				insertButton["command"]=lambda:self.Top_His(self.Lista_Menu.get(self.Lista_Menu.curselection())[:8])
			else:
				messagebox.showerror("Error!!","La inserción solo será posible dentro de los 5 dias, desde la antención ")
		else:			
			insertButton["state"]="disabled"

		marco_Insert=LabelFrame(self.FrameRight,text="Produccion His",font=("Helvetica",11,"italic"),bg='#D1DAE2',width=700,height=600)
		marco_Insert.grid(row=1,column=0,columnspan=9,padx=5)
		marco_Insert.grid_propagate(False)

		font1=('Comic Sans MS',12,'bold')
		style=ttk.Style()
		style.configure("MyEntry.TEntry",padding=6,foreground="#0000ff")
		dni=self.Lista_Menu.get(self.Lista_Menu.curselection())[:8]		
		rowsHisDeta=self.obj_ConsultaTriaje.Query_HisDeta(dni,self.IdEspecialidad,self.calendarioHis.selection_get())

		label=Label(marco_Insert,text="Numero de Registro",font=font1,bg='#D1DAE2')
		label.grid(row=0,column=0)

		Entry_IdRegistro=ttk.Entry(marco_Insert,width=15,style="MyEntry.TEntry")		
		Entry_IdRegistro.grid(row=0,column=1,pady=5)

		self.varActualizar=IntVar()
		checkButton=Checkbutton(marco_Insert,text="Actualizar",variable=self.varActualizar,onvalue=1,offvalue=0)
		checkButton.grid(row=0,column=3,columnspan=15,sticky="e")					

		label=Label(marco_Insert,text="PC",font=font1,bg='#D1DAE2')
		label.grid(row=1,column=0)

		Entry_PC=ttk.Entry(marco_Insert,width=15,style="MyEntry.TEntry")		
		Entry_PC.grid(row=1,column=1,pady=5)	

		label=Label(marco_Insert,text="Pab",font=font1,bg='#D1DAE2')
		label.grid(row=1,column=2,pady=5)

		Entry_Pab=ttk.Entry(marco_Insert,width=15,style="MyEntry.TEntry")		
		Entry_Pab.grid(row=1,column=3,pady=5)

		label=Label(marco_Insert,text="Peso",font=font1,bg='#D1DAE2')
		label.grid(row=2,column=0)

		Entry_Peso=ttk.Entry(marco_Insert,width=15,style="MyEntry.TEntry")		
		Entry_Peso.grid(row=2,column=1,pady=5)	

		label=Label(marco_Insert,text="Talla",font=font1,bg='#D1DAE2')
		label.grid(row=2,column=2,pady=5)

		Entry_Talla=ttk.Entry(marco_Insert,width=15,style="MyEntry.TEntry")		
		Entry_Talla.grid(row=2,column=3,pady=5)

		label=Label(marco_Insert,text="HB",font=font1,bg='#D1DAE2')
		label.grid(row=3,column=0,pady=5)

		Entry_Hb=ttk.Entry(marco_Insert,width=15,style="MyEntry.TEntry")		
		Entry_Hb.grid(row=3,column=1,pady=5)
		
		id_deta=None
		if rowsHisDeta:
			id_deta=rowsHisDeta[0].ID_DETA
			Entry_IdRegistro.insert(0,id_deta)
			Entry_IdRegistro["state"]="readonly"
			Entry_PC.insert(0,rowsHisDeta[0].PC)
			Entry_Pab.insert(0,rows[0].PAB)
			Entry_Peso.insert(0,rows[0].Peso)
			Entry_Talla.insert(0,rows[0].Talla)
			Entry_Hb.insert(0,rows[0].Hb)


		self.table_editar=ttk.Treeview(marco_Insert,height=3,columns=('#1','#2','#3','#4','#5'),show='headings')
		self.table_editar.heading("#1",text="ID")
		self.table_editar.column("#1",width=50,anchor="w",stretch='NO')
		self.table_editar.heading("#2",text="DESCRIPCION")
		self.table_editar.column("#2",width=350,anchor="w",stretch='NO')	
		self.table_editar.heading("#3",text="Tipo DX")
		self.table_editar.column("#3",width=80,anchor="w",stretch='NO')
		self.table_editar.heading("#4",text="LAB")
		self.table_editar.column("#4",width=80,anchor="w",stretch='NO')
		self.table_editar.heading("#5",text="CIE")
		self.table_editar.column("#5",width=80,anchor="w",stretch='NO')				
		self.table_editar.grid(row=4,column=0,padx=10,columnspan=20)
		self.table_editar.bind("<Double-Button-1>",self.top_EditarCie) 
		self.table_editar.configure(height=5)

		if id_deta:		
			self.llenar_EditaDiagnostico(id_deta)


		btn_guardar=ttk.Button(marco_Insert,width=10,text="Grabar")
		##error here
		Entry_IdRegistro['state']='normal'
		codigo=Entry_IdRegistro.get()
		Entry_IdRegistro['state']='readonly'
		btn_guardar["command"]=lambda:self.Update_Deta(codigo,Entry_PC.get(),Entry_Pab.get(),Entry_Peso.get(),Entry_Talla.get(),Entry_Hb.get())
		btn_guardar.grid(row=9,column=2,pady=5)

		btn_Eliminar=ttk.Button(marco_Insert,width=10,text="Eliminar")
		btn_Eliminar["command"]=lambda:self.delete_His(codigo)
		btn_Eliminar.grid(row=9,column=3)
	
	def delete_His(self,codigo):
		if date.today()==self.calendarioHis.selection_get():
			nro=None
			nro=self.obj_ConsultaTriaje.query_DeleteHis(codigo)
			if nro:
				messagebox.showinfo("Alerta","Se eliminó correctamente!!")
		else:
			messagebox.showinfo("Alerta","No es posible eliminar, debe eliminarse dentro de las 24 horas")


	def Update_Deta(self,codigo,pc,pab,peso,talla,hb):
		if self.varActualizar.get():
			if date.today()-timedelta(days=3)<=self.calendarioHis.selection_get():
				iden=self.table_editar.get_children()
				dat=[]
				for a in iden:
					datos=self.table_editar.item(a)["values"]			
					self.obj_ConsultaTriaje.Update_diagnostico(datos)
				
				nro=self.obj_ConsultaTriaje.Update_DetalleHis(codigo,pc,pab,peso,talla,hb)
				if nro>0:
					messagebox.showinfo('Alerta','Successful!')
			else:
				messagebox.showinfo("Notificación","No es posible Modificar, solo es posible dentro de los 3 dias, desde el registro!")
		else:
			messagebox.showinfo("Notificación","Para Modificar marque el casillero 'Actualizar'")
			

	def llenar_EditaDiagnostico(self,iddeta):
		rows=self.obj_ConsultaTriaje.query_DIAGNOSTICOS(iddeta)
		for data in rows:
			self.table_editar.insert('','end',values=(data.Id_Diagnostico,data.Descripcion,data.TipDx,data.Lab,data.CODCIE))

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

	def top_EditarCie(self,event):
		self.top_EditarC=Toplevel()
		self.top_EditarC.title("Buscar Diagnostico")
		self.top_EditarC.iconbitmap('img/buscar.ico')
		self.top_EditarC.geometry("700x100")
		self.top_EditarC.resizable(0,0)
		self.top_EditarC.grab_set()

		itemTable=self.table_editar.selection()[0]
		id_diagnostico=self.table_editar.item(self.table_editar.selection()[0])['values'][0]
	

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

		self.table_editar.insert('','end',values=(id_diagnostico,descripcionDX,tipoDx,lab,codigo_cie))
		self.top_EditarC.destroy()
		#self.Top_Editar.grab_set()
		self.table_editar.delete(itemTable)

	def Top_His(self,dni):
		if self.Lista_Menu.curselection():
			if self.TopHis:
				self.TopHis.destroy()
			self.TopHis=Toplevel(bg="#074E86")
			self.TopHis.geometry("1100x800")
			self.TopHis.title("Insertar datos His")
			self.TopHis.grab_set()
			#self.codigo_HISCABE=codigo
			#self.codigo_servicio=servicio
			font1=('Comic Sans MS',12,'bold')
			
			style=ttk.Style()
			style.configure("MyEntry.TEntry",padding=4,foreground="#0000ff")

			etiqueta=Label(self.TopHis,text="DNI PACIENTE :",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=1,column=0)
			self.dni_p=StringVar()	

			self.entry_DniPaciente=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry",textvariable=self.dni_p)
			self.entry_DniPaciente.grid(row=1,column=1,columnspan=3,pady=5)
		
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

			etiqueta=Label(self.TopHis,text="FINANCIAMIENTO :",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=3,column=0)
			self.combo_financiamiento=ttk.Combobox(self.TopHis,width=30,style="MyEntry.TEntry",values=['SIS','PARTICULAR','SALUDPOL','SOAT','OTRO'],state='readonly')
			self.combo_financiamiento.current(0)
			self.combo_financiamiento.unbind("<<ComboboxSelected>>")
			self.combo_financiamiento.grid(row=3,column=1,columnspan=3,pady=5)	

			etiqueta=Label(self.TopHis,text="ETNIA:",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=3,column=4)
			self.entry_EtniaPaciente=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry")
			self.entry_EtniaPaciente.grid(row=3,column=5,columnspan=3,pady=5)

			etiqueta=Label(self.TopHis,text="GENERO :",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=4,column=0)
			self.entry_GENERO=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry")
			self.entry_GENERO.grid(row=4,column=1,columnspan=3,pady=5)

			etiqueta=Label(self.TopHis,text="EDAD:",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=4,column=4)
			self.entry_EdadPaciente=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry")
			self.entry_EdadPaciente.grid(row=4,column=5,columnspan=3,pady=5)

			etiqueta=Label(self.TopHis,text="Distrito Proc.:",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=5,column=0)
			self.entry_DistritoProcedencia=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry")
			self.entry_DistritoProcedencia.grid(row=5,column=1,columnspan=3,pady=5)

			etiqueta=Label(self.TopHis,text="CT. POBLADO:",font=font1,bg='#074E86',fg='#fff')
			etiqueta.grid(row=5,column=4)
			self.entry_CentroPoblado=ttk.Entry(self.TopHis,width=30,style="MyEntry.TEntry")
			self.entry_CentroPoblado.grid(row=5,column=5,columnspan=3,pady=5)

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
			self.llenar_datosPaciente()

			btn_addDatos=ttk.Button(self.TopHis,width=15,text="Agregar")
			btn_addDatos["command"]=lambda:self.insertData(dni)
			btn_addDatos.grid(row=15,column=2,pady=5)
			btn_cancleDatos=ttk.Button(self.TopHis,width=15,text="Cancelar")
			#btn_cancleDatos["command"]=self.Top_His.destroy		
			btn_cancleDatos.grid(row=15,column=4,pady=5)
		else:
			messagebox.showinfo("Alerta","Seleccione un Item!")

	def insertData(self,dni):
		#recuperando valores
		dni_p=dni				
		pab_p=self.entry_Pab.get()		
		peso_p=self.entry_peso.get()
		talla_p=self.entry_talla.get()
		hb_p=self.entry_Hb.get()
		pc_p=self.entry_PC.get()

		establecimiento=self.entry_Establecimiento.get()
		servicio=self.entry_Servicio.get()
		
		#Recuperando servicios
		datos=[dni_p,pab_p,peso_p,talla_p,hb_p,pc_p,self.IdEspecialidad,self.calendarioHis.selection_get(),self.dniUser]
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
				
				self.obj_ConsultaTriaje.insert_HISDETA(id_deta,datos,'CE',establecimiento,servicio)

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
				messagebox.showerror("Alerta","Al menos inserte un diagnostico")			

		except Exception as e:
			messagebox.showerror("error!!",e)


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
		self.borrar_tabla()
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

	def delete_tableSelected(self):
		try:
			selected_item = self.table_datos.selection()[0]
			self.table_datos.delete(selected_item)	
		except Exception as e:
			messagebox.showinfo("Alerta","Seleccione un Item")

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

	def llenar_datosPaciente(self):
		dni=self.Lista_Menu.get(self.Lista_Menu.curselection())[:8]		
		today = date.today()
		rows=self.obj_ConsultaGalen.query_PacienteV1(dni)					
		
		for val in rows:			
			#rows=self.obj_consultaGalen.query_Paciente(dni)
			self.entry_DniPaciente.insert(0,val.NroDocumento)										
			self.entry_NombrePaciente.insert(0,val.PrimerNombre)
			self.entry_ApellidosPaciente.insert(0,val.ApellidoPaterno+" "+val.ApellidoMaterno)
			self.entry_HistoriaPaciente.insert(0,val.NroHistoriaClinica)
			self.entry_GENERO.insert(0,val.Descripcion)
			self.entry_EtniaPaciente.insert(0,val.IdEtnia)
			self.entry_DistritoProcedencia.insert(0,val.Nombre)
			fechanacimiento=val.FECHANACIMIENTO				
			edad=int(today.year)-int(fechanacimiento[:4])
			self.entry_EdadPaciente.insert(0,edad)
			establecimiento,servicio=self.obj_operaciones.VEstablecimiento(dni,self.IdEspecialidad)

			self.entry_Establecimiento.insert(0,establecimiento)
			#self.entry_Establecimiento["state"]="readonly"				
			self.entry_Servicio.insert(0,servicio)
			#self.entry_Servicio["state"]="readonly"		
		

	def Llenar_Atenciones(self,event,frame,ancho,alto):

		self.FrameRight=Frame(frame,width=int(ancho*0.85),height=int(alto*0.8),bg='#D1DAE2')
		self.FrameRight.place(x=270,y=10)
		self.FrameRight.grid_propagate(False)

		rowsmedicinafisica=self.obj_ConsultaGalen.query_PerteneceMedicinaFisica(self.dniUser,self.calendarioHis.selection_get())
		
			
		valor=rowsmedicinafisica[0]
		try:
			self.Lista_Menu.delete(0,'end')			
			if valor:
				
				rows=self.obj_ConsultaGalen.query_TodosMedicinaFisica(self.calendarioHis.selection_get())
			else:
								
				rows=self.obj_ConsultaGalen.query_Atenciones(self.calendarioHis.selection_get(),self.dniUser)

			self.IdEspecialidad=rows[0].IdEspecialidad
			n=0			
			digitados=0
			for val in rows:
				dni=val.DNIPACIENTE
				self.Lista_Menu.insert(n,dni+":"+val.PrimerNombre+" "+val.ApellidoPaterno+" "+val.ApellidoMaterno)
				rowsE=self.obj_ConsultaTriaje.consultaRegistroPaciente(dni,self.IdEspecialidad,self.calendarioHis.selection_get())
				if rowsE:
					digitados+=1
					self.Lista_Menu.itemconfig(n,{'bg':'OrangeRed3'})
				n+=1
			self.frameBottomWidget(1,len(rows),digitados)
		except Exception as e:
			messagebox.showinfo('Alerta','No hay pacientes, Atendidos!!')
			self.frameBottomWidget(0,0,0)
		

	

