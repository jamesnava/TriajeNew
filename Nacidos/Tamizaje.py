from Consulta_Galen import queryGalen
from Nacidos.consultaN import Consulta
from Consulta_Triaje import queryTriaje
from tkinter import *
from tkinter import ttk,messagebox

class Tamizaje(object):

	def __init__(self,frame,width,height):		
		self.obj_consultaN=Consulta()
		self.obj_ConsultaTriaje=queryTriaje()
		self.frameMadre=frame
		self.width=width
		self.height=height

	def Frame_Tamizaje(self,frame,width,height):
		frameM=Frame(frame,width=width,height=height,bg="#828682")
		frameM.place(x=0,y=0)
		frameM.pack_propagate(False)

		#buttonHistorial=Label(frameM,cursor='hand2',bg='#828682')
		#buttonHistorial.bind("<Button-1>",self.HistorialAlojamiento)
		#buttonHistorial.grid(row=1,column=3,pady=10,padx=10)

		self.menuTamizaje=Menu(frameM,tearoff=0)
		self.menuTamizaje.add_command(label="Datos Tamizaje",command=self.Top_Tamizaje)
		

		letra_leyenda=('Candara',16,'bold italic')
		label=Label(frameM,text="Datos por ingresar pacientes de Tamizaje",bg="#828682",font=letra_leyenda)
		label.grid(row=0,column=1,pady=10,columnspan=20)
		style=ttk.Style()
		style.theme_use("default")
		style.configure("Treeview",background="silver",foreground="black",rowheight=25,fieldbackground="silver")
		style.map('Treeview',background=[('selected','green')])

		self.table_Tamizaje=ttk.Treeview(frameM,columns=('#1','#2','#3','#4','#5','#6'),show='headings')
		self.table_Tamizaje.heading("#1",text="Item")
		self.table_Tamizaje.column("#1",width=30,anchor="w",stretch='NO')
		self.table_Tamizaje.heading("#2",text="DNI MADRE")
		self.table_Tamizaje.column("#2",width=100,anchor="w",stretch='NO')
		self.table_Tamizaje.heading("#3",text="DATOS MADRE")
		self.table_Tamizaje.column("#3",width=500,anchor="w",stretch='NO')
		self.table_Tamizaje.heading("#4",text="DATOS NACIDO")
		self.table_Tamizaje.column("#4",width=200,anchor="w",stretch='NO')
		self.table_Tamizaje.heading("#5",text="HCL NACIDO")
		self.table_Tamizaje.column("#5",width=200,anchor="w",stretch='NO')
		self.table_Tamizaje.heading("#6",text="Fecha Nac. RN")
		self.table_Tamizaje.column("#6",width=200,anchor="w",stretch='NO')						
		self.table_Tamizaje.grid(row=3,column=2,padx=10,pady=2,columnspan=20)
		self.llenarTablaHistorialTAMIZAJE()
		self.table_Tamizaje.bind("<Button-3>",self.EventMenuTamizaje)
		#self.table_Alojamiento.bind('<<TreeviewSelect>>',self.Selection_Table)
		
		#self.table_Alojamiento.bind("<Double-Button-1>",self.top_Alojamiento) 

	def llenarTablaHistorialTAMIZAJE(self):
		rows=self.obj_consultaN.consulta_DigitadosAIRN()
		obj_Paciente=queryGalen()
		for val in rows:
			rowsMadre=obj_Paciente.query_Paciente(val.DNI)
			rowsNacido=obj_Paciente.query_PacienteXHCL(val.HCL)
			self.table_Tamizaje.insert("","end",values=(val.Id_AIR,val.DNI,rowsMadre[0].PrimerNombre+" "+rowsMadre[0].ApellidoPaterno+" "+rowsMadre[0].ApellidoMaterno,rowsNacido[0].PrimerNombre+" "+rowsNacido[0].ApellidoPaterno+" "+rowsNacido[0].ApellidoMaterno,val.HCL,rowsNacido[0].FechaNacimiento))

	def EventMenuTamizaje(self,event):
		item=self.table_Tamizaje.identify_row(event.y)
		self.table_Tamizaje.selection_set(item)
		self.menuTamizaje.post(event.x_root,event.y_root)

	def Top_Tamizaje(self):
		if self.table_Tamizaje.selection():
			idAirn=self.table_Tamizaje.item(self.table_Tamizaje.selection())["values"][0]
			rowsid=self.obj_consultaN.get_idTable("TAMIZAJE","Id_Air",idAirn,"Id_Air")
			if not rowsid:			
				self.top_Tamizaje=Toplevel()
				self.top_Tamizaje.geometry("430x100")
				self.top_Tamizaje.title("Ingresar datos Tamizaje")
				self.top_Tamizaje.grab_set()
				self.top_Tamizaje.resizable(0,0)

				label=Label(self.top_Tamizaje,text="Nro Filtro")
				label.grid(row=1,column=1)
				entry_filtro=Entry(self.top_Tamizaje)
				entry_filtro.grid(row=2,column=1,padx=10)

				label=Label(self.top_Tamizaje,text="1ra Toma")
				label.grid(row=1,column=2)
				entry_Toma1=Entry(self.top_Tamizaje)
				entry_Toma1.grid(row=2,column=2,padx=10)

				label=Label(self.top_Tamizaje,text="2da Toma")
				label.grid(row=1,column=3)
				entry_Toma2=Entry(self.top_Tamizaje)
				entry_Toma2.grid(row=2,column=3,padx=10)

				btn=Button(self.top_Tamizaje,text="Grabar")
				btn.configure(command=lambda:self.insert_tamizaje(idAirn,entry_filtro,entry_Toma1,entry_Toma2))
				btn.grid(row=3,column=2,pady=10)
			else:
				messagebox.showerror("Alerta","Ya cuenta con un registro")
		else:
			messagebox.showerror("Error","Seleccione un Item!!")

	def insert_tamizaje(self,idair,filtro,toma1,toma2):
		fil=filtro.get()
		t1=toma1.get()
		t2=toma2.get()
		nro=self.obj_consultaN.insert_Tamizaje(idair,fil,t1,t2)
		if nro:
			messagebox.showinfo("Notificación","Se insertó correctamente")
			self.top_Tamizaje.destroy()
		else:
			messagebox.showerror("Error","No se pudo insertar!!")
			self.top_Tamizaje.destroy()


