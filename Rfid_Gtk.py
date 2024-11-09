import gi
import threading
import nfc
import signal
from Rfid_Lector import Rfid_Lector
from gi.repository import Gtk, GLib, Gdk

gi.require_version('Gtk', '3.0')

class RfidApp(Gtk.Window):
	def __init__(self):
		super().__init__(title = "Lector RFID")
		self.set_default_size(400, 200) 													#Ajustar el tamany de la finestra
		self.set_border_width(20)															#Ajustar el tamany dels bordes
		
		distribucio = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 6)			#Layout Principal
		self.add(distribucio)

		self.msg = Gtk.Label(label = "Apropeu la targeta siusplau")							#Missatge Principal
		self.msg.set_size_request(300, 100)													#Mida desitjada del text (en blau)
		self.msg.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 1, 1))		#Fons de color blau (0, 0, 1, 1
		self.msg.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 1, 1, 1))				#Lletra de color blanc (0, 0, 0, 0)
		distribucio.pack_start(self.msg, True, True, 0)

		self.buto = Gtk.Button(label = "Clear")												#Boto Clear
		self.buto.connect("clicked", self.clear)											#Funcio que ha de cridar quan sigui clicat
		distribucio.pack_start(self.buto, True, True, 0)
		
		self.rfid_lector = Rfid_Lector()													#Crida del programa anterior (Puzzle 1)
		
		self.lect_thread = threading.Thread(target = self.lectura_rfid)						#Creació del thread de lectura
		self.lect_thread.daemon = True														#Identifiquem com a daemon
		self.lect_thread.start()															#Iniciem el thread
	
	def clear(self, widget):																#Funció del buto de clear
		self.msg.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 1, 1))		#Retorna el color a Blau
		self.msg.set_text("Apropeu la targeta siusplau")									#Retorna el missatge al original
		
	def lectura_rfid(self):																	#Funció per la lectura del uid
		while True:
			uid = self.rfid_lector.read_uid()												#Lectura del uid
			if uid:
				GLib.idle_add(self.update_msg_uid, uid.upper())								#Si la lactura es correcte (true) que s'actualitzi en el text
			else:
				threading.Event().wait(1)													#Si la lectura no es valida (false) fem que el thread s'esperi 1 segon
		
	def update_msg_uid(self, uid_hex):														#Funció per actualitzar el text amb la uid
		self.msg.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1, 0, 0, 1))		#Canviar el color a Vermell
		self.msg.set_text("uid: " + uid_hex)												#Canviar el text a la uid que ens donguin																	
	
if __name__ == "__main__":
	a = RfidApp()
	a.connect("destroy", Gtk.main_quit)
	a.show_all()
	Gtk.main()
