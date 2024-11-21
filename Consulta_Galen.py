import conect_bd

class queryGalen(object):
	def __init__(self):
		pass
	def query_Programacion(self,fecha):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT S.IdServicio,Nombre,IdMedico,IdTurno FROM ProgramacionMedica AS P  
			INNER JOIN Servicios as S ON P.IdServicio=S.IdServicio  
			AND P.Fecha=CONVERT(date,'{fecha}') ORDER BY Nombre ASC"""						
			cursor.execute(sql)
			rows=cursor.fetchall()			
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows	

	def query_ProgramacionServicios(self,fechaI,fechaF,idEspe):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT S.IdServicio,Nombre,IdMedico,T.Descripcion,CONVERT(date,P.Fecha) AS fecha FROM 
			ProgramacionMedica AS P  INNER JOIN Servicios as S ON P.IdServicio=S.IdServicio INNER JOIN Turnos 
			AS T ON P.IdTurno=T.IdTurno WHERE  P.Fecha BETWEEN CONVERT(date,'{fechaI}') AND CONVERT(date,'{fechaF}') 
			AND S.IdEspecialidad={idEspe}"""
								
			cursor.execute(sql)
			rows=cursor.fetchall()			
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows	
	def queryMedicoEspecialidad(self,fechaI,fechaF,idservicio):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f'''SELECT EMPLE.DNI,EMPLE.Nombres,EMPLE.ApellidoPaterno,EMPLE.ApellidoMaterno,CONVERT(DATE,P.Fecha)AS Fecha,T.Codigo FROM ProgramacionMedica AS P INNER JOIN Servicios AS S ON P.IdServicio=S.IdServicio
			INNER JOIN Medicos AS MED ON P.IdMedico=MED.IdMedico INNER JOIN Empleados AS EMPLE ON MED.IdEmpleado=EMPLE.IdEmpleado INNER JOIN 
			(SELECT DISTINCT IdEspecialidad FROM ProgramacionMedica WHERE IdServicio={idservicio}) AS SubQ ON P.IdEspecialidad=SubQ.IdEspecialidad INNER JOIN Turnos AS T ON P.IdTurno=T.IdTurno
			WHERE  CONVERT(DATE,Fecha) BETWEEN '{fechaI}' AND '{fechaF}' '''
			cursor.execute(sql)
			rows=cursor.fetchall()	
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows


	def query_ProgramacionEspecialidad(self,fechaI,fechaF):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT ESPE.IdEspecialidad,ESPE.Nombre AS especialidad FROM ProgramacionMedica AS P  
			INNER JOIN Servicios as S ON P.IdServicio=S.IdServicio INNER JOIN Especialidades AS ESPE ON S.IdEspecialidad=ESPE.IdEspecialidad  
			WHERE P.Fecha BETWEEN CONVERT(date,'{fechaI}') AND CONVERT(date,'{fechaF}') 
			GROUP BY ESPE.IdEspecialidad, ESPE.Nombre  ORDER BY ESPE.Nombre DESC
			"""						
			cursor.execute(sql)
			rows=cursor.fetchall()			
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows	

	def query_Paciente(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		
		try:
			rows=[]
			sql=f"""SELECT * FROM Pacientes INNER JOIN CentrosPoblados ON Pacientes.IdCentroPobladoDomicilio=CentrosPoblados.IdCentroPoblado WHERE NroDocumento='{dni.strip()}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			cursor.close()
			return rows	
		except Exception as e:
			print(e)
		finally:		
			obj_conectar.close_conection()
				

	def query_PacienteV1(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]		
			sql=f"""SELECT P.NroDocumento,P.PrimerNombre,P.ApellidoPaterno,P.ApellidoMaterno,P.NroHistoriaClinica,CONVERT(DATE,P.FechaNacimiento,102) 
			AS FECHANACIMIENTO,TS.Descripcion,D.Nombre,D.IdDistrito,P.IdEtnia FROM Pacientes AS P INNER JOIN TiposSexo AS TS  ON TS.IdTipoSexo=P.IdTipoSexo INNER JOIN Distritos
			AS D ON P.IdDistritoProcedencia=D.IdDistrito AND P.NroDocumento='{dni}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def consulta_Medico_Responsable(self,servicio,fecha,idmedico,turno):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""
			SELECT E.DNI,E.Nombres,E.ApellidoPaterno,E.ApellidoMaterno,TUR.Descripcion 
			FROM ProgramacionMedica AS P  INNER JOIN Servicios as S ON P.IdServicio=S.IdServicio 
			AND P.Fecha=CONVERT(date,'{fecha}') AND
			S.Nombre='{servicio}' AND P.IdMedico='{idmedico}'
 			INNER JOIN Medicos as M ON  P.IdMedico=M.IdMedico INNER JOIN Empleados AS 
 			E ON M.IdEmpleado=E.IdEmpleado INNER JOIN Turnos as TUR ON P.IdTurno=TUR.IdTurno AND
 			 TUR.IdTurno='{turno}'
			"""						
			cursor.execute(sql)
			rows=cursor.fetchall()	
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def query_Establecimiento(self,digitacion):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT EST.Nombre AS Establecimiento,DIST.Nombre AS Distrito,PROV.Nombre AS Provincia FROM Establecimientos AS EST INNER JOIN Distritos as DIST ON DIST.IdDistrito=EST.IdDistrito
			INNER JOIN Provincias AS PROV ON DIST.IdProvincia=PROV.IdProvincia WHERE EST.Nombre LIKE '%{digitacion}%'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows	


	def query_DatosPaciente(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute(f"""SELECT PrimerNombre,SegundoNombre,ApellidoPaterno,ApellidoMaterno,Telefono FROM Pacientes WHERE NroDocumento='{dni}'""")
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def query_DatosLIKEPaciente(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute(f"""SELECT NroDocumento,PrimerNombre,SegundoNombre,ApellidoPaterno,ApellidoMaterno FROM Pacientes WHERE NroDocumento LIKE '{dni}%'""")
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows		

	def query_financiamiento(self):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute(f"""SELECT Descripcion FROM TiposFinanciamiento WHERE IdTipoFinanciamiento IN (1,2,3)""")
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def query_TipoTurnos(self,id_turno):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute(f"""SELECT * FROM Turnos WHERE IdTurno={id_turno}""")
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def query_EspecialidadesCEXT(self):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			cursor.execute(f"""SELECT DISTINCT ES.Nombre FROM Servicios AS S 
			INNER JOIN TiposServicio AS TS ON S.IdTipoServicio=TS.IdTipoServicio 
			INNER JOIN Especialidades AS ES ON ES.IdEspecialidad=S.IdEspecialidad AND TS.IdTipoServicio=1 ORDER BY ES.Nombre ASC""")
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
	#his

	def query_Atenciones(self,fecha,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT PA.NroDocumento AS DNIPACIENTE,PA.PrimerNombre,PA.SegundoNombre,PA.ApellidoPaterno,PA.ApellidoMaterno,SER.Nombre,EMP.DNI AS DNIMEDICO,SER.IdEspecialidad
 				FROM Atenciones AS A INNER JOIN Medicos AS MED ON A.IdMedicoIngreso=MED.IdMedico INNER JOIN Empleados AS EMP 
 				ON MED.IdEmpleado=EMP.IdEmpleado INNER JOIN Pacientes AS PA ON PA.IdPaciente=A.IdPaciente INNER JOIN Servicios AS SER
 				ON SER.IdServicio=A.IdServicioIngreso  AND CONVERT(VARCHAR,A.FechaIngreso,23)='{fecha}' AND EMP.DNI='{dni}' AND SER.IdTipoServicio=1 AND A.idEstadoAtencion=1"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def query_TodosMedicinaFisica(self,fecha):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT PA.NroDocumento AS DNIPACIENTE,PA.PrimerNombre,PA.SegundoNombre,PA.ApellidoPaterno,PA.ApellidoMaterno,SER.Nombre,EMP.DNI AS DNIMEDICO,SER.IdEspecialidad
 				FROM Atenciones AS A INNER JOIN Medicos AS MED ON A.IdMedicoIngreso=MED.IdMedico INNER JOIN Empleados AS EMP 
 				ON MED.IdEmpleado=EMP.IdEmpleado INNER JOIN Pacientes AS PA ON PA.IdPaciente=A.IdPaciente INNER JOIN Servicios AS SER
 				ON SER.IdServicio=A.IdServicioIngreso  AND CONVERT(VARCHAR,A.FechaIngreso,23)='{fecha}'  AND SER.IdEspecialidad=51 AND SER.IdTipoServicio=1 AND A.idEstadoAtencion=1"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
	def query_PerteneceMedicinaFisica(self,dni,fecha):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT COUNT(EM.DNI) AS valor FROM ProgramacionMedica AS P INNER JOIN Medicos AS M ON P.IdMedico=M.IdMedico INNER JOIN Empleados
			AS EM ON M.IdEmpleado=EM.IdEmpleado WHERE  P.IdEspecialidad=51 AND CONVERT(DATE,P.Fecha)='{fecha}' AND EM.DNI='{dni}'"""
			cursor.execute(sql)
			rows=cursor.fetchone()			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows


	def query_MedicoData(self,fechaI,fechaF,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]		
			sql=f"""SELECT TOP 1 PA.NroDocumento AS DNIPACIENTE,PA.PrimerNombre,PA.SegundoNombre,PA.ApellidoPaterno,PA.ApellidoMaterno,SER.Nombre,EMP.DNI AS DNIMEDICO,SER.IdEspecialidad,ES.Nombre as especialidad,
 				EMP.Nombres,EMP.ApellidoPaterno as map,EMP.ApellidoMaterno AS mam  FROM Atenciones AS A INNER JOIN Medicos AS MED ON A.IdMedicoIngreso=MED.IdMedico INNER JOIN Empleados AS EMP 
 				ON MED.IdEmpleado=EMP.IdEmpleado INNER JOIN Pacientes AS PA ON PA.IdPaciente=A.IdPaciente INNER JOIN Servicios AS SER ON SER.IdServicio=A.IdServicioIngreso INNER JOIN Especialidades AS ES ON 
 				SER.IdEspecialidad=ES.IdEspecialidad AND EMP.DNI='{dni}' AND SER.IdTipoServicio=1 AND A.idEstadoAtencion=1 AND CONVERT(VARCHAR,A.FechaIngreso,23) BETWEEN '{fechaI}' AND '{fechaF}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows		

	def query_datosPaciente(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT P.PrimerNombre,P.ApellidoPaterno,P.ApellidoMaterno,D.Nombre,P.NroHistoriaClinica,P.Telefono FROM Pacientes AS
			 P INNER JOIN Distritos AS D ON P.IdDistritoProcedencia=D.IdDistrito AND NroDocumento='{dni}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def query_PacienteSindireccion(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			sql=f"""SELECT P.PrimerNombre,P.ApellidoPaterno,P.ApellidoMaterno,P.NroHistoriaClinica,P.Telefono FROM Pacientes AS P WHERE P.NroDocumento='{dni}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def query_EspecialidadesExterno(self):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT DISTINCT E.Nombre,E.IdEspecialidad FROM Servicios AS S INNER JOIN Especialidades AS E ON
			 S.IdEspecialidad=E.IdEspecialidad AND S.IdTipoServicio=1 ORDER BY E.Nombre ASC"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows		

	def query_Empleado(self,nombre):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT DNI,Nombres,ApellidoPaterno,ApellidoMaterno  FROM Empleados WHERE Nombres LIKE '{nombre}%' OR ApellidoPaterno LIKE '{nombre}%'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows		

	def query_EmpleadoDNI(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT DNI,Nombres,ApellidoPaterno,ApellidoMaterno  FROM Empleados WHERE DNI='{dni}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def query_PacienteXHCL(self,hcl):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			#sql=f"""SELECT PrimerNombre,ApellidoPaterno,ApellidoMaterno,NroHistoriaClinica,FechaNacimiento FROM Pacientes WHERE NroHistoriaClinica='{hcl}'"""
			sql=f"""SELECT P.PrimerNombre,P.ApellidoPaterno,P.ApellidoMaterno,P.NroHistoriaClinica,P.FechaNacimiento, TS.Descripcion FROM Pacientes as P INNER JOIN TiposSexo AS TS ON 
			P.IdTipoSexo=TS.IdTipoSexo WHERE P.NroHistoriaClinica='{hcl}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def query_NoAtendidos(self,fechai,fechaf,especialidad,nrodocumento):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]	
			
			sql=f"""SELECT PA.NroDocumento,PA.PrimerNombre,PA.ApellidoPaterno,PA.ApellidoMaterno,ESPE.Nombre,A.FechaIngreso
 					FROM Atenciones AS A INNER JOIN Medicos AS MED ON A.IdMedicoIngreso=MED.IdMedico INNER JOIN Empleados AS EMP 
 					ON MED.IdEmpleado=EMP.IdEmpleado INNER JOIN Pacientes AS PA ON PA.IdPaciente=A.IdPaciente INNER JOIN Servicios AS SER
 					ON SER.IdServicio=A.IdServicioIngreso INNER JOIN Especialidades AS ESPE ON SER.IdEspecialidad=ESPE.IdEspecialidad WHERE  
 					 SER.IdTipoServicio=1  AND ESPE.Nombre='Endocrinología' AND CAST(A.FechaIngreso AS DATE)  BETWEEN '{fechai}' AND '{fechaf}' 
 					 AND PA.NroDocumento='{nrodocumento}'
				"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def query_Hospitalizados(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]	
			
			sql=f"""SELECT DISTINCT P.NroDocumento,P.PrimerNombre,P.SegundoNombre,P.ApellidoPaterno,
			P.ApellidoMaterno,P.NroHistoriaClinica FROM Atenciones AS AT INNER JOIN 
			Pacientes AS P ON AT.IdPaciente=P.IdPaciente WHERE AT.IdTipoServicio=3 AND 
			P.NroDocumento='{dni}' AND AT.IdTipoAlta IS NULL"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def query_EspecialidadMedico(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]	
			
			sql=f"""SELECT EM.DNI,EM.Nombres,EM.ApellidoPaterno,EM.ApellidoMaterno,ES.Nombre,ES.IdEspecialidad FROM Empleados 
			AS EM INNER JOIN Medicos AS M ON EM.IdEmpleado=M.IdEmpleado INNER JOIN MedicosEspecialidad AS ME ON ME.IdMedico=M.IdMedico 
			INNER JOIN Especialidades AS ES ON ES.IdEspecialidad=ME.IdEspecialidad WHERE EM.DNI='{dni}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def query_IdDistritoProcedencia(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]	
			
			sql=f"""SELECT COUNT(P.NroDocumento) AS NRO FROM Pacientes AS P INNER JOIN Distritos AS D 
			ON P.IdDistritoProcedencia=D.IdDistrito WHERE P.NroDocumento='{dni}' """
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def query_Especialidades(self,valor):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT DISTINCT E.Nombre,E.IdEspecialidad FROM Servicios AS S INNER JOIN Especialidades AS E ON
			 S.IdEspecialidad=E.IdEspecialidad WHERE E.Nombre LIKE '{valor}%' ORDER BY E.IdEspecialidad ASC"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def datosEmpleadoEspecialidad(self,codigo):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT DISTINCT EMP.DNI,EMP.Nombres,EMP.ApellidoPaterno,EMP.ApellidoMaterno FROM Empleados AS EMP INNER JOIN Medicos AS ME ON EMP.IdEmpleado=ME.IdEmpleado 
			INNER JOIN MedicosEspecialidad AS MESP ON ME.IdMedico=MESP.IdMedico WHERE MESP.IdEspecialidad={codigo}"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def datos_EmpleadosConsultorioExt(self,dni):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM Empleados AS EMP INNER JOIN 
			Medicos AS M ON M.IdEmpleado=EMP.IdEmpleado WHERE EMP.DNI='{dni}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def datos_MedicoDNI(self,i_medico):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM Empleados AS EMP INNER JOIN 
			Medicos AS M ON M.IdEmpleado=EMP.IdEmpleado WHERE M.IdMedico={i_medico}"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def datos_Medicoss(self,medico):
		obj_conectar=conect_bd.Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT DNI FROM Medicos AS M INNER JOIN Empleados AS EMPLE ON M.IdEmpleado=EMPLE.IdEmpleado 
			WHERE EMPLE.Nombres+' '+EMPLE.ApellidoPaterno+' '+EMPLE.ApellidoMaterno='{medico}' """
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows



		