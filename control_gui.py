# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 15:26:04 2015

@author: nick
"""

import sys
import glob
import serial
import windfreak_control2 as wc
from PyQt4 import QtGui, uic
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QPixmap
import datetime


form_class = uic.loadUiType("windfreakgui.ui")[0] 

def serial_ports():
    
	"""Lists serial ports
	:raises EnvironmentError:
	On unsupported or unknown platforms
	:returns:
	A list of available serial ports
	"""				
	if sys.platform.startswith('win'):
		ports = ['COM' + str(i + 1) for i in range(256)]
	elif sys.platform.startswith('linux'):
	# this is to exclude your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	
	else:
		raise EnvironmentError('Unsupported platform')
	
	result = []
	for port in ports:
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
		except serial.SerialException:
			pass
	return result
    




class MyWindowClass(QtGui.QMainWindow, form_class):
	connected = bool(False)
	windfreak = None 
	time = 0
	
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.ButtonUpdate.clicked.connect(self.ButtonUpdate_clicked)# Bind the event handlers
		self.ButtonConnect.clicked.connect(self.ButtonConnect_clicked)
		self.comboSerialBox.addItems(serial_ports()) #Gets a list of avaliable serial ports to connect to and adds to combo box
		
		
	def ButtonConnect_clicked(self,connection):
		if not self.connected:
			self.windfreak = wc.windfreakusb2(str(self.comboSerialBox.currentText()))
			self.timer = QTimer()
			self.connected = True
			self.timer.timeout.connect(self.update)
			self.timer.start(1000)
			self.control_label.setText('connected to ' + str(self.comboSerialBox.currentText()))
			self.freq = float(self.windfreak.get_freq())/1000
			self.power = self.windfreak.get_power()
			self.label_freq.setText(str(self.freq))
			self.label_power.setText(str(self.power))
			self.windfreak.set_clock(str(1)) #sets internal clock so that is locks
			self.windfreak.set_freq(str(self.freq))
			
	def ButtonUpdate_clicked(self,value):
		self.windfreak.set_freq(self.freq_box.text())
		self.freq = float(self.windfreak.get_freq())/1000
		self.label_freq.setText(str(self.freq))
		print 'done'
		
	def update(self):
		self.time = self.time + 1
		#self.freq = self.textSetfreq.textChanged[str]
		
		

app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
