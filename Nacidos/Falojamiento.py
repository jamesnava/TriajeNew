from tkinter import *
from tkinter import ttk,messagebox
from Consulta_Galen import queryGalen
from tkcalendar import DateEntry
from Nacidos.consultaN import Consulta
from Util import util
from datetime import datetime

class CAlojamiento(object):
	
	def __init__(self,usuario,tabla):
		self.usuario=usuario
		self.dni=None
		self.historia=None
		self.tabla=tabla
	def TopIngresoAlojamiento(self):
		TopIngreso=Toplevel()
		TopIngreso.geometry("600x400")
		TopIngreso.title("Ingresar Datos")
		TopIngreso.grab_set()
		TopIngreso.resizable(0,0)

		datosmadre=LabelFrame(TopIngreso,text="Datos de la Madre")
		datosmadre.grid(row=1,column=0,columnspan=4)

		label=Label(datosmadre,text="DNI")
		label.grid(row=1,column=1)
		entry_dni=ttk.Entry(datosmadre)
		entry_dni.grid(row=1,column=2,pady=10)
		entry_dni.bind("<Return>",lambda event:self.fillMadre(event,entry_dni,self.entry_Nombres))

		self.entry_Nombres=ttk.Entry(datosmadre,width=30,state="readonly")
		self.entry_Nombres.grid(row=1,column=3,padx=10,pady=10,columnspan=2)

		label=Label(datosmadre,text="Nro. Celular: ")
		label.grid(row=2,column=1)
		entry_TelefonoMadre=ttk.Entry(datosmadre)
		entry_TelefonoMadre.grid(row=2,column=2,pady=10)

		label=Label(datosmadre,text="EE.SS Origen: ")
		label.grid(row=2,column=3,padx=10)
		entry_EstaOrigen=ttk.Entry(datosmadre)
		entry_EstaOrigen.grid(row=2,column=4,pady=10)		

		datosRN=LabelFrame(TopIngreso,text="Datos RN")
		datosRN.grid(row=2,column=0,columnspan=4)

		label=Label(datosRN,text="Historia")
		label.grid(row=1,column=1)
		entry_hclrn=ttk.Entry(datosRN)
		entry_hclrn.grid(row=1,column=2,pady=10)
		entry_hclrn.bind("<Return>",lambda event:self.searchAIRN(event,entry_hclrn,self.entry_NombresRN))

		self.entry_NombresRN=ttk.Entry(datosRN,width=30,state="readonly")
		self.entry_NombresRN.grid(row=1,column=3,padx=10,pady=10,columnspan=2)

		label=Label(datosRN,text="CNV: ")
		label.grid(row=2,column=1)
		entry_Cnv=ttk.Entry(datosRN)
		entry_Cnv.grid(row=2,column=2,pady=10)		

				

		btnAceptar=Button(TopIngreso,text="Aceptar")
		btnAceptar.grid(row=6,column=1,pady=10)
		btnAceptar['command']=lambda:self.InsertarDatos(entry_dni,entry_TelefonoMadre,entry_EstaOrigen,entry_hclrn,entry_Cnv,TopIngreso)

		btnCancelar=Button(TopIngreso,text="Cancelar")
		btnCancelar.configure(command=TopIngreso.destroy)
		btnCancelar.grid(row=6,column=2,padx=5,pady=10)


	def fillMadre(self,event,dnimadre,nombresmadre):		
		dni=dnimadre.get()
		obj_Paciente=queryGalen()
		row=obj_Paciente.query_Paciente(dni)		
		if len(row):
			self.dni=dni			
			nombresmadre['state']='normal'
			nombresmadre.delete(0,"end")
			nombresmadre.insert("end",row[0].PrimerNombre+" "+row[0].ApellidoPaterno+" "+row[0].ApellidoMaterno)
			nombresmadre.configure(state='readonly')
		else:
			
			nombresmadre['state']='normal'
			nombresmadre.delete(0,"end")
			nombresmadre['state']='readonly'

	def searchAIRN(self,event,entryhcl,entrynombres):
		hc=entryhcl.get()
		objGalen=queryGalen()
		rows=objGalen.query_PacienteXHCL(hc)
		if len(rows)>0:
			self.historia=hc
			entrynombres['state']='normal'
			entrynombres.delete(0,'end')
			entrynombres.insert('end',rows[0].PrimerNombre+" "+rows[0].ApellidoPaterno+" "+rows[0].ApellidoMaterno)
			entrynombres.configure(state='readonly')			
		else:
			messagebox.showerror("Error","Datos no encontrados!!")
			entryhcl.delete(0,'end')

	def InsertarDatos(self,EdniMadre,ETelefonoMadre,EstaOrigen,hclrn,Cnv,ventana):
		dniM=EdniMadre.get()
		Telefono=ETelefonoMadre.get()
		EOrigen=EstaOrigen.get()
		hcl=hclrn.get()
		cnv=Cnv.get()


		obj_Triaje=Consulta()
		#insertando Madre
		nro=0
		IdM=obj_Triaje.get_id('MADRE','IDMADRE')
		nro=1 if IdM[0].ID==None else IdM[0].ID+1

		self.entry_Nombres.configure(state='normal')
		self.entry_NombresRN.configure(state='normal')
		campos={"Dni Madre":self.entry_Nombres.get(),"HCL RN":self.entry_NombresRN.get(),"Establecimiento Origen":EstaOrigen.get()}
		
		if self.dni and self.historia:
			if util.validarCampos(campos):
				
				Cnro=obj_Triaje.insertDataTable("MADRE",('IDMADRE','DNI','OBSERVACION','estadoAIRN','estadoPARTO','usuario','INGRESOALOJAMIENTO'),(nro,self.dni,Telefono,1,1,self.usuario,'1'))
				Cnro=1
				if Cnro:
					IdAir=0
					IdM=obj_Triaje.get_id('AIR','Id_AIR')
					IdAir=1 if IdM[0].ID==None else IdM[0].ID+1
					#id usuario
					rowsUsuario=obj_Triaje.get_idTableSTR("USUARIO",'Usuario',self.usuario,'Id_Usuario')
			
					idusuario=rowsUsuario[0].Id_Usuario

					CAir=obj_Triaje.insertDataTable("AIR",('Id_AIR','HCL','CNV','IdUser','INTERCONSULTA','estadoAlojamiento','estado','IDMADRE'),(IdAir,self.historia,cnv,idusuario,0,0,1,nro))
			
					#ingresando parto
					IdM=obj_Triaje.get_id('PARTO','ID_PARTO')
					idparto=1 if IdM[0].ID==None else IdM[0].ID+1
					CAir=obj_Triaje.insertDataTable("PARTO",('ID_PARTO','PROCEDENCIA','IDMADRE'),(idparto,EOrigen,nro))
					messagebox.showinfo("Note","success!!")
					ventana.destroy()
					self.llenar_TAlojamiento()

				else:
					messagebox.showerror("Error","No se pudo Insertar")
		else:
			messagebox.showerror("Alerta","Datos incorrectos!!")

	def validarDigit(self,event,entry):
		param=""
		param=param+entry.get()
		if not param.isdigit():
			messagebox.showerror("Alerta","Solo se Acepta valores numericos")
			entry.delete(0,"end")

	def llenar_TAlojamiento(self):
		self.borrarTabla(self.tabla)
		obj_Triaje=Consulta()
		objGalen=queryGalen()
		rows=obj_Triaje.ConsultaIngresaAlojamiento()
		#obj_Paciente=queryGalen()
		for val in rows:
			rowG=objGalen.query_Paciente(val.DNI)
			rowsNacido=objGalen.query_PacienteXHCL(val.HCL)						
			self.tabla.insert("","end",values=(val.Id_AIR,val.DNI,rowG[0].PrimerNombre+" "+rowG[0].ApellidoPaterno+" "+rowG[0].ApellidoMaterno,rowsNacido[0].PrimerNombre+" "+rowsNacido[0].ApellidoPaterno+" "+rowsNacido[0].ApellidoMaterno,val.HCL,rowsNacido[0].FechaNacimiento))

	def borrarTabla(self,tabla):		
		for item in tabla.get_children():
			tabla.delete(item)

	def EliminarDataTable(self,tabla):
		if tabla.selection():

			idair=tabla.item(tabla.selection())["values"][0]
			# IDMADRE
			obj_Triaje=Consulta()
			rowsM=obj_Triaje.get_idTable("AIR","Id_AIR",idair,"IDMADRE")
			idmadre=rowsM[0].IDMADRE

			#IDPARTO
			rowsP=obj_Triaje.get_idTable("PARTO","IDMADRE",idmadre,"ID_PARTO")
			idparto=rowsP[0].ID_PARTO
			#se puede eliminar
			rowsC=obj_Triaje.QUERY_MADRE(idmadre)

			if len(rowsC)>0:
				obj_Triaje.deleteTable("AIR",'Id_AIR',idair)
				obj_Triaje.deleteTable("PARTO",'ID_PARTO',idparto)
				obj_Triaje.deleteTable("MADRE",'IDMADRE',idmadre)
				messagebox.showinfo('Alerta','Se eliminó!')
				self.llenar_TAlojamiento()
			else:
				messagebox.showerror("Error","No se puede Eliminar!!")



		else:
			messagebox.showerror("Error","No se pudo Eliminar!!")