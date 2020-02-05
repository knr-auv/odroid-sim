
from server import *
from threading import Thread

#ip = '192.168.137.208' #adres odroida

# IP_ADDRESS_1 = '10.42.0.158'  # address jetson
# IP_ADDRESS_2 = '192.168.137.208'  # address odroid
#
# PORT = 8181

#klasa służaca do tworzenia wątku ktory wyswietla presłane mu obiekty(na potrzeby testów)
class DataUser():
	def __init__(self, dataFrame):
		self.dataFrame = dataFrame

	def useData(self):
		for frame in self.dataFrame:
			print(frame)
		print('WAITING FOR NEXT DATA...')

	def setDataFrame(self, dataFrame):
		self.dataFrame = dataFrame

class Connection(Thread):
	def __init__(self, ip, port):
		Thread.__init__(self)
		self.server = Server(ip, port)
		#obiekt stworzony do testow, sama koncepcja wykorzystywania odebranych danych do zmiany
		self.dataUser = DataUser([])
		self.dataFrame = []
		print('Server running at', ip, ': PORT :', port)

	def run(self):
		while True:
			self.dataFrame = self.server.receiveData()
			#self.dataUser.setDataFrame(self.dataFrame)
			#self.usingThread = Thread(target=self.dataUser.useData)
			#self.usingThread.start()

	def getDataFrame(self):
		return self.dataFrame


if __name__ == '__main__':
	print('start connection')
	conn = Connection('10.41.0.42', 8787) #w MainOdroid
	conn.start()
