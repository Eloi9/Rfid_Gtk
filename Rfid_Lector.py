import nfc

class Rfid_Lector:
	def __init__(self): 			#Inicialitza el lector NFC
		self.clf = None
		
	def connect_reader(self):		#Conexió amb el NFC	
		if self.clf is None:
			try:
				self.clf = nfc.ContactlessFrontend('usb')
			except Exception as e:
				print("Error al llegir la targeta: " + str(e))
				self.clf = None
				
	def read_uid(self): 			#Lectura del uid i es torna en un string hex
		self.connect_reader()
		if self.clf:
			try:
				tag = self.clf.connect(rdwr={'on-connect': lambda tag: False})
				uid = tag.identifier.hex()
				return uid
			except Exception as e:
				print("Error al llegir la targeta NFC: "+ str(e))
				return None
		else:
			print("Lector NFC no disponible o desconectat")
			return None
			
	def disconnect_reader(self):	#Desconexió del LectorNFC
		if self.clf:
			self.clf.close()
			self.clf = None
	
if __name__ =="__main__":
	rf = Rfid_Lector()
	print("Esperant targeta NFC...")
	uid = rf.read_uid()
	if uid:
		print("UID de la targeta: "+ uid.upper())
	else:
		print("No s'ha pogut llegir la targerta correctament")	
