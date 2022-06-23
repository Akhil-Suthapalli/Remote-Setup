# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 12:02:40 2022

@Author: Akhil Suthapalli - R&D
@Contact: Suthapalli.Akhil@tvsmotor.com
@Mobile: +91 9494475575
"""

import os, subprocess, time

#os.environ["ANDROID_HOME"] = "C:\\Users\\suthapalli.akhil\\AppData\\Local\\Android\\Sdk"

adb_path = "C:\\Users\\suthapalli.akhil\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"
real_adb_path = os.path.realpath(adb_path)
adb_obj = None



class Adb():

	def __init__(self, adb_path, device = None):
		self.adb = adb_path
		self.device = None
		self.device_list = []

	def raw_command(self, command):
		p = subprocess.Popen(self.adb+" "+command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return p.communicate()[0].decode("utf-8")

	def devices(self):
		'''get a dict of attached devices. key is the device serial, value is device name.'''
		out = self.raw_command("devices")
		match = "List of devices attached"
		index = out.find(match)
		if index < 0:
			raise EnvironmentError("adb is not working.")
		return dict([s.split("\t") for s in out[index + len(match):].strip().splitlines() if s.strip()])

	def device_l(self):
		l = self.devices()
		t = list(l)
		self.device_list = t.copy()
		j=1
		for i in t:
			print(j,i)
			j=j+1
		return len(t)


	def select_device(self,list_num = None, device_id = None):
		if list_num != None:
			self.device = self.device_list[list_num-1]
		if device_id != None:
			self.device = device_id

	def send_command(self, command):


		if self.device == None:
			res = self.raw_command(command)
		else:
			res = self.raw_command("-s "+self.device+" "+command)

		return res


	def unlock_device(self):

		#Specific to Redmi Phone (logic can be derived here)
		#For pin kepad touch points can be traced to press for particular model
		self.send_command("shell input keyevent 26")
		time.sleep(0.5)
		self.send_command("shell input swipe 500 800 500 200 100")

	def tap_at_point(self,x,y):

		self.send_command("shell input tap "+str(int(x))+" "+str(int(y)))

	def open_app(self):
		#Darwin Box implementation
		self.send_command("shell am start com.darwinbox.darwinbox/com.darwinbox.splashscreen.ui.SplashScreenActivity")

	def find_pid(self):

		res = self.send_command("shell pidof com.akhil.chargeadequacy")

		try:
			pid = res.split()[0]
		except:
			pid = None

		return pid




	def _logcat(self, pid):

		p = subprocess.Popen(self.adb+" logcat | findstr " + str(pid), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return p


def check_in():
	global adb_obj

	adb_obj.unlock()
	time.sleep(3)
	adb_obj.open_app()
	time.sleep(10)
	adb_obj


adb_obj = Adb(adb_path = real_adb_path)





