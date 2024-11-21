from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from Consulta_Galen import queryGalen
#borrar tabla
def borra_Table(tabla):
	for item in tabla.get_children():
		tabla.delete(item)
		
def llenar_Table(tabla,rows,lista):
	for val in rows:
		valores=tuple(getattr(val,valor) for valor in lista)
		tabla.insert('','end',values=valores)

def get_dataTable(tabla,indice):
	if tabla.selection():
		dato=tabla.item(tabla.selection()[0],option="value")[indice]
		return dato
	else:
		messagebox.showerror("Alerta","Se debe seleccionarse un Item")

def borrar_seleccionado(tabla):
	if tabla.selection():
		itemTable=tabla.selection()[0]
		tabla.delete(itemTable)
	else:
		messagebox.showerror("Error","No se puede quitar, seleccione un  Item!!")

def validarCampos(diccionario):

	for clave,valor in diccionario.items():
		if len(valor)==0:
			messagebox.showerror("Error",f"llenar el campo {clave}")			
			return 0
	return 1

def get_Treeview(tabla,indices):
	rows=[]
	for line in tabla.get_children():
		t=[]
		for i in indices:
			t.append(tabla.item(line)['values'][i])
		rows.append(tuple(t))
	return rows

def llenar_combo(combo,rows,lista):
	valoresCombo=[]
	for valor in rows:
		items=str(getattr(valor,lista[0]))+"_"+getattr(valor,lista[1])
		valoresCombo.append(items)
	combo.configure(values=valoresCombo)

def validar_Campo(check,campo):		
	if check.get():
		campo.configure(state="normal")
	else:
		campo.configure(state="disabled")

def validaEntry(check,rpm):
	if check.get():
		rpm.configure(state='disabled')
	else:
		rpm.configure(state='normal')
		rpm.delete(0,"end")

def validarEntero(event,campo):
	dato=campo.get()

	try:
		int(dato)
		
	except Exception as e:
		messagebox.showerror("Alerta","Solo valores Numericos")
		campo.delete(0,"end")

def itemTable_SelectedCIE(event,tablaorigen,tabladestino,toplevel):
	if len(tablaorigen.focus())!=0:
		codigo=tablaorigen.item(tablaorigen.selection()[0],option='values')[0]
		descripcion=tablaorigen.item(tablaorigen.selection()[0],option='values')[1]
		valorbool=False
		for item in tabladestino.get_children():
			if tabladestino.item(item,'values')[0]==codigo:
				valorbool=True
		if not valorbool:
			tabladestino.insert('',"end",values=(codigo,descripcion))	
			toplevel.destroy()
		else:
			messagebox.showerror("Alerta","El diagnostico ya Existe!!")	

def Top_searchPersonal(event,campo):
	TopGeneral=Toplevel()
	TopGeneral.title('Datos Personales')
	TopGeneral.iconbitmap('img/centro.ico')
	TopGeneral.geometry("550x350+350+50")
	TopGeneral.focus_set()	
	TopGeneral.grab_set()
	TopGeneral.resizable(0,0)	

	label_title=Label(TopGeneral,text='Buscar')
	label_title.place(x=20,y=20)
	Entry_buscar_General=ttk.Entry(TopGeneral,width=30)
	Entry_buscar_General.focus()
	Entry_buscar_General.place(x=80,y=20)
	Entry_buscar_General.bind('<Key>',lambda event:buscar_DatosPersonales(event,table_General,Entry_buscar_General))		

	#tabla...
	table_General=ttk.Treeview(TopGeneral,columns=('#1','#2'),show='headings')		
	table_General.heading("#1",text="DNI")
	table_General.column("#1",width=100,anchor="center")
	table_General.heading("#2",text="Nombres")
	table_General.column("#2",width=400,anchor="center")										
	table_General.place(x=10,y=70)
	table_General.bind('<<TreeviewSelect>>',lambda event:itemTable_selected(event,table_General,campo,TopGeneral))			
	#botones de accion
	btn_TPG_Close=ttk.Button(TopGeneral,text='Cerrar')
	btn_TPG_Close.place(x=280,y=365)
	btn_TPG_Close['command']=lambda :TopGeneral.destroy()

def buscar_DatosPersonales(event,tabla,campo):
	obj_Galen=queryGalen()
	parametro=''
	borra_Table(tabla)
	if len(campo.get())!=0:
		parametro=parametro+campo.get()
		rows=obj_Galen.query_Empleado(parametro)
		for valores in rows:
			tabla.insert('','end',values=(valores.DNI,valores.Nombres+" "+valores.ApellidoPaterno+" "+valores.ApellidoMaterno))


def itemTable_selected(event,table_General,campo,ventana):
	if len(table_General.focus())!=0:						
		campo['state']="normal"
		campo.delete(0,'end')
		campo.insert('end',table_General.item(table_General.selection()[0],option='values')[0])
		campo['state']="readonly"	
		ventana.destroy()

def EventMenu(event,table,menu):
	item=table.identify_row(event.y)
	table.selection_set(item)
	menu.post(event.x_root,event.y_root)