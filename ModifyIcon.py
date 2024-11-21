from PIL import Image, ImageTk

def modificar_Icon(address):
	img=Image.open(address)
	img=img.resize((16,16))
	icono=ImageTk.PhotoImage(img)
	return icono