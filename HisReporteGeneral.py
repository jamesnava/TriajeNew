from tkinter import *
from tkinter import ttk,filedialog
from tkinter import messagebox
from tkcalendar import DateEntry
from Consulta_Galen import queryGalen
from reporte import Reporte


class ReporteHis(object):
	def __init__(self,dni):
		self.dni_user=dni
	def Frame_Reporte(self,frame,ancho,alto):
		frame.grid_propagate(False)
		letra=('Arial',18,'bold')
		label=Label(frame,text="Desde: ",font=letra,bg="#828682")
		label.grid(row=0,column=0,pady=10,padx=10)
		self.fechaDesde=DateEntry(frame,selectmode='day',date_pattern='yyyy-MM-dd')
		self.fechaDesde.grid(row=0,column=1,pady=10,padx=10)
		#self.fechaDesde.bind("<<DateEntrySelected>>",lambda event:self.event_Combo(event,0))

		label=Label(frame,text="Hasta: ",font=letra,bg="#828682")
		label.grid(row=0,column=2,pady=10,padx=10)
		self.fechaHasta=DateEntry(frame,selectmode='day',date_pattern='yyyy-MM-dd')
		self.fechaHasta.grid(row=0,column=3,pady=10,padx=10)
		#self.fechaHasta.bind("<<DateEntrySelected>>",lambda event:self.event_Combo(event,0))

		label=Label(frame,text="Servicios",font=letra,bg="#828682")
		label.grid(row=0,column=4,columnspan=2,pady=10,padx=10)
		self.Entryservicio=ttk.Entry(frame)
		self.Entryservicio.bind("<Return>",self.Top_searchServicio)
		self.Entryservicio.grid(row=0,column=6)


		label=Label(frame,text="Medicos",font=letra,bg="#828682")
		label.grid(row=1,column=1,columnspan=6,pady=10,padx=10)

		self.ListaMedico=Listbox(frame,width=50,height=10)
		self.ListaMedico.grid(row=2,column=3,columnspan=2)
		self.ListaMedico.bind("<<ListboxSelect>>",self.event_lista)

		self.btn_GenerarR=ttk.Button(frame,text="Generar Reporte",state="disabled")
		self.btn_GenerarR.grid(row=3,column=3,columnspan=2,pady=10)
		self.btn_GenerarR["command"]=self.Generar_Reporte

	def Top_searchServicio(self,event):
		self.TopServicio=Toplevel()
		self.TopServicio.title('Medicos')		
		self.TopServicio.geometry("720x400+350+50")			
		self.TopServicio.grab_set()
		self.TopServicio.resizable(0,0)	
		#self.TopCIE.iconbitmap('image/diagnostico.ico')

		label_title=Label(self.TopServicio,text='Buscar')
		label_title.place(x=20,y=20)
		self.Entry_buscar_General=ttk.Entry(self.TopServicio,width=30)
		self.Entry_buscar_General.focus()
		self.Entry_buscar_General.place(x=80,y=20)
		self.Entry_buscar_General.bind('<Key>',self.buscar_especialidad)		

		#tabla...
		self.table_Servicio=ttk.Treeview(self.TopServicio,columns=('#1','#2'),show='headings')		
		self.table_Servicio.heading("#1",text="codigo")
		self.table_Servicio.column("#1",width=80,anchor="center")
		self.table_Servicio.heading("#2",text="Descripcion")
		self.table_Servicio.column("#2",width=200,anchor="center")										
		self.table_Servicio.place(x=10,y=70,width=700,height=290)
		self.table_Servicio.bind('<<TreeviewSelect>>',self.itemTable_selected)


	def buscar_especialidad(self,event):
		obj_ConsultaGalen=queryGalen()
		self.borrar_tabla()
		parametro=''		
		if len(self.Entry_buscar_General.get())!=0:
			parametro=parametro+self.Entry_buscar_General.get()
			rows=obj_ConsultaGalen.query_Especialidades(parametro)
			for valores in rows:
				self.table_Servicio.insert('','end',values=(valores.IdEspecialidad,valores.Nombre))

	def borrar_tabla(self):
		for item in self.table_Servicio.get_children():
			self.table_Servicio.delete(item)

	def itemTable_selected(self,event):
		if len(self.table_Servicio.focus())!=0:
			self.Entryservicio.delete(0,'end')			
			codigo=self.table_Servicio.item(self.table_Servicio.selection()[0],option='values')[0].strip()
			self.Entryservicio.insert(0,codigo)
			#self.medico.insert(0,self.table_CIE.item(self.table_CIE.selection()[0],option='values')[0])			
		self.TopServicio.destroy()
		self.btn_GenerarR.configure(state="disabled")
		self.llenar_Lista(codigo,self.ListaMedico)

	def llenar_Lista(self,codigo,lista):
		lista.delete(0,"end")
		obj_Galen=queryGalen()		
		rows=obj_Galen.datosEmpleadoEspecialidad(codigo)
		for val in rows:
			lista.insert("end",val.DNI.strip()+"_"+val.Nombres+" "+val.ApellidoPaterno+" "+val.ApellidoMaterno)
		


	def event_lista(self,event):
		if self.ListaMedico.curselection():
			self.btn_GenerarR.configure(state="normal")
		

	def Generar_Reporte(self):
		dni=self.ListaMedico.get(self.ListaMedico.curselection())
		dni_=dni[:dni.find("_")]
		file_Address=filedialog.asksaveasfile(mode="w",defaultextension=".xlsx")
		idespecialidad=self.Entryservicio.get()
		fechaI=self.fechaDesde.get_date()
		fechaF=self.fechaHasta.get_date()		
		obj_reporte=Reporte()
		obj_reporte.Genera_RDatosGeneral(dni_,file_Address,fechaI,fechaF,idespecialidad)
		

		
		


