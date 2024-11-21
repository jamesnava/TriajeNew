from cryptography.fernet import Fernet
import base64

from cryptography.fernet import Fernet
import base64

# Función para descifrar
def descifrar(llave,cifrado_base64):
	 
	try:
		fernet = Fernet(llave)
        
        # Decodificar el valor cifrado desde Base64
		binario_cifrado = base64.b64decode(cifrado_base64)
		
        
        # Desencriptar el valor
		valor_descifrado = fernet.decrypt(binario_cifrado).decode('utf-8')
		return valor_descifrado
    
	except Exception as e:
		print(f"Ocurrió un error: {type(e)}, {str(e)}")

# Función para cifrar
def cifrar(llave, texto):
	fernet = Fernet(llave)

    # Encriptar el texto
	valor_cifrado = fernet.encrypt(texto.encode())

    # Codificar el valor cifrado en Base64 para almacenamiento
	cifrado_base64 = base64.b64encode(valor_cifrado).decode('utf-8')
	return cifrado_base64

