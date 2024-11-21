import requests
import json

def datos_persona(url):	
	response=requests.get(url)
	nombres=''
	apellidop=''
	apellidom=''
	if response.status_code==200:
		contenido=response.content		
		datos_personales=json.loads(contenido.decode('utf8'))
		nombres=datos_personales['nombres']
		apellidop=datos_personales['apellidoPaterno']
		apellidom=datos_personales['apellidoMaterno']
	return nombres,apellidop,apellidom





#print(response)

