from tkinter import *
from tkinter import ttk,messagebox
from Neonatologia.consultaNeonatologia import Consulta
from Util import util
from Consulta_Galen import queryGalen

class Vista(object):
	def __init__(self):
		self.obj_ConsultaNeo=Consulta()
		self.obj_galen=queryGalen()
	def TopDetalle(self,table):
		letra=("Helvetica", "14", "bold italic")
		Resul=("Times", "10", "bold italic")
		if table.selection():
			toplevel=Toplevel()
			toplevel.geometry("600x450")
			toplevel.title("Detalle del paciente")
			toplevel.resizable(0,0)
			toplevel.grab_set()
			label=Label(toplevel,text='Datos',font=letra)
			label.grid(row=0,column=0)
			self.labelRN=Label(toplevel,text='.',font=Resul)
			self.labelRN.grid(row=0,column=1)

			label=Label(toplevel,text="Medico",font=letra)
			label.grid(row=1,column=0,padx=10,pady=10)

			self.labelMedico=Label(toplevel,text='.',font=Resul)
			self.labelMedico.grid(row=1,column=1)

			label=Label(toplevel,text="Transferido desde: ",font=letra)
			label.grid(row=2,column=0,pady=10)
			self.labelServicio=Label(toplevel,text='.',font=Resul)
			self.labelServicio.grid(row=2,column=1)

			self.table_DX=ttk.Treeview(toplevel,columns=('#1','#2'),show='headings')
			self.table_DX.heading("#1",text="DNI MADRE")
			self.table_DX.column("#1",width=80,anchor="w",stretch='NO')
			self.table_DX.heading("#2",text="DATOS MADRE")
			self.table_DX.column("#2",width=250,anchor="w",stretch='NO')								
			self.table_DX.grid(row=3,column=0,padx=10,pady=10,columnspan=2)
			self.llenarWidget(table)

		else:
			messagebox.showerror('Error','Seleccione un Item!')

	def llenarWidget(self,tabla):
		iddata=util.get_dataTable(tabla,4)
		rows=self.obj_ConsultaNeo.get_codigo('DATOS_INGRESO','Id_DATOSINGRESO',iddata)
		#datos para la consulta
		idRnNeo=rows[0].ID_INGRESO
		idAsociado=rows[0].Id_Asociado
		dniMedico=rows[0].M_RESPONSABLE
		#consulta rn
		rowsRnNeo=self.obj_ConsultaNeo.get_codigo('RNNEO','ID_INGRESO',idRnNeo)
		#Obteniendo datos
		HC=rowsRnNeo[0].HC
		idMadre=rowsRnNeo[0].IDMADRE

		#CONSULTAMOS DATOS DEL RN
		rowsRNData=self.obj_galen.query_PacienteXHCL(HC)
		self.labelRN.configure(text=rowsRNData[0].PrimerNombre+" "+rowsRNData[0].ApellidoPaterno+" "+rowsRNData[0].ApellidoMaterno)

		#CONSULTAMOS DATOS DEL MEDICO
		rowsMedico=self.obj_galen.query_EmpleadoDNI(dniMedico)
		self.labelMedico.configure(text=rowsMedico[0].Nombres+" "+rowsMedico[0].ApellidoPaterno+" "+rowsMedico[0].ApellidoMaterno)
		
		#SERVICIO
		if not idAsociado==0:
			rowsDatos=self.obj_ConsultaNeo.get_codigo('DATOS_INGRESO','Id_DATOSINGRESO',idAsociado)
			#Obtengo datos
			IdDestino=rowsDatos[0].ID_DESTINO
			rowsDestinos=self.obj_ConsultaNeo.get_codigo('DESTINO','ID_DESTINO',IdDestino)
			self.labelServicio.configure(text=rowsDestinos[0].NOMBRE_DESTINO)

		#obteniendo los diagnosticos
		rowsdx=self.obj_ConsultaNeo.get_codigo('DXNEO','Id_DATOSINGRESO',iddata)
		util.llenar_Table(self.table_DX,rowsdx,['CODCIE','DESCRIPCION'])




		
		