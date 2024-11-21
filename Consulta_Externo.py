from conect_bd import Conexion_Externo

class consultaExterno(object):

	def __init__(self):
		obj_conectar=Conexion_Externo()
		obj_conectar.ejecutar_conn()
		self.cursor=obj_conectar.get_cursor()
	def numberFuas(self):
		try:
			rows=[]
			sql="""SELECT * FROM SisFua"""
			self.cursor.execute(sql)
			rows=self.cursor.fetchall()
			return rows
		except Exception as e:
			print(e)
