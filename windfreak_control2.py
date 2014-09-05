# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 17:32:49 2014

@author: Nick Lewty

Python software for communicating with windfreak USB2

Windfreak USB2 is a $250 PLL that can set frequencies between  34.4MHz - 4.4GHz 

Details about windfreak can be found at this web address 

http://www.windfreaktech.com/

Code fairly simple hence no comments in the code
"""

import serial

class windfreakusb2(object):
    
    baudrate = 115200
    
    def __init__(self, port):
        self.serial = self._open_port(port)
        
    def _open_port(self, port):
        ser = serial.Serial(port, self.baudrate, timeout=5)
        ser.readline()
        ser.timeout = 1
        return ser

    def _serial_write(self, string):
        self.serial.write(string + '\n')
    
    def _serial_read(self):
        msg_string = self.serial.readline()
        # Remove any linefeeds etc
        msg_string = msg_string.rstrip()
        return msg_string
    
    def get_freq(self):
        self._serial_write('f?')
        return self._serial_read()
        
    def get_power(self):
        self._serial_write('a?')
        return self._serial_read()
    
    def set_freq(self,value):
        self._serial_write('f' + str(value))
        
    def check_osci(self):
        self._serial_write('p')
        return self._serial_read()

    def set_power(self,value):
        self._serial_write('a' + str(value))
    
    def serial_number(self):
        self._serial_write('+')
        return self._serial_read()
    

    
    
        
        


	
					


