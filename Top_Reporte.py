from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from tkdocviewer import *
import os
import datetime
import Consulta_Triaje
import Consulta_Galen
import Impresion

class Reporte(object):
	def __init__(self):
		self.font_text=('Candara',12,'bold')
		self.obj_ConsultaGalen=Consulta_Galen.queryGalen()
		self.obj_ConsultaTriaje=Consulta_Triaje.queryTriaje()
		self.obj_Impresion=Impresion.Reporte()

	def Top_Reporte(self):
		self.ventana_Reporte=Toplevel()
		self.ventana_Reporte.geometry('450x300+250+100')
		self.ventana_Reporte.attributes('-topmost',True)
		self.ventana_Reporte.overrideredirect(True)
		self.ventana_Reporte.title('Reporte')

		date=datetime.datetime.now()

		etiqueta_fecha=Label(self.ventana_Reporte,text='Seleccione Fecha: ',font=self.font_text,fg='#105B79')
		etiqueta_fecha.grid(row=1,column=0,pady=10)
		self.calendario=Calendar(self.ventana_Reporte,selectmode='day',year=date.year,month=date.month,day=date.day)
		self.calendario.grid(row=1,column=1,columnspan=2)
		self.calendario.bind('<<CalendarSelected>>',self.Llenar_Combobox)
		etiqueta_servicio=Label(self.ventana_Reporte,text='Consultorio',font=self.font_text,fg='#105B79')
		etiqueta_servicio.grid(row=2,column=0,pady=10)
		self.current_var=StringVar()
		self.Lista_Consultorio=ttk.Combobox(self.ventana_Reporte,textvariable=self.current_var,width=30)
		self.Lista_Consultorio.grid(row=2,column=1,pady=10,columnspan=2)	

		self.btn_Guardar=ttk.Button(self.ventana_Reporte,text='GENERAR')
		self.btn_Guardar['command']=self.Generar_Reporte
		self.btn_Guardar.grid(row=4,column=1)	

		self.btn_Cancelar=ttk.Button(self.ventana_Reporte,text='CANCELAR')
		self.btn_Cancelar['command']=self.ventana_Reporte.destroy
		self.btn_Cancelar.grid(row=4,column=2)
		self.ventana_Reporte.focus()
		self.ventana_Reporte.grab_set()	
		self.ventana_Reporte.mainloop()
	def Llenar_Combobox(self,event):		
		lista=[]		
		rows=self.obj_ConsultaGalen.query_Programacion(self.calendario.selection_get())
		for val in rows:
			lista.append(str(val.IdTurno)+'-'+str(val.IdMedico)+'_'+val.Nombre)
		lista.append('1-1_TODOS')
		self.Lista_Consultorio['values']=lista			
	def Generar_Reporte(self):
		fecha=self.calendario.selection_get()
		consultorio_total=self.Lista_Consultorio.get()

		consultorio_get=consultorio_total[consultorio_total.find('_')+1:]
		turno=consultorio_total[:consultorio_total.find('-')]
		turno_Name=''
		if int(turno)==33:
			turno_Name='Consulta Externa - Tarde'
		elif int(turno)==4:
			turno_Name='Consulta Externa -  mañana'
		
		
		self.ventana_Reporte.destroy()
		self.Windows_Reporte=Toplevel()
		self.Windows_Reporte.geometry('1000x650')
		self.Windows_Reporte.title('Reporte de pacientes con citas')
		self.table=ttk.Treeview(self.Windows_Reporte,columns=('#1','#2','#3','#4','#5','#6','#7','#8','#9','#10','#11','#12','#13'),show='headings')		
		self.table.heading("#1",text="DNI")
		self.table.column("#1",width=60,anchor="center")
		self.table.heading("#2",text="NOMBRES")
		self.table.column("#2",width=200,anchor="center")
		self.table.heading("#3",text="APELLIDOS")
		self.table.column("#3",width=200,anchor="center")
		self.table.heading("#4",text="TELEFONO")
		self.table.column("#4",width=80,anchor="center")		
		self.table.heading("#5",text="PROCEDENCIA")
		self.table.column("#5",width=200,anchor="center")
		self.table.heading("#6",text="NRO CUPO")
		self.table.column("#6",width=50,anchor="center")
		self.table.heading("#7",text="NRO REFERENCIA")
		self.table.column("#7",width=100,anchor="center")
		self.table.heading("#8",text="ESTABLECIMIENTO")
		self.table.column("#8",width=150,anchor="center")
		self.table.heading("#9",text="CONSULTORIO")
		self.table.column("#9",width=300,anchor="center")
		self.table.heading("#10",text="MEDICO")		
		self.table.column("#10",width=150,anchor="center")
		self.table.heading("#11",text="CONT.")	
		self.table.column("#11",width=150,anchor="center")
		self.table.heading("#12",text="FUA")
		self.table.column("#12",width=150,anchor="center")
		self.table.heading("#13",text="HCL")	
		self.table.column("#13",width=150,anchor="center")			
		self.table.place(x=10,y=70,width=1200,height=550)
		self.llenar_Table(fecha,consultorio_get,turno_Name)
		vsb=ttk.Scrollbar(self.Windows_Reporte,orient='horizontal',command=self.table.xview)
		vsb.place(x=10, y=600, width=1200)
		self.table.configure(xscrollcommand=vsb.set)
		#imprimir el reporte
		Label_Imprimir=Label(self.Windows_Reporte,text='imprimir',fg='blue',cursor='hand2')
		Label_Imprimir.bind('<Button-1>',self.imprimir)
		Label_Imprimir.place(x=0,y=620)

		Label_visualizar=Label(self.Windows_Reporte,text='Visualizar',fg='blue',cursor='hand2')
		Label_visualizar.bind('<Button-1>',self.top_ConsultaGeneral)
		Label_visualizar.place(x=60,y=620)
		self.Windows_Reporte.focus()
		self.Windows_Reporte.grab_set()
		self.Windows_Reporte.mainloop()
	def llenar_Table(self,fecha,consultorio,turno):
		if not consultorio=='TODOS':
			rows=self.obj_ConsultaTriaje.consulta_Triaje(fecha,consultorio,turno)
		else:
			rows=self.obj_ConsultaTriaje.consulta_TriajeConsultorios(fecha)

		#valor=[]
		for valores in rows:			
			Data_PacienteBDT=self.obj_ConsultaTriaje.consulta_DatosPaciente(valores.dni)
			Data_PacienteBDG=self.obj_ConsultaGalen.query_DatosPaciente(valores.dni)
			control=True			
			#if len(Data_PacienteBDT)!=0 and control:
			#	for triaje in Data_PacienteBDT:
			#		self.table.insert('','end',values=(valores.dni,triaje.Nombre,triaje.Apellido_Paterno+' '+triaje.Apellido_Materno,valores.Telefono,triaje.Procedencia,valores.Nro_Cupo,valores.Nro_Referencia,valores.P_C,valores.Especialidad,valores.Medico,valores.Continuador,valores.FUA,valores.Historia))
			#		control=False
			#elif len(Data_PacienteBDG)!=0 and control:
			#	for galen in Data_PacienteBDG:
			#		self.table.insert('','end',values=(valores.dni,str(galen.PrimerNombre)+' '+str(galen.SegundoNombre),str(galen.ApellidoPaterno)+' '+str(galen.ApellidoMaterno),valores.Telefono,'desconocido',valores.Nro_Cupo,valores.Nro_Referencia,valores.P_C,valores.Especialidad,valores.Medico,valores.Continuador,valores.FUA,valores.Historia))
			#		control=False
			
			if len(Data_PacienteBDG)!=0 and control:
				for galen in Data_PacienteBDG:
					self.table.insert('','end',values=(valores.dni,str(galen.PrimerNombre)+' '+str(galen.SegundoNombre),str(galen.ApellidoPaterno)+' '+str(galen.ApellidoMaterno),valores.Telefono,'desconocido',valores.Nro_Cupo,valores.Nro_Referencia,valores.P_C,valores.Especialidad,valores.Medico,valores.Continuador,valores.FUA,valores.Historia))
					control=False
			elif len(Data_PacienteBDT)!=0 and control:
				for triaje in Data_PacienteBDT:
					self.table.insert('','end',values=(valores.dni,triaje.Nombre,triaje.Apellido_Paterno+' '+triaje.Apellido_Materno,valores.Telefono,triaje.Procedencia,valores.Nro_Cupo,valores.Nro_Referencia,valores.P_C,valores.Especialidad,valores.Medico,valores.Continuador,valores.FUA,valores.Historia))
					control=False	

	def imprimir(self,event):		
		data=self.current_var.get()
		turno=data[:data.find('-')]
		idmedico=data[data.find('-')+1:data.find('_')]
		consultorio=data[data.find('_')+1:]	
		fecha=self.calendario.selection_get()
		rows=self.obj_ConsultaGalen.consulta_Medico_Responsable(consultorio,fecha,idmedico,turno)
		medico=''
		for val in rows:
			medico=str(val.Nombres)+' '+str(val.ApellidoPaterno)+' '+str(val.ApellidoMaterno)

		if len(consultorio)!=0:		
			self.obj_Impresion.Reporte_Consultorio(self.table,consultorio,medico,fecha,turno)
			os.startfile('consultorio.pdf','print')
			self.Windows_Reporte.destroy()
		else:
			messagebox.showerror('Alerta','Seleccione Consultorio')
	def visualizar_Reporte(self):
		data=self.current_var.get()
		turno=data[:data.find('-')]
		idmedico=data[data.find('-')+1:data.find('_')]
		consultorio=data[data.find('_')+1:]		

		fecha=self.calendario.selection_get()
		rows=self.obj_ConsultaGalen.consulta_Medico_Responsable(consultorio,fecha,idmedico,turno)
		medico=''
		for val in rows:
			medico=str(val.Nombres)+' '+str(val.ApellidoPaterno)+' '+str(val.ApellidoMaterno)

		if len(consultorio)!=0:		
			self.obj_Impresion.Reporte_Consultorio(self.table,consultorio,medico,fecha,turno)			
			self.Windows_Reporte.destroy()
		else:
			messagebox.showerror('Alerta','Seleccione Consultorio')
	def borrado_widget(self):
		self.Entry_Dni.delete(0,'end')
		self.Entry_Nombre.delete(0,'end')
		self.Entry_apellidoP.delete(0,'end')
		self.Entry_apellidoM.delete(0,'end')		
		self.Entry_Telefono.delete(0,'end')
		self.Entry_Procedencia.delete(0,'end')

	def top_ConsultaCupo(self):
		self.ventana_cupo=Toplevel()
		self.ventana_cupo.geometry('325x600')
		self.ventana_cupo.resizable(0,0)
		self.ventana_cupo.grab_set()		
		self.ventana_cupo.title('Consulta Cupo')
		self.ventana_cupo.iconbitmap('img/pdf.ico')
		v = DocViewer(self.ventana_cupo)
		v.pack(side = "top", expand = 1, fill = "both")
		# Display some document
		v.display_file("cupo.pdf")

	def top_ConsultaGeneral(self,event):
		self.visualizar_Reporte()
		self.ventana_General=Toplevel()
		self.ventana_General.geometry('900x750')
		#self.ventana_General.resizable(0,0)
		self.ventana_General.grab_set()		
		self.ventana_General.title('Visualizar Reporte')
		v = DocViewer(self.ventana_General)
		v.pack(side = "top", expand = 1, fill = "both")
		# Display some document
		v.display_file("consultorio.pdf")