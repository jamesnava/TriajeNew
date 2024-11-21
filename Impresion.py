from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import Consulta_Triaje
import Consulta_Galen

class Reporte(object):
	def __init__(self):
		self.obj_Triaje=Consulta_Triaje.queryTriaje()
		self.obj_Galen=Consulta_Galen.queryGalen()
		pdfmetrics.registerFont(TTFont('Vera','Vera.ttf'))		
	def Reporte_Consultorio(self,table,consultorio,medico,fecha,turno):
		libro=canvas.Canvas('consultorio.pdf',landscape(letter))
		w,h=landscape(letter)		
		libro.drawString(20,h-20,f'REPORTE DE CONSULTORIO EXTERNO {consultorio}')
		libro.drawString(20,h-35,f'MEDICO RESPONSABLE: {medico}')
		libro.drawString(20,h-50,f'FECHA: {fecha}')
		nombre_turn=''
		if int(turno)==4:
			nombre_turn='Mañana'
		elif int(turno)==33:
			nombre_turn='Tarde'
		elif int(turno)==1:
			nombre_turn='Mañana y Tarde'

		libro.drawString(400,h-50,f'TURNO: {nombre_turn}')		
		ylist=[]		
		xlist=[10,60,140,270,320,370,435,505,525,550,590,680,780]			

		alto_Celda=70
		for i in range(len(table.get_children())+2):
			ylist.append(h-alto_Celda)
			alto_Celda+=15
		libro.setFont('Times-Roman',10)
		libro.drawString(5,h-82,'DNI')
		libro.drawString(55,h-82,'NOMBRES')
		libro.drawString(135,h-82,'APELLIDOS')
		libro.drawString(260,h-82,'TELEF.')
		libro.drawString(312,h-82,'CUPO')
		libro.drawString(365,h-82,'NRO REF.')
		libro.drawString(427,h-82,'ESTABLECIM.')
		#libro.drawString(495,h-82,'CT.')
		libro.drawString(516,h-82,'FUA')
		libro.drawString(542,h-82,'HIST.')
		libro.drawString(581,h-82,'CONSULT.')
		libro.drawString(671,h-82,'MEDICO')
		lista_Datos=[]

		for i in table.get_children():
			#print(table.item(i)['values'][0])
			#lista_Datos.append(table.item(i)['values'])
			lista_Datos.append(table.item(i,"values"))

		letra_distancia=95
		cantidad=len(lista_Datos)
		libro.setFont('Times-Roman',9)
		contador=0
		for i in range(cantidad):						
			libro.drawString(5,h-letra_distancia,f"""{lista_Datos[i][0]}""")
			libro.drawString(57,h-letra_distancia,f'{lista_Datos[i][1][:lista_Datos[i][1].find(" ")]}')
			libro.drawString(133,h-letra_distancia,f'{lista_Datos[i][2]}')
			libro.drawString(260,h-letra_distancia,f'{lista_Datos[i][3]}')
			libro.drawString(315,h-letra_distancia,f'{lista_Datos[i][5]}')
			libro.drawString(365,h-letra_distancia,f'{lista_Datos[i][6]}')
			libro.drawString(424,h-letra_distancia,f'{lista_Datos[i][7]}')
			#libro.drawString(492,h-letra_distancia,f'{lista_Datos[i][10]}')
			libro.drawString(515,h-letra_distancia,f'{lista_Datos[i][11]}')
			libro.drawString(538,h-letra_distancia,f'{lista_Datos[i][12]}')
			
			if len(lista_Datos[i][8])>27:
				libro.drawString(592,h-letra_distancia,f'{lista_Datos[i][8][0:27]}')
			else:
				libro.drawString(592,h-letra_distancia,f'{lista_Datos[i][8]}')
			if len(lista_Datos[i][9])>22:
				libro.drawString(682,h-letra_distancia,f'{lista_Datos[i][9][0:22]}')
			else:
				libro.drawString(682,h-letra_distancia,f'{lista_Datos[i][9]}')
			letra_distancia=letra_distancia+15
			if i==25:
				libro.showPage()
				w,h=landscape(letter)
				letra_distancia=95
				libro.setFont('Times-Roman',9)

		
		#libro.grid(xlist,ylist)

		libro.save()
	def imprimir_Cupo(self,dni,id_fuente,cupo,medico,consultorio,nro_Referencia,fecha_A,historia,establecimiento,Turno,usuario,fechaR,estado):
		nomb_apelle=''
		procedencia=''
		rows=self.obj_Triaje.consulta_DatosPaciente(dni)
		if len(rows)!=0:
			for val in rows:
				nomb_apelle=str(val.Nombre)+' '+str(val.Apellido_Paterno)+' '+str(val.Apellido_Materno)
				procedencia=val.Procedencia
		else:
			rows_galen=self.obj_Galen.query_Paciente(dni)
			for val in rows_galen:
				nomb_apelle=str(val.PrimerNombre)+' '+str(val.SegundoNombre)+' '+str(val.ApellidoPaterno)+' '+str(val.ApellidoMaterno)
				procedencia=val.Nombre

		libro=canvas.Canvas('cupo.pdf')
		#7.7
		w,h=3.15*inch,6.0*inch
		libro.setPageSize((w,h))
		libro.drawImage('img/log_HSRA.png',150,260, width=70, preserveAspectRatio=True)
		libro.setFont('Helvetica-Bold',10)
		libro.drawString(40,h-15,'CONSULTA EXTERNA')
		#libro.drawString(40,h-30,'EXTERNA')
		libro.drawString(0,h-30,f'______________________________________')	
		libro.setFont('Helvetica-Bold',10)

		libro.drawString(10,h-45,f'DATOS DEL PACIENTE')
		libro.setFont('Times-Roman',10)
		libro.drawString(10,h-60,f'{nomb_apelle}')
		libro.drawString(10,h-75,f'DNI: {dni}')
		libro.setFont('Helvetica-Bold',10)
		libro.drawString(10,h-90,f'PROCEDENCIA')
		libro.setFont('Times-Roman',10)
		libro.drawString(10,h-105,f'{procedencia}')
		libro.setFont('Helvetica-Bold',10)
		libro.drawString(0,h-115,f'______________________________________')		
		libro.drawString(0,h-130,f'DETALLE DE LA ATENCIÓN')
		libro.drawString(0,h-145,f'______________________________________')
		
		libro.setFont('Helvetica-Bold',10)
		libro.drawString(10,h-160,f'CONSULTORIO')
		libro.setFont('Times-Roman',10)
		libro.drawString(10,h-175,f'{consultorio}')
		libro.setFont('Helvetica-Bold',10)
		libro.drawString(10,h-190,f'MEDICO')
		libro.setFont('Times-Roman',10)
		libro.drawString(10,h-205,f'{medico}')
		libro.setFont('Helvetica-Bold',10)		
		libro.drawString(10,h-220,f'ESTABLECIMIENTO')
		libro.setFont('Times-Roman',10)
		libro.drawString(10,h-235,f'{establecimiento}')
		libro.setFont('Helvetica-Bold',10)		
		libro.drawString(10,h-250,f'FUENTE')
		libro.setFont('Times-Roman',10)
		libro.drawString(10,h-265,f'{id_fuente}')
		libro.setFont('Helvetica-Bold',10)
		libro.drawString(10,h-280,f'NRO REFERENCIA')
		libro.setFont('Times-Roman',10)
		libro.drawString(20,h-295,f'{nro_Referencia}')

		libro.setFont('Helvetica-Bold',10)
		libro.drawString(10,h-310,f'Turno')
		libro.setFont('Times-Roman',10)
		libro.drawString(20,h-325,f'{Turno}')

		libro.setFont('Helvetica-Bold',10)
		libro.drawString(10,h-340,f'NRO CUPO')
		libro.setFont('Times-Roman',10)
		libro.drawString(20,h-355,f'{cupo}')
		libro.setFont('Helvetica-Bold',10)
		libro.drawString(10,h-370,f'Historia Clinica')
		libro.setFont('Times-Roman',10)
		libro.drawString(20,h-385,f'{historia}')
		libro.setFont('Helvetica-Bold',10)
		libro.drawString(10,h-400,f'FECH. ATENCION')
		libro.setFont('Times-Roman',10)
		libro.drawString(20,h-415,f'{fecha_A} ')

		libro.setFont('Helvetica-Bold',10)
		libro.drawString(112,h-400,f'ESTADO')
		libro.setFont('Times-Roman',10)
		libro.drawString(112,h-415,f'{estado} ')

		libro.setFont('Helvetica-Bold',8)
		libro.drawString(10,h-430,f"Registrado por:")
		libro.setFont('Times-Roman',8)
		libro.drawString(75,h-430,f'{usuario}')	

		libro.setFont('Helvetica-Bold',8)
		libro.drawString(112,h-430,f"F.Rg:")
		libro.setFont('Times-Roman',8)
		libro.drawString(140,h-430,f'{fechaR}')
		libro.showPage()
		libro.save()
