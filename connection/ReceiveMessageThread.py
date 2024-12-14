import threading


class ReceiveMessageThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)