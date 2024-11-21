from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import calendar
from datetime import datetime
import locale
from Consulta_Galen import queryGalen

class ProgEspecialidad(object):
	def __init__(self,FrameM,width,height):		
		locale.setlocale(locale.LC_TIME,'es_ES.UTF-8')
		self.ConsultorioP=Frame(FrameM,width=int(width*0.80),height=int(height*0.14),bg='#828682',relief="solid",bd=1)		
		self.ConsultorioP.place(x=0,y=0)
		self.ConsultorioP.grid_propagate(False)
		self.obj_Galen=queryGalen()	

	def Programacion(self,fecha,idservicio):
		fechaDate=datetime.strptime(str(fecha),"%Y-%m-%d").date()
		mes=fechaDate.month
		anio=fechaDate.year
		_,numdays=calendar.monthrange(anio,mes)
		columns=tuple([f'#{i+1}' for i in range(numdays+1)])
			
		self.ConsultorioP.grid_columnconfigure(0, weight=1)
		self.ConsultorioP.grid_rowconfigure(0, weight=1)
		
		self.table_Programacion=ttk.Treeview(self.ConsultorioP,columns=columns,show='headings',height=3)
		for i in range(numdays+2):
			
			if i==1:

				self.table_Programacion.heading(f"#{i}",text=f"Nombres Medicos")
				self.table_Programacion.column(f"#{i}",width=200,anchor="w",stretch='NO')
			elif i>1:
				fechaName=datetime(anio,mes,i-1)
				nombreDia=fechaName.strftime("%A")[0].upper()
				self.table_Programacion.heading(f"#{i}",text=f"{nombreDia}-{i-1}")
				self.table_Programacion.column(f"#{i}",width=50,anchor="w",stretch='NO')
			#numeros.append(i+1)
		#self.table_Programacion.insert("","end",values=tuple(numeros))
		self.LlenarProgramacion(f'{anio}-{mes}-01',f'{anio}-{mes}-{numdays}',idservicio)
		scrollbar = ttk.Scrollbar(self.ConsultorioP, orient="horizontal",command=self.table_Programacion.xview)
		self.table_Programacion.configure(xscrollcommand=scrollbar.set)
		self.table_Programacion.grid(row=0,column=0,sticky='nsew')
		scrollbar.grid(row=1, column=0,sticky='ew')

	def LlenarProgramacion(self,fechaI,fechaF,idservicio):
		rows=self.obj_Galen.queryMedicoEspecialidad(fechaI,fechaF,idservicio)
		aux=[]
		datos=[]
		for val in rows:
			dni=val.DNI.strip()
			nombre_completo=val.Nombres+' '+val.ApellidoPaterno+' '+val.ApellidoMaterno
			if dni not in aux:
				aux.append(dni)
				datos.append([[dni],[nombre_completo]])
		for valores in datos:
			self.table_Programacion.insert("","end",values=(valores[1]))

		

