import logging
from logl_ import Login as obj


logging.basicConfig(filename='app.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
if __name__=='__main__':
	try:
		logging.info("inicio de la aplicacion")
		obj()
		logging.info("la aplicacion se ejecuto correctamente")

	except Exception as e:
		logging.error(f'ocurrio un error: {e} ')
	