from Consulta_Triaje import queryTriaje

class operaciones(object):

	def __init__(self):
		self.obj_consultas=queryTriaje()

	def VEstablecimiento(self,dni,ser):
		rows=self.obj_consultas.existencia_pacienteBD(dni)
		Establecimiento,servicio="",""
		#comprobar si el paciente se atendio
		
		if len(rows)>0:			
			rowsAnio=self.obj_consultas.existencia_pacienteBDAnio(dni)
			if len(rowsAnio)>0:
				Establecimiento="C"				
				rowsServicioNow=self.obj_consultas.existencia_pacienteBDServicioAnio(dni,ser)				
				if len(rowsServicioNow)>0:
					servicio="C"
				else:
					rowsNuevo=self.obj_consultas.existencia_pacienteBDServicio(dni,ser)
					if len(rowsNuevo)>0:
						servicio="R"
					else:
						servicio="N"
			else:
				Establecimiento="R"
				rowsServicioAnio=self.obj_consultas.existencia_pacienteBDServicio(dni,ser)
				if len(rowsServicioAnio)>0:
					servicio="R"
				else:
					servicio="N"
		else:
			Establecimiento,servicio="N","N"
		
		return Establecimiento,servicio