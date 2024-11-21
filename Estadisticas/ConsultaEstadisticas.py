import conect_bd
from tkinter import messagebox
import pyodbc
class ConsultaEstadistica(object):

	def __init__(self):
		pass

	def cupos_Total(self):
		pass
	def consulta_medicos(self):
		obj_conectar=conect_bd.Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f'''SELECT Medico FROM TRIAJE GROUP BY Medico ORDER BY Medico'''
			cursor.execute(sql)
			rows=cursor.fetchall()
			return rows
		except Exception as e:
			raise e