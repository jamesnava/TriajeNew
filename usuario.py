import Consulta_Triaje
import GUI_User

class usuario(object):
	def __init__(self):
		self.obj_queryUser=Consulta_Triaje.queryTriaje()
		self.conectado=False
		self.obj_user=GUI_User.Usuario()
	def conectar(self,usuario,contra):
		self.obj_user.set_Password(contra)
		contrasenia=self.obj_user.Contrasenia
		rows=self.obj_queryUser.query_User(usuario,contrasenia)		
		identificador=-1
		user=""
		nivel=0
		estado="INACTIVO"
		dni=""
		idrol=0
		iduser=0		
		if len(rows)!=0:
			identificador=1
			
			for val in rows:
				user=val.Usuario
				nivel=val.Nivel
				estado=val.estado
				dni=val.dni	
				idrol=val.idRol	
				iduser=val.Id_Usuario
		else:
			identificador=-1

		return identificador,user,nivel,estado,dni,idrol,iduser



