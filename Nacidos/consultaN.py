import conect_bd
import pyodbc
from tkinter import messagebox
class Consulta(object):

	def __init__(self):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		self.cursor=obj_conectar.get_cursor()
	
	def insertarMadre(self,dni,grupof,rpm,hta,itu3,dosis,cpn,observacion,usuario,ingresoAlojamiento,Egestacional):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			nro=0		
			IdM=self.get_id('MADRE','IDMADRE')
			nro=IdM[0].ID		
			if nro==None:
				nro=1
			else:
				nro=nro+1
		
			sql=f"""INSERT INTO MADRE VALUES({nro},'{dni}','{grupof}','{rpm}','{hta}','{itu3}','{dosis}',0,0,'{cpn}','{observacion}','{usuario}',GETDATE(),'{ingresoAlojamiento}',{Egestacional},0)"""
			cursor.execute(sql)
			cursor.commit()
			return cursor.rowcount
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
		

	def deleteMadre(self,idMadre):
		try:
			obj_conectar=conect_bd.Conexion_Triaje()
			obj_conectar.ejecutar_conn()
			cursor=obj_conectar.get_cursor()
			sql=f"""DELETE FROM MADRE WHERE IDMADRE={idMadre}"""
			cursor.execute(sql)
			cursor.commit()
			return cursor.rowcount
		except Exception as e:
			messagebox.showerror("Error",e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
	
	def deleteTable(self,tabla,campo,valor):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""DELETE FROM {Tabla} WHERE {campo}={valor}"""
			cursor.execute(sql)
			cursor.commit()
			nro=cursor.rowcount
			cursor.close()
			return nro
		except Exception as e:
			messagebox.showerror("Error",e)
		finally:
			obj_conectar.close_conection()
		
	def insertParto(self,procedencia,idmadre,hiso,heso,hisp,tipoP,cesaria):
		nro=0
		IdP=self.get_id('PARTO','ID_PARTO')
		nro=IdP[0].ID
		if nro==None:
			nro=1
		else:
			nro=nro+1

		#print('here',nro,procedencia,idmadre,hiso,heso,hisp,tipoP,cesaria)
		sql=f"""INSERT INTO PARTO VALUES({nro},'{procedencia}',{idmadre},'{hiso}','{heso}','{hisp}','{tipoP}','{cesaria}')"""
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount		

	def get_id(self,Tabla,idd):
		
		try:
			rows=[]
			sql=f"""SELECT MAX({idd}) AS ID FROM {Tabla}"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def get_idTable(self,Tabla,condicionName,condicionValor,idname):
		try:
			rows=[]
			sql=f"""SELECT {idname} FROM {Tabla} WHERE {condicionName}={condicionValor}"""
			
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)
	def QUERY_MADRE(self,idmadre):
		try:
			rows=[]
			sql=f"""SELECT IDMADRE FROM MADRE WHERE IDMADRE={idmadre} AND INGRESOALOJAMIENTO='1'"""
			
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def get_idTableSTR(self,Tabla,condicionName,condicionValor,idname):
		try:
			rows=[]
			sql=f"""SELECT {idname} FROM {Tabla} WHERE {condicionName}='{condicionValor}'"""
			
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_Tabla(self,Tabla,condicion1,condicion2,valor1,valor2):
		try:
			rows=[]
			sql=f"""SELECT * FROM {Tabla} WHERE {condicion1}={valor1} OR {condicion2}={valor2}"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)
	def consultarResponsableAtencion(self,valor):
		try:
			obj_conectar=conect_bd.Conexion_Triaje()
			obj_conectar.ejecutar_conn()
			cursor=obj_conectar.get_cursor()
			
			sql=f"""SELECT * FROM RES_ATENCION AS RA INNER JOIN AIR AS A ON RA.Id_AIR=A.Id_AIR
				INNER JOIN MADRE AS M ON A.IDMADRE=M.IDMADRE WHERE M.IDMADRE={valor}"""		
			
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except pyodbc.Error as error:
			print(">",error)
		finally:
			obj_conectar.close_conection()
			return rows
	def consultarTop100(self,tabla):
		try:
			obj_conectar=conect_bd.Conexion_Triaje()
			obj_conectar.ejecutar_conn()
			cursor=obj_conectar.get_cursor()
			
			sql=f"""SELECT TOP 100 * FROM {tabla} ORDER BY IDMADRE DESC"""		
			
			cursor.execute(sql)
			rows=cursor.fetchall()
			
		except pyodbc.Error as error:
			print(">",error)
		finally:
			obj_conectar.close_conection()
			return rows


	def consulta_IngresoLlenar(self,Tabla,condicion1,condicion2,condicion3,valor1,valor2,valor3):
		try:
			rows=[]
			sql=f"""SELECT * FROM {Tabla} WHERE ({condicion1}={valor1} OR {condicion2}={valor2}) AND ({condicion3}={valor3})"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_TablaAND(self,Tabla,condicion1,condicion2,valor1,valor2,Retornar):
		try:
			rows=[]
			sql=f"""SELECT {Retornar} FROM {Tabla} WHERE {condicion1}={valor1} AND {condicion2}={valor2}"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_Tabla1(self,Tabla,condicion1,valor1):
		try:
			rows=[]
			sql=f"""SELECT * FROM {Tabla} WHERE {condicion1}={valor1}"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_TablaALL(self):
		try:
			rows=[]
			sql=f"""SELECT A.Id_AIR,M.IDMADRE,M.DNI AS MADRE,A.HCL AS NACIDO,A.CNV,A.HCL FROM MADRE AS M INNER JOIN AIR AS A ON M.IDMADRE=A.IDMADRE AND M.estadoPARTO=1 AND M.estadoAIRN=1 AND A.estado=0"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_General(self,fechai,fechaf):
		try:
			rows=[]
			sql=f"""SELECT M.DNI,M.GRUPO_FACTOR,A.HCL,A.CNV,A.PESO,A.TALLA,A.PC,A.PT,A.PA,A.PB,A.EX_FI,A.FUR,A.APGAR_1,A.Fecha_Nacimiento,A.APGAR_5,A.APGAR_10,A.ASFIXIA,A.GRUPO_FACTOR AS GRUPORNA,M.EGESTACIONAL,
			CONCAT(PA.Nombre,' ',PA.Apellido_Paterno,' ',PA.Apellido_Materno) AS RESPONSABLEATENCION FROM MADRE AS M 
			INNER JOIN AIR AS A ON M.IDMADRE=A.IDMADRE INNER JOIN  RES_ATENCION AS RA ON A.Id_AIR=RA.Id_AIR INNER JOIN USUARIO AS U ON M.usuario=U.Usuario INNER JOIN PACIENTE AS PA ON U.dni=PA.dni
			WHERE A.Fecha_Nacimiento BETWEEN '{fechai}' AND '{fechaf}'
			"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)	

	def Interconsulta(self,fechai,fechaf):
		try:
			rows=[]
			sql=f"""SELECT M.DNI,A.HCL,A.CNV,A.PESO,A.TALLA,A.PC,A.PT,A.PA,A.PB,A.EX_FI,A.FUR,A.APGAR_1,A.Fecha_Nacimiento,
			A.APGAR_5,A.APGAR_10,A.ASFIXIA,A.GRUPO_FACTOR AS GRUPORNA,A.RESP_MEDICO_INTERCONSULTA,M.EGESTACIONAL,
			CONCAT(PA.Nombre,' ',PA.Apellido_Paterno,' ',PA.Apellido_Materno) AS RESPONSABLEATENCION FROM MADRE AS M 
			INNER JOIN AIR AS A ON M.IDMADRE=A.IDMADRE INNER JOIN  RES_ATENCION AS RA ON A.Id_AIR=RA.Id_AIR INNER JOIN USUARIO AS U ON M.usuario=U.Usuario INNER JOIN PACIENTE AS PA ON U.dni=PA.dni
			WHERE (A.Fecha_Nacimiento BETWEEN '{fechai}' AND '{fechaf}') AND INTERCONSULTA=1
			"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def Update_Tabla(self,Tabla,variable,valorVariable,condicion,valor):
		sql=f"""UPDATE {Tabla} SET {variable}={valorVariable} WHERE {condicion}={valor}"""
		self.cursor.execute(sql)
		self.cursor.commit()
		return self.cursor.rowcount

	def Update_DataTables(self,Tabla,datos,condicion,valorcondicion):
		try:
			obj_conectar=conect_bd.Conexion_Triaje()
			obj_conectar.ejecutar_conn()
			cursor=obj_conectar.get_cursor()
			sql=f"UPDATE {Tabla} SET "
			sql1=""
			for clave,valor in datos.items():
				try:
					int(valor)
					sql1=sql1+f"{clave}={valor}, "
				except Exception as e:
					sql1=sql1+f"{clave}='{valor}', "	

			
			sql=sql+sql1[:-2]+f" WHERE {condicion}={valorcondicion}"
			
			cursor.execute(sql)
			cursor.commit()
			cursor.close()
			return cursor.rowcount
		except pyodbc.Error as error:
			print(">",error)
		finally:
			obj_conectar.close_conection()



	def insertDataTable(self,Tabla,lista,valores):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			lista1=','.join(lista)			
			sql=f"INSERT INTO {Tabla} ({lista1}) values{valores} "		
			cursor.execute(sql)
			cursor.commit()
			cursor.close()
			return cursor.rowcount
		except pyodbc.Error as error:
			print(">",error)
		finally:
			obj_conectar.close_conection()
		

	def Insert_AIRN(self,datos,fechaN,iduser):
		nro=0
		IdAirn=self.get_id('AIR','Id_AIR')
		nro=IdAirn[0].ID
		if nro==None:
			nro=1
		else:
			nro=nro+1
		
		try:
			sql=f"""INSERT INTO AIR(Id_AIR,HCL,CNV,T_PINZA,CONTAC_PRECOZ,INI_LME,CONTAC_PAPACANGURO,PESO,TALLA,
			PC,PT,PA,PB,EX_FI,FUR,APGAR_1,APGAR_5,APGAR_10,TEMPERATURA,PROF_OCULAR,VIT_K,CLASF_NUTRICIONAL,
			L_AMNIOTICO,KRISTELLER,MECONIO,ORINA,ASFIXIA,DESTINO_RN,OBS_RN,GRUPO_FACTOR,IDMADRE,H_EGRESO_AIRN,
			estado,Fecha_Nacimiento,estadoAlojamiento,IdUser,Hospitalizado,INTERCONSULTA,RESP_MEDICO_INTERCONSULTA,
			FINANCIAMIENTO,RNEONATAL,REANIMACIONNEONATAL) 
			VALUES({nro},'{datos[0]}','{datos[1]}','{datos[2]}','{datos[3]}','{datos[4]}','{datos[5]}',{datos[6]},{datos[7]},
			{datos[8]},{datos[9]},{datos[10]},{datos[11]},{datos[12]},{datos[13]},{datos[14]},{datos[15]},{datos[16]}
			,{datos[17]},'{datos[18]}','{datos[19]}',
			'{datos[20]}','{datos[21]}','{datos[22]}','{datos[23]}','{datos[24]}','{datos[25]}','{datos[26]}','{datos[27]}'
			,'{datos[28]}','{datos[29]}','{datos[30]}',0,'{fechaN}',0,{iduser},{datos[31]},'{datos[32]}','{datos[33]}','{datos[34]}','{datos[35]}'
			,'{datos[36]}')"""
			print(sql)
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount,nro
		except Exception as e:
			messagebox.showerror("Error",f"No se pudo insertar {e} \n se requiere llenar todos los campos!!")

	def deleteTable(self,Tabla,campo,idData):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"""DELETE FROM {Tabla} WHERE {campo}={idData}"""
			cursor.execute(sql)
			cursor.commit()
			nro=cursor.rowcount
			cursor.close()
			return nro
		except Exception as e:
			messagebox.showerror("Error",e)
		finally:
			obj_conectar.close_conection()

	def Insert_AIRNObservacion(self,datos):

		try:
			sql=f"""INSERT INTO OBSERVACIONAIRN(id_obs,Id_AIR,ID_ALOJAMIENTO,FECHAI,FECHAS,ESTADO) 
			VALUES({datos[0]},{datos[1]},{datos[2]},'{datos[3]}','{datos[4]}',{datos[5]})"""
			
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount
			
		except Exception as e:
			messagebox.showerror("Error",f"No se pudo insertar {e}!!")

	def Insert_AIRNObservacionDX(self,datos):		
		try:

			sql=f"""INSERT INTO DXOBSERVACIONAIRN VALUES({datos[0]},'{datos[1]}','{datos[2]}','{datos[3]}',{datos[4]})"""
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount
		except Exception as e:
			messagebox.showerror("Error",f"No se pudo insertar {e} \n se requiere llenar todos los campos!!")

	def AltaObservacion(self,estado,idobs):
		try:
			sql=f"""UPDATE OBSERVACIONAIRN SET FECHAS=GETDATE(),ESTADO='{estado}' WHERE id_obs={idobs}"""
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount
		except Exception as e:
			messagebox.showerror("Error",f"No se pudo insertar {e} \n se requiere llenar todos los campos!!")

	def insertarDxAIR(self,codcie,idair):
		try:
			sql=f"""INSERT INTO DXAIRN VALUES('{codcie}',{idair})"""
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount
		except Exception as e:
			messagebox.showerror("Error",f"No se pudo insertar {e}")		

	def Insert_RESATENCION(self,datos,tecnicaE,air):
		nro=0
		IdRes=self.get_id('RES_ATENCION','ID_RESPONSABLE')
		nro=IdRes[0].ID

		if nro==None:
			nro=1
		else:
			nro=nro+1
		
		try:
			sql=f"""INSERT INTO RES_ATENCION VALUES({nro},'{datos[0]}','{tecnicaE}','{datos[1]}','{datos[2]}',{air})"""
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount
		except Exception as e:
			messagebox.showerror('Error',e)		

	def ConsultaIngresaAlojamiento(self):
		try:
			rows=[]
			sql=f"""SELECT M.DNI,A.HCL,A.Id_AIR FROM AIR AS A INNER JOIN MADRE AS M ON A.IDMADRE=M.IDMADRE WHERE
			   A.estado=1 AND A.estadoAlojamiento=0 AND A.DESTINO_RN=6"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def Report_GeneralRN(self,desde,hasta):
		rows=[]
		sql=f"""SELECT A.Id_AIR,A.HCL,A.CNV,A.Fecha_Nacimiento,A.PESO,A.TALLA,M.EGESTACIONAL,M.DNI,P.tipo_Parto,A.FINANCIAMIENTO 
		FROM MADRE AS M INNER JOIN AIR AS A ON M.IDMADRE=A.IDMADRE INNER JOIN PARTO AS P ON P.IDMADRE=M.IDMADRE
		WHERE A.Fecha_Nacimiento BETWEEN '{desde}' AND '{hasta}'"""
		self.cursor.execute(sql)
		rows=self.cursor.fetchall()
		return rows

	def consulta_datosAir(self,id_air):
		try:
			rows=[]
			sql=f"""SELECT * FROM AIR AS A INNER JOIN MADRE AS M ON A.IDMADRE=M.IDMADRE INNER JOIN PARTO AS P ON M.IDMADRE=P.IDMADRE AND A.Id_AIR={id_air}"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_datosAirDX(self,id_air):
		try:
			rows=[]
			sql=f"""SELECT * FROM DXAIRN AS DX INNER JOIN CIE AS C ON DX.CODCIE=C.CODCIE WHERE DX.Id_AIR={id_air}"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_DigitadosAIRN(self):
		try:
			rows=[]
			sql=f"""SELECT TOP 50 M.DNI,M.GRUPO_FACTOR,A.HCL,A.Fecha_Nacimiento,A.Id_AIR FROM MADRE AS 
			M INNER JOIN AIR AS A ON M.IDMADRE=A.IDMADRE WHERE M.estadoAIRN=1 AND M.estadoPARTO=1 AND A.estado=1 ORDER BY A.Fecha_Nacimiento DESC """
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_DigitadosAIRNLike(self,hcl):
		try:
			rows=[]
			sql=f"""SELECT  M.DNI,M.GRUPO_FACTOR,A.HCL,A.Id_AIR FROM MADRE AS 
			M INNER JOIN AIR AS A ON M.IDMADRE=A.IDMADRE AND M.estadoAIRN=1 AND M.estadoPARTO=1 AND A.estado=1 AND A.HCL LIKE '{hcl}%'"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_DigitadosAlojamiento(self):
		try:
			rows=[]
			sql=f"""SELECT M.DNI,A.HCL FROM AIR AS A INNER JOIN MADRE AS M ON A.IDMADRE=M.IDMADRE AND A.estadoAlojamiento=1"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

	def consulta_DigitadosAlojamientoLike(self,hcl):
		try:
			rows=[]
			sql=f"""SELECT M.DNI,A.HCL FROM AIR AS A INNER JOIN MADRE AS M ON A.IDMADRE=M.IDMADRE AND A.estadoAlojamiento=1 AND A.HCL LIKE '{hcl}%'"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()			
			return rows
		except Exception as e:
			print(e)

#tamizaje
	def insert_Tamizaje(self,idairn,filtro,toma1,toma2):
		try:
			sql=f"""INSERT INTO TAMIZAJE VALUES({idairn},'{filtro}','{toma1}','{toma2}')"""		
			self.cursor.execute(sql)
			self.cursor.commit()
			return self.cursor.rowcount
		except Exception as e:
			raise e
		finally:
			pass

	def Tabla_All(self,tabla):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			rows=[]
			sql=f"SELECT * FROM {tabla}"
			cursor.execute(sql)			
			rows=cursor.fetchall()
			cursor.close()	
			return rows
		except Exception as e:
			print(e)
		
