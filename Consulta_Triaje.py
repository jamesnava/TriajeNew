import conect_bd
from tkinter import messagebox


class queryTriaje(object):
	def __init__(self):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		self.cursor=obj_conectar.get_cursor()
	
	def query_Paciente(self,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT dni,Nombre,Apellido_Paterno,Apellido_Materno,Telefono,Procedencia FROM PACIENTE WHERE dni='{dni}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows	
			
	def query_User(self,usuario,contra):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM USUARIO WHERE Usuario='{usuario}' AND Clave='{contra}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def Insert_Cita(self,usuario,dni,fuente,cupo,n_referencia,medico,consultorio,fecha_Atencion,telefono,establecimiento,continuador,FUA,HCL,turno,tipocupo,idservicio,dnimedico):
		
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""INSERT INTO TRIAJE(Id_Usuario,dni,idFuente,Nro_Cupo,Nro_Referencia,Medico,Especialidad,
			Fecha_Atencion,Telefono,P_C,Continuador,FUA,Historia,Turno,FechaR,Id_Etriaje,ID_TIPOA,Cod_Servicio,DniMedico)
			VALUES({usuario},'{dni}','{fuente}','{cupo}',{n_referencia},'{medico}','{consultorio}',
			'{fecha_Atencion}','{telefono}','{establecimiento}','{continuador}','{FUA}','{HCL}','{turno}'
			,GETDATE(),1,{tipocupo},'{idservicio}','{dnimedico}')"""

			cursor.execute(sql)
			cursor.commit()
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
		

	def Anular_Cita(self, cupo, fecha, consultorio,medico,turno):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""UPDATE TRIAJE SET Id_Etriaje=2 OUTPUT INSERTED.Id_Triaje WHERE 
			(Nro_Cupo={cupo} AND Fecha_Atencion='{fecha}' AND Especialidad='{consultorio}') AND (Medico='{medico}' 
			AND Turno='{turno}')"""
			cursor.execute(sql)		
			id_modificado=cursor.fetchone()
			cursor.commit()
			
		except Exception as e:
			print(e)
		finally:			
			cursor.close()
			obj_conectar.close_conection()
			return id_modificado
		

	def query_Cupo(self,fecha,consultorio,Dmedico,turno):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT Nro_Cupo,dni,Id_Etriaje,ID_TIPOA FROM TRIAJE 
			WHERE (Fecha_Atencion='{fecha}' AND Especialidad='{consultorio}') 
			AND (DniMedico='{Dmedico}' AND Turno='{turno}')"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
		
	def query_PacienteCuposLast(self,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT Nro_Cupo,dni,Especialidad,Fecha_Atencion,Medico FROM TRIAJE WHERE  (Fecha_Atencion >=(SELECT CONVERT(VARCHAR(10),GETDATE(),23))) AND dni='{dni}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def query_UserName(self,usuario):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT Id_Usuario FROM USUARIO WHERE Usuario='{usuario}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
		
	def delete_Cupo(self,cupo,fecha):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		
		try:
			sql=f"""DELETE FROM TRIAJE WHERE Nro_Cupo='{cupo}' AND Fecha_Atencion='{fecha}'"""
			cursor.execute(sql)
			cursor.commit()
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()		

	def query_CupoNumber(self,fecha,consultorio,cupo,turno,Dmedico):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT dni,Id_Etriaje FROM TRIAJE WHERE (Fecha_Atencion='{fecha}' AND Especialidad='{consultorio}' AND Nro_Cupo={cupo}) AND (Turno='{turno}' AND DniMedico='{Dmedico}')"""
			cursor.execute(sql)
			rows=cursor.fetchall()			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def query_AgendadoXUsuario(self,fecha,consultorio,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]		
			sql=f"""SELECT * FROM TRIAJE WHERE Fecha_Atencion='{fecha}' AND Especialidad='{consultorio}' AND dni='{dni}' AND Id_Etriaje=1"""
			cursor.execute(sql)
			rows=cursor.fetchall()			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def Insert_Paciente(self,datos):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			cursor.execute(f"""INSERT INTO PACIENTE VALUES('{datos["dni"]}','{datos["nombres"]}','{datos["apellidoP"]}','{datos["apellidoM"]}','{datos["telefono"]}','{datos["procedencia"]}')""")
			cursor.commit()
			nro=cursor.rowcount
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return nro
		
	def Consulta_DatosPaciente(self):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute(f"""SELECT top 50 * FROM PACIENTE""")
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def Consulta_DatosPacienteLIKE(self,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute(f"""SELECT * FROM PACIENTE WHERE dni LIKE '{dni}%'""")
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def Consulta_DNIPaciente(self,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:			
			
			cursor.execute(f"""SELECT * FROM PACIENTE WHERE dni LIKE '{dni}'""")
			rows=cursor.fetchone()			
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def Update_Pacientes(self,dni,nombre,apellidop,apellidom,telefono,procedencia):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			cursor.execute(f"""UPDATE PACIENTE SET Nombre='{nombre}',Apellido_Paterno='{apellidop}',Apellido_Materno='{apellidom}',Telefono='{telefono}',Procedencia='{procedencia}' WHERE dni='{dni}'""")
			cursor.commit()
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()		

	def consulta_Triaje(self,fecha,consultorio,Turno):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute(f"""SELECT * FROM TRIAJE WHERE Fecha_Atencion='{fecha}' AND Especialidad='{consultorio}' AND Turno='{Turno}'""")
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def consulta_TriajeConsultorios(self,fecha):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute(f"""SELECT * FROM TRIAJE WHERE Fecha_Atencion='{fecha}' ORDER BY Especialidad ASC""")
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def consulta_DatosPaciente(self,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]		
			cursor.execute(f"""SELECT * FROM PACIENTE WHERE dni='{dni}'""")
			rows=cursor.fetchall()		
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def consulta_Fuente(self):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute("SELECT * FROM FINANCIAMIENTO")
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def consulta_FuenteId(self,name):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute(f"""SELECT * FROM FINANCIAMIENTO WHERE fuente='{name}'""")
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows		

	def query_DataTriaje(self,fecha,consultorio,cupo,medico,turno):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			sql=f"""SELECT T.Id_Triaje,T.Id_Usuario,T.dni,T.idFuente,T.Nro_Cupo,T.Nro_Referencia
			,T.Medico,T.Especialidad,CONVERT(VARCHAR,Fecha_Atencion,106) AS Fecha_Atencion,T.Telefono,
			T.P_C,T.Continuador,T.FUA,T.Historia,T.Turno,USUARIO.Usuario,FINANCIAMIENTO.fuente,
			T.FechaR,ET.estado FROM TRIAJE AS T INNER JOIN FINANCIAMIENTO ON T.idFuente=FINANCIAMIENTO.idFuente 
			INNER JOIN USUARIO ON T.Id_Usuario=USUARIO.Id_Usuario INNER JOIN ESTADO_TRIAJE AS ET ON 
			ET.Id_Etriaje=T.Id_Etriaje AND (T.Fecha_Atencion='{fecha}' AND T.Cod_Servicio='{consultorio}' 
			AND T.Nro_Cupo={cupo}) AND (T.DniMedico='{medico}' AND T.Turno='{turno}')"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def Consulta_ExistUsuario(self,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			cursor.execute(f"""SELECT * FROM USUARIO WHERE dni='{dni}'""")
			rows=cursor.fetchall()			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def Consulta_UserExists(self,nombre):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM USUARIO WHERE Usuario='{nombre}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
			
		
	def Insert_User(self,dni,usuario,passs,nivel,idrol):
		
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""INSERT INTO USUARIO VALUES((SELECT MAX(Id_Usuario)+1 FROM USUARIO),'{dni}','{usuario}','{passs}','{nivel}',GETDATE(),'ACTIVO',{idrol})"""
			cursor.execute(sql)
			cursor.commit()
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()		

	def Consulta_Usuarios(self):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM USUARIO"""
			cursor.execute(sql)
			rows=cursor.fetchall()			
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	
	def update_State(self,estado,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""UPDATE USUARIO SET estado='{estado}' WHERE dni='{dni}'"""
			cursor.execute(sql)
			cursor.commit()
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()

	def update_Table(self,tabla,campo,condicion,campovalor,condicionvalor):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql="UPDATE {} SET {}='{}' WHERE {}='{}'".format(tabla,campo,campovalor,condicion,condicionvalor)
			cursor.execute(sql)
			cursor.commit()
			return cursor.rowcount
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
		
	def change_password(self,passs,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""UPDATE USUARIO SET Clave='{passs}' WHERE dni='{dni}'"""
			cursor.execute(sql)
			cursor.commit()
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
		

	def query_Atenciones(self,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]		
			sql=f"""SELECT TOP 20 * FROM TRIAJE INNER JOIN FINANCIAMIENTO ON TRIAJE.idFuente=FINANCIAMIENTO.idFuente INNER JOIN USUARIO ON TRIAJE.Id_Usuario=USUARIO.Id_Usuario AND TRIAJE.dni LIKE '{dni}%' 
			ORDER BY Fecha_Atencion DESC"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows		

	def query_CupoOcupado(self,cupo,medico,especialidad,turno,fecha):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]		
			sql=f"""SELECT COUNT(*) AS NRO FROM TRIAJE WHERE Nro_Cupo={cupo} AND 
			Medico='{medico}' AND Especialidad='{especialidad}' AND 
			Turno='{turno}' AND Fecha_Atencion='{fecha}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows		

	def insertar_MotivoAnulacion(self,usuario,motivo,id_triaje):		
		motivo1=motivo.strip()
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""INSERT INTO MODIFICACION_CUPO VALUES(GETDATE(),'{usuario}','{motivo1}',{id_triaje})"""
			cursor.execute(sql)
			cursor.commit()
			cursor.close()
		except Exception as e:
			print(e)
		finally:
			obj_conectar.close_conection()
		

	#:::::::::::::::consulta incidentes:::::::::::::::::
	def getId_Incidencias(self):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT MAX(Id_Incidencia) AS IDINCIDENCIA FROM Incidencias"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		
	def insert_Incidencias(self, datos):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			sql=f"""INSERT INTO Incidencias VALUES({datos[0]},'{datos[1]}','{datos[2]}','{datos[3]}','{datos[4]}','{datos[5]}',
			{datos[6]},'{datos[7]}','{datos[8]}',GETDATE(),'{datos[9]}')"""
			cursor.execute(sql)
			cursor.commit()
			nro=cursor.rowcount
		except Exception as e:
			messagebox.showerror("Alert",e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return nro


	def query_IncidenciasLike(self,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			sql=f"""SELECT * FROM Incidencias WHERE Dni_Paciente LIKE '%{dni}%'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

		

	def query_IncidenciaFechas(self,fechaI,fechaF):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			sql=f"""SELECT * FROM Incidencias WHERE Fecha BETWEEN '{fechaI}' AND '{fechaF}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
		
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	#REPORTE NO ATENDIDOS
	def ReporteNoAtendidos(self,fechaI,fechaf):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:			
			rows=[]
			#sql=f"""SELECT I.Usuario,I.Dni_Paciente,I.Especialidad,I.Fecha,I.FECHAR,U.Usuario,PA.Nombre,PA.Apellido_Paterno,PA.Apellido_Materno,PA.Telefono,I.Motivo FROM Incidencias AS I INNER JOIN USUARIO AS U 
			#ON I.Usuario=U.Id_Usuario INNER JOIN PACIENTE AS PA ON PA.dni=I.Dni_Paciente AND I.Fecha BETWEEN '{fechaI}' AND '{fechaf}' ORDER BY I.Especialidad DESC"""
		
			sql=f""" SELECT I.Usuario,I.Dni_Paciente,I.Especialidad,I.Fecha,I.FECHAR,U.Usuario,I.Motivo FROM Incidencias AS I INNER JOIN USUARIO AS U ON I.Usuario=U.Id_Usuario  
				WHERE I.FECHAR BETWEEN '{fechaI}' AND '{fechaf}' ORDER BY I.Especialidad"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()			
			obj_conectar.close_conection()
			return rows

	#CONSULTA PRODUCCION HIS

	def existencia_pacienteBD(self,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM HIS_DETA WHERE DNI_PAC='{dni}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:			
			cursor.close()
			obj_conectar.close_conection()
			return rows
	def His_Interconsultas(self,fecha,dniuser):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM HIS_DETA WHERE FechaIngreso='{fecha}' AND TCONSULTA='IC' AND DNI_USER='{dniuser}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:			
			cursor.close()
			obj_conectar.close_conection()
			return rows

		

	def existencia_pacienteBDAnio(self,dni):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT HD.DNI_PAC FROM HIS_DETA AS HD WHERE HD.DNI_PAC='{dni}' AND YEAR(HD.FechaIngreso)=YEAR(GETDATE())"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def query_cie10(self,descrip):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM CIE WHERE  CODCIE LIKE '{descrip}%' OR NOMBRE LIKE '{descrip}%'"""
			cursor.execute(sql)
			rows=cursor.fetchall()			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def query_idMAXHIS_DETA(self):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			sql=f"""SELECT MAX(ID_DETA) AS codigo FROM HIS_DETA"""
			cursor.execute(sql)
			rows=cursor.fetchall()			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def insert_HISDETA(self,id_deta,datos,tipo,establecimiento,servicio):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			sql=f"""INSERT INTO HIS_DETA VALUES({id_deta},'{datos[0]}','{datos[1]}','{datos[2]}','{datos[3]}','{datos[4]}','{datos[5]}',GETDATE(),'{datos[6]}','{datos[7]}','{datos[8]}','{tipo}','{establecimiento}','{servicio}')"""
			cursor.execute(sql)		
			cursor.commit()
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
		

	def query_idMAX_DIAGNOSTICOS(self):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			sql=f"""SELECT MAX(Id_Diagnostico) AS codigo FROM DIAGNOSTICOS"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
			
		

	def insert_DIAGNOSTICOS(self,id_DIAGNOSTICO,id_deta,datos):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			sql=f"""INSERT INTO DIAGNOSTICOS VALUES({id_DIAGNOSTICO},'{datos[1]}','{datos[2]}','{datos[3]}','{datos[0]}',{id_deta})"""
			cursor.execute(sql)		
			cursor.commit()
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()

	

	def consultaRegistroPaciente(self,dnipac,idServicio,FechaIngreso):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			sql=f"""SELECT * FROM HIS_DETA WHERE DNI_PAC='{dnipac}' AND FechaIngreso='{FechaIngreso}' AND ServicioIngreso='{idServicio}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def existencia_pacienteBDServicio(self,dnipaciente,servicio):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM HIS_DETA WHERE DNI_PAC='{dnipaciente}' AND ServicioIngreso='{servicio}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def existencia_pacienteBDServicioAnio(self,dnipaciente,servicio):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			sql=f"""SELECT * FROM HIS_DETA WHERE DNI_PAC='{dnipaciente}' AND ServicioIngreso='{servicio}' AND YEAR(FechaIngreso)=YEAR(GETDATE())"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def Query_HisDeta(self,dni,servicio,FechaIngreso):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM HIS_DETA WHERE DNI_PAC='{dni}' AND 
			ServicioIngreso='{servicio}' AND FechaIngreso='{FechaIngreso}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows 
		
	def query_DIAGNOSTICOS(self,iddeta):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			sql=f"""SELECT * FROM DIAGNOSTICOS WHERE ID_DETA={iddeta}"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def query_cie10Param(self,codigo):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()


		try:
			rows=[]
			sql=f"""SELECT * FROM CIE WHERE CODCIE='{codigo}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def Update_diagnostico(self,datos):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""UPDATE DIAGNOSTICOS SET Descripcion='{datos[1]}',TipDx='{datos[2]}',Lab='{datos[3]}',CODCIE='{datos[4]}' WHERE Id_Diagnostico={datos[0]}"""
			cursor.execute(sql)
			cursor.commit()
			
		except Exception as e:
			messagebox.showerror("Alerta",f"No pudo Ejecutarse D...! {e}")
		finally:
			cursor.close()
			obj_conectar.close_conection()
	
	def Update_DetalleHis(self,codigo,pc,pab,peso,talla,hb):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""UPDATE HIS_DETA SET PC='{pc}',Hb='{hb}',Talla='{talla}',Peso='{peso}',PAB='{pab}' WHERE ID_DETA={codigo}"""
			cursor.execute(sql)
			cursor.commit()
			nro=cursor.rowcount			
		except Exception as e:
			messagebox.showerror("Alerta",f"No pudo Ejecutarse...! {e}")
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return nro

	def datos_HojaV2(self,dni,fecha):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM HIS_DETA WHERE DNI_USER='{dni}' AND FechaIngreso='{fecha}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def datos_HojaXDias(self,dni,fechaI,fechaF,Especialidad):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"""SELECT * FROM HIS_DETA WHERE DNI_USER='{dni}' AND ServicioIngreso='{Especialidad}' AND FechaIngreso BETWEEN '{fechaI}' AND '{fechaF}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def query_DIAGNOSTICOS(self,iddeta):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			rows=[]
			sql=f"""SELECT * FROM DIAGNOSTICOS WHERE ID_DETA={iddeta}"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
		

	def query_DeleteHis(self,codigo):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			sql=f"""DELETE FROM DIAGNOSTICOS WHERE ID_DETA={codigo}
				DELETE FROM HIS_DETA WHERE ID_DETA={codigo}"""
			cursor.execute(sql)
			cursor.commit()
			nro=cursor.rowcount
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			

	def query_SelectTable(self,tabla,campocondicion,valorcondicion):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			sql=f"""SELECT * FROM {tabla} WHERE {campocondicion}={valorcondicion}"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			return rows
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			
		


	#######USUARIOS###########	

	def InsertarPerfil(self,valor):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""INSERT INTO ROL(nombre) VALUES('{valor}')"""
			cursor.execute(sql)
			cursor.commit()
			nro=cursor.rowcount
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return nro


	def consultaPefil(self):
		rows=[]
		sql="SELECT * FROM ROL"
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return rows

	def ExisteAsignacion(self,idd):
		rows=[]
		sql=f"""SELECT * FROM ASIGNACION WHERE idRol={idd}"""
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return bool(len(rows))

	def InsertarAsignaciones(self,idd,valor,estado):
		sql=f"""INSERT INTO ASIGNACION VALUES({idd},'{valor}',{estado})"""
		
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount

	def DeleteAsignacion(self,idd):
		sql=f"""DELETE FROM ASIGNACION WHERE idRol={idd}"""
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount

	def ConsultaAsignacion(self,idd):
		rows=[]
		sql=f"""SELECT * FROM ASIGNACION WHERE idRol={idd} and Estado=1"""
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return rows

	#insertar cupos
	def InsertarCupos(self,valor):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""INSERT INTO CUPOS(Cod_Servicio,Turno,Medico,Fecha,Cantidad) 
			VALUES('{valor[0]}','{valor[1]}','{valor[2]}','{valor[3]}',{valor[4]})"""
			cursor.execute(sql)
			cursor.commit()
			nro=cursor.rowcount
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return nro

	def ConsultaConfCupos(self,medico,servicio,turno,fecha):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""SELECT * FROM CUPOS WHERE Cod_Servicio={servicio} AND 
			Turno='{turno}' AND Medico={medico} AND Fecha='{fecha}'"""
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
	def ConsultaCountCupos(self,dnimedico,servicio,turno,idtipo,fechai,fechaf):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""SELECT COUNT(*) AS cantidad FROM TRIAJE WHERE  
			(DniMedico='{dnimedico}' AND TURNO='{turno}') 
			AND (Cod_Servicio={servicio} AND ID_TIPOA={idtipo}) AND Fecha_Atencion 
			BETWEEN '{fechai}' AND '{fechaf}'"""
			
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def ConsultaCountCuposXdia(self,dnimedico,servicio,turno,idtipo,fecha):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""SELECT COUNT(*) AS cantidad FROM TRIAJE WHERE  
			(DniMedico='{dnimedico}' AND TURNO='{turno}') 
			AND (Cod_Servicio={servicio} AND ID_TIPOA={idtipo}) AND Fecha_Atencion='{fecha}'"""
			
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	

	def Update_DataTables(self,Tabla,datos,condicion,valorcondicion):
		try:
			obj_conectar=conect_bd.Conexion_Triaje()
			obj_conectar.ejecutar_conn()
			cursor=obj_conectar.get_cursor()
			sql=f"UPDATE {Tabla} SET "
			sql1=""
			for clave,valor in datos.items():
				sql1=sql1+f"{clave}={valor}, "
			
			sql=sql+sql1[:-2]+f" WHERE {condicion}={valorcondicion}"
			
			cursor.execute(sql)
			cursor.commit()
			cursor.close()
			return cursor.rowcount
		except pyodbc.Error as error:
			print(">",error)
		finally:
			obj_conectar.close_conection()




