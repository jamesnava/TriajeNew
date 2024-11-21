from tkinter import *
from tkinter import ttk,messagebox
from Nacidos.consultaN import Consulta
from tktimepicker import SpinTimePickerModern, SpinTimePickerOld
from tktimepicker import constants
from Util import util
from Consulta_Triaje import queryTriaje

class Rn(object):
	def __init__(self):
		self.obj_consultaN=Consulta()
	def UpdateDataRN(self,Id_AIR):
		self.TopAIRN=Toplevel()
		self.TopAIRN.geometry("1000x600")
		self.TopAIRN.resizable(0,0)
		self.TopAIRN.title("Modificar Datos")
		self.TopAIRN.configure(bg="#273C6A")
		self.TopAIRN.grab_set()

		label=Label(self.TopAIRN,text="HCL: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=1,column=1,pady=10)
		self.AEntry_HCL=ttk.Entry(self.TopAIRN,width=20)
		self.AEntry_HCL.grid(row=1,column=2,pady=10)		

		label=Label(self.TopAIRN,text="CNV: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=2,column=1,pady=10)
		self.AEntry_CNV=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_CNV.grid(row=2,column=2,pady=10)

		label=Label(self.TopAIRN,text="Pinzam(min): ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=2,column=3,pady=10)
		self.AEntry_PINZAMIENTO=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_PINZAMIENTO.grid(row=2,column=4,pady=10)	
			
		
		label=Label(self.TopAIRN,text="LME(hh:mm): ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=2,column=5,pady=10)
		self.AEntry_LME=ttk.Entry(self.TopAIRN,width=15)	
		self.AEntry_LME.grid(row=2,column=6,pady=10)

		label=Label(self.TopAIRN,text="PA : ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=2,column=7,pady=10)
		self.AEntry_PA=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_PA.grid(row=2,column=8,pady=10)
		
		

		label=Label(self.TopAIRN,text="PESO(grs): ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=3,column=1,pady=10)
		self.AEntry_PESO=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_PESO.grid(row=3,column=2,pady=10)
		

		label=Label(self.TopAIRN,text="TALLA(cm): ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=3,column=3,pady=10)
		self.AEntry_TALLA=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_TALLA.grid(row=3,column=4,pady=10)
		

		label=Label(self.TopAIRN,text="PC : ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=3,column=5,pady=10)
		self.AEntry_PC=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_PC.grid(row=3,column=6,pady=10)
		

		label=Label(self.TopAIRN,text="PT : ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=3,column=7,pady=10)
		self.AEntry_PT=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_PT.grid(row=3,column=8,pady=10)
		

		
		label=Label(self.TopAIRN,text="PB: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=4,column=1,pady=10)
		self.AEntry_PB=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_PB.grid(row=4,column=2,pady=10)
		

		label=Label(self.TopAIRN,text="EXFI: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=4,column=3,pady=10)
		self.AEntry_EXFI=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_EXFI.grid(row=4,column=4,pady=10)		


		label=Label(self.TopAIRN,text="FUR: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=4,column=5,pady=10)
		self.AEntry_FUR=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_FUR.grid(row=4,column=6,pady=10)
		

		label=Label(self.TopAIRN,text="APGAR 1 : ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=4,column=7,pady=10)
		self.AEntry_APGAR1=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_APGAR1.grid(row=4,column=8,pady=10)
		

		label=Label(self.TopAIRN,text="APGAR 5 : ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=5,column=1,pady=10)
		self.AEntry_APGAR5=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_APGAR5.grid(row=5,column=2,pady=10)
	

		label=Label(self.TopAIRN,text="APGAR 10: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=5,column=3,pady=10)
		self.AEntry_APGAR10=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_APGAR10.grid(row=5,column=4,pady=10)
		

		label=Label(self.TopAIRN,text="TEMPERATURA: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=5,column=5,pady=10)
		self.AEntry_TEMPERATURA=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_TEMPERATURA.grid(row=5,column=6,pady=10)								

		label=Label(self.TopAIRN,text="COLOR AMNIOTICO: ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=6,column=3,pady=10)
		self.AEntry_AMNIOTICO=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_AMNIOTICO.grid(row=6,column=4,pady=10)

		label=Label(self.TopAIRN,text="T. KRISTELLER(min): ",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=6,column=5,pady=10)
		self.AEntry_KRISTELLER=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_KRISTELLER.grid(row=6,column=6,pady=10)
		

		label=Label(self.TopAIRN,text="Hora E.",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=5,column=7,pady=10)
		self.time_EgresoAIRN=SpinTimePickerModern(self.TopAIRN)
		self.time_EgresoAIRN.addAll(constants.HOURS24)		
		self.time_EgresoAIRN.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
		self.time_EgresoAIRN.configure_separator(bg="#404040",fg="#fff")
		self.time_EgresoAIRN.grid(row=5,column=8,pady=10)
			

		label=Label(self.TopAIRN,text="GRUPO FACTOR:",font=('Arial',10,'bold'),bg="#273C6A",fg="#fff")
		label.grid(row=6,column=1,pady=10)
		self.AEntry_GRUPOF=ttk.Entry(self.TopAIRN,width=15)
		self.AEntry_GRUPOF.grid(row=6,column=2,pady=10)
		self.fillWidget(Id_AIR)	
	

		style = ttk.Style()
		style.configure("btnAdd.TButton",background="#9A4419",font=("Helvetica", 12))

		self.ButtonAddCIE=ttk.Button(self.TopAIRN,text="Agregar DX",style="btnAdd.TButton",cursor="hand2")
		self.ButtonAddCIE.grid(row=8,column=3,pady=10)
		self.ButtonAddCIE['command']=self.Top_searchCie
			
		style = ttk.Style()
		style.configure("btnClose.TButton",background="red",font=("Helvetica", 12))
		self.ButtonEliminaCIE=ttk.Button(self.TopAIRN,text="Quitar Dx",style="btnClose.TButton",cursor="hand2")
		self.ButtonEliminaCIE.grid(row=8,column=5,pady=10)
		self.ButtonEliminaCIE['command']=lambda :self.eliminarSeleccionTable(self.table_DX)

		self.table_DX=ttk.Treeview(self.TopAIRN,columns=('#1','#2'),show='headings',height=5)
		self.table_DX.heading("#1",text="CODIGO CIE")
		self.table_DX.column("#1",width=100,anchor="w",stretch='NO')
		self.table_DX.heading("#2",text="DESCRIPCION")
		self.table_DX.column("#2",width=400,anchor="w",stretch='NO')								
		self.table_DX.grid(row=9,column=1,padx=10,pady=2,columnspan=20)
		
		rowsDX=	self.obj_consultaN.consulta_datosAirDX(Id_AIR)
		util.llenar_Table(self.table_DX,rowsDX,["CODCIE","NOMBRE"])	

		ButtonAddAIRN=ttk.Button(self.TopAIRN,text="Aceptar",cursor="hand2")
		ButtonAddAIRN.grid(row=10,column=4,pady=10)
		ButtonAddAIRN['command']=lambda:self.UpdateAIR(Id_AIR)
			
		ButtonCloseAIRN=ttk.Button(self.TopAIRN,text="Cerrar",cursor="hand2")
		ButtonCloseAIRN.grid(row=10,column=5,pady=10)
		ButtonCloseAIRN['command']=self.TopAIRN.destroy

	def eliminarSeleccionTable(self,table):
		seleccion=self.table_DX.focus()
		if seleccion:
			self.table_DX.delete(seleccion)

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
		self.table_CIE.bind('<<TreeviewSelect>>',self.itemTable_SelectedCIE)

	def itemTable_SelectedCIE(self,event):
		if len(self.table_CIE.focus())!=0:
			codigo=self.table_CIE.item(self.table_CIE.selection()[0],option='values')[0]
			descripcion=self.table_CIE.item(self.table_CIE.selection()[0],option='values')[1]
			valorbool=False
			for item in self.table_DX.get_children():
				if self.table_DX.item(item,'values')[0]==codigo:
					valorbool=True
			if not valorbool:
				self.table_DX.insert('',"end",values=(codigo,descripcion))	
				self.TopCIE.destroy()
			else:
				messagebox.showerror("Alerta","El diagnostico ya Existe!!")	

	def buscar_cie(self,event):		
		self.borrarTabla(self.table_CIE)
		parametro=''		
		if len(self.Entry_buscar_General.get())!=0:			
			parametro=parametro+self.Entry_buscar_General.get()
			obj_query=queryTriaje()
			rows=obj_query.query_cie10(parametro)			
			for valores in rows:
				self.table_CIE.insert('','end',values=(valores.CODCIE,valores.NOMBRE))
				
	def borrarTabla(self,tabla):		
		for item in tabla.get_children():
			tabla.delete(item)

	def fillWidget(self,idair):
		
		rows=self.obj_consultaN.consulta_Tabla1("AIR","Id_AIR",idair)

		for val in rows:
			self.AEntry_HCL.insert("end",val.HCL)
			self.AEntry_HCL.configure(state="readonly")			
			self.AEntry_CNV.insert("end",val.CNV)
			self.AEntry_PINZAMIENTO.insert("end",val.T_PINZA)
			self.AEntry_LME.insert("end",str(val.INI_LME))
			self.AEntry_PA.insert("end",val.PA)
			self.AEntry_PESO.insert("end",val.PESO)
			self.AEntry_TALLA.insert("end",val.TALLA)
			self.AEntry_PC.insert("end",val.PC)
			self.AEntry_PT.insert("end",val.PT)
			self.AEntry_PB.insert("end",val.PB)
			self.AEntry_EXFI.insert("end",val.EX_FI)
			self.AEntry_FUR.insert("end",val.FUR)
			self.AEntry_APGAR1.insert("end",val.APGAR_1)
			self.AEntry_APGAR5.insert("end",val.APGAR_5)
			Apgar10=val.APGAR_10 if not val.APGAR_10==-1 else "" 
			self.AEntry_APGAR10.insert("end",Apgar10)
			self.AEntry_TEMPERATURA.insert("end",val.TEMPERATURA)
			self.AEntry_AMNIOTICO.insert("end",val.L_AMNIOTICO)
			self.AEntry_KRISTELLER.insert("end",val.KRISTELLER)
			self.AEntry_GRUPOF.insert("end",val.GRUPO_FACTOR)
			self.time_EgresoAIRN.set24Hrs(val.H_EGRESO_AIRN[:val.H_EGRESO_AIRN.find(":")])
			self.time_EgresoAIRN.setMins(val.H_EGRESO_AIRN[val.H_EGRESO_AIRN.find(":")+1:])
	def UpdateAIR(self,idair):				
		cnv=self.AEntry_CNV.get()
		pinzamiento=self.AEntry_PINZAMIENTO.get()
		lme=self.AEntry_LME.get()
		pa=self.AEntry_PA.get()
		peso=self.AEntry_PESO.get()
		talla=self.AEntry_TALLA.get()
		pc=self.AEntry_PC.get()
		pt=self.AEntry_PT.get()
		pb=self.AEntry_PB.get()
		exfi=self.AEntry_EXFI.get()
		fur=self.AEntry_FUR.get()
		apgar1=self.AEntry_APGAR1.get()
		apgar5=self.AEntry_APGAR5.get()		
		apgar10=self.AEntry_APGAR10.get() if len(self.AEntry_APGAR10.get())>0 else -1
		temperatura=self.AEntry_TEMPERATURA.get()
		amniotico=self.AEntry_AMNIOTICO.get()
		kriss=self.AEntry_KRISTELLER.get()
		grupof=self.AEntry_GRUPOF.get()
		horaEAIRN="{}:{}".format(*self.time_EgresoAIRN.time())
		datos={"CNV":f"""'{cnv}'""","T_PINZA":f"""'{pinzamiento}'""","INI_LME":f"""'{lme}'""","PA":pa,"PESO":peso
		,"TALLA":talla,"PC":pc,"PT":pt,"PB":pb,"EX_FI":exfi,"FUR":fur,"APGAR_1":apgar1,"APGAR_5":apgar5,'APGAR_10':apgar10,
		"TEMPERATURA":temperatura,"L_AMNIOTICO":f"""'{amniotico}'""","KRISTELLER":f"""'{kriss}'""","GRUPO_FACTOR":f"""'{grupof}'""",
		"H_EGRESO_AIRN":f"""'{horaEAIRN}'"""}

		
		listaDX=util.get_Treeview(self.table_DX,[0,1])
		diagnosticos=[]
		for t in listaDX:
			t1=(t[0],idair)
			diagnosticos.append(t1)
		
		self.obj_consultaN.deleteTable("DXAIRN","Id_AIR",idair)
		for valores in diagnosticos:
			self.obj_consultaN.insertDataTable("DXAIRN",('CODCIE','Id_AIR'),valores)
		nro=self.obj_consultaN.Update_DataTables("AIR",datos,"Id_AIR",idair)

		if nro:
			messagebox.showinfo("Notificación","Se actualizó correctamente")
			self.TopAIRN.destroy()
		else:
			messagebox.showerror("Error","No pudo actualizar")

			
