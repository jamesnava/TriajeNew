from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import Consulta_Galen
from Estadisticas import ConsultaEstadisticas

class Triaje_Estadisticas(object):
	def __init__(self,width,height,usuario,root,ventana):
		self.width=width
		self.height=height
		self.usuario=usuario
		self.root=root
		self.ventana=ventana
		self.obj_galen=Consulta_Galen.queryGalen()
		self.obj_estadisticas=ConsultaEstadisticas.ConsultaEstadistica()
		
	def FramePrincipal(self):
		Contenedor=Frame(self.root,width=self.width,height=self.height,bg="#828682")
		Contenedor.grid(row=1,column=0)
		Contenedor.pack_propagate(False)

		self.capa1=Frame(Contenedor,width=int(self.width/2),height=int(self.height/2),bg="#828682",highlightthickness=1)
		self.capa1.place(x=0,y=0)
		self.capa1.grid_propagate(False)

		button=Button(self.capa1,text='Generar')

		button.grid(row=1,column=0)
		button.configure(command=self.generador)

		self.capa2=Frame(Contenedor,width=int(self.width/2)-2,height=int(self.height/2),bg="#828682",highlightthickness=1)
		self.capa2.place(x=int(self.width/2)+2,y=0)
		self.capa2.grid_propagate(False)

		self.capa3=Frame(Contenedor,width=int(self.width/2),height=int((self.height/2)*.7),bg="#828682",highlightthickness=1)
		self.capa3.place(x=0,y=int(self.height/2)+2)
		self.capa3.grid_propagate(False)

		self.capa4=Frame(Contenedor,width=int(self.width/2)-2,height=int((self.height/2)*.7),bg="#828682",highlightthickness=1)
		self.capa4.place(x=int(self.width/2)+2,y=int(self.height/2)+2)
		self.capa4.grid_propagate(False)



	def generador(self):
		rows_E=self.obj_estadisticas.consulta_medicos()
		for val in rows_E:
			rows_Galen=self.obj_galen.datos_Medicoss(val.Medico)
			if rows_Galen:
				with open('codigo.txt', 'a') as archivo:				
					archivo.write(f'''UPDATE TRIAJE SET DniMedico='{rows_Galen[0].DNI.strip()}' WHERE Medico='{val.Medico}' ''' + '\n')

	def Frame(self):
		Capa=Frame(self.root,width=self.width,height=self.height,bg="#828682")
		Capa.grid(row=1,column=0)
		Capa.pack_propagate(False)

		self.f = Figure( figsize=(15, 7), dpi=80 )


		self.ax0 = self.f.add_axes( (0.25, .25, .50, .50), frameon=False)       
      
		self.ax0.set_xlabel( 'Y' )
		self.ax0.set_ylabel( 'X' )
		self.ax0.plot([1,4,5,6,7,4,8])

		self.canvas = FigureCanvasTkAgg(self.f, master=Capa)
		self.canvas.get_tk_widget().pack()
		self.canvas.draw()

		self.toolbar = NavigationToolbar2Tk(self.canvas, Capa)
		self.toolbar.pack()
		self.toolbar.update()


		

		
