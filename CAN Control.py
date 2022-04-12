# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 16:22:16 2022

@Author: Akhil Suthapalli - R&D
@Contact: Suthapalli.Akhil@tvsmotor.com
@Mobile: +91 9494475575
"""

import can, time, threading
import tkinter as tk
from tkinter import Button, Label, PhotoImage, Scale, HORIZONTAL

try:
	bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1')
except:
	print("Already Initalised")

#GUI box layout
root = tk.Tk()
root.geometry("500x400")
root.title("CAN Tool")
root.eval('tk::PlaceWindow . center')

"""

ID 300

Byte 1,2 	Engine Speed 	0 - 6553.5 -> 0 - 65535

ID 500
Byte 0,1 	speed      	0 - 6553.5 -> 0 - 65535
Byte 2 	 	Engine Temp  	-40 - 200  -> 0 - 255

ID 502
Byte  	1 	 	MIL, PWR, ECO
Value 	0x01 	OFF  OFF  ON
Value 	0x02 	OFF  ON   OFF
Value 	0x09 	ON   OFF  ON
Value 	0x0A 	ON   ON   OFF


"""

def mapFromTo(x,a,b,c,d):
   y=(x-a)/(b-a)*(d-c)+c
   return y

can_on = True
is_eco = True
is_mil_on = False

eco_image = PhotoImage(file = "eco2.png")
pwr_image = PhotoImage(file = "power2.png")

on = PhotoImage(file = "on.png")
off = PhotoImage(file = "off.png")

main_array = [
		#[cyclic time(ms), abritation_id, array 1 - 8 ]
		#Don't change order
		[10,0x500,0,0,0,0,0,0,0,0],
		[10,0x502,0,0x01,0,0,0,0,0,0],
		[10,0x300,0,0,0,0,0,0,0,0]
		]


"""
msg = can.Message(arbitration_id = 0x500, is_extended_id = False,
				  data=[0,255,0,0,0,0,0,0])

bus.send(msg)

"""

def change_eco_mil():

	global main_array

	if is_eco and is_mil_on:
		main_array[1][3]=0x09
	elif is_eco and not is_mil_on:
		main_array[1][3]=0x01
	elif not is_eco and is_mil_on:
		main_array[1][3]=0x0A
	elif not is_eco and not is_mil_on:
		main_array[1][3]=0x02

def change_mil():
	global is_mil_on, mil_switch

	if not is_mil_on:
		mil_switch.configure(image = on)
		is_mil_on = True
	else:
		mil_switch.configure(image = off)
		is_mil_on = False

	change_eco_mil()

def change_eco():
	global is_eco, eco_switch

	if is_eco:
		eco_switch.configure(image = pwr_image)
		is_eco = False
	else:
		eco_switch.configure(image = eco_image)
		is_eco = True

	change_eco_mil()

def check_change_speed():
	global main_array

	speed_value = 0
	if speed.get()>1:
		speed_value = (int(speed.get())-2)*10

	high_byte = '0'
	low_byte = '0'

	speed_in_hex = hex(speed_value)
	a = speed_in_hex[2:]
	length = len(a)
	if length == 1:
		low_byte = '0'+a
	elif length == 2:
		low_byte = a
	elif length == 3:
		low_byte = a[1:]
		high_byte = '0'+a[0]
	else:
		low_byte = a[1:]
		high_byte = a[0:2]

	#print(low_byte)
	#print(int(low_byte,16))
	main_array[0][2] = int(high_byte,16)
	main_array[0][3] = int(low_byte,16)


	#engine Temperature
	temp_value = temp.get()
	temp_dec_value = int(mapFromTo(temp_value,-40,200,0,254))
	main_array[0][4] = temp_dec_value





def can_continous_send():
	global main_array, can_on
	timer_1 = 0
	while(can_on):
		time.sleep(0.01)
		timer_1 = timer_1 + 10
		check_change_speed()
		for i in main_array:
			if(timer_1%i[0] == 0):
				msg = can.Message(arbitration_id = i[1],
				is_extended_id = False,
				data = i[2:9]
				)
				#print(msg)
				bus.send(msg)

		if timer_1 == 100:
			timer_1 = 0


if __name__ == "__main__":




	eco_label = Label(root,text = "ECO", font=('Arial', 20) )
	eco_label.place(x=10,y=12)
	eco_switch = Button(root,image = eco_image,command = change_eco)
	eco_switch.place(x = 90, y= 10)
	pwr_label = Label(root, text = "POWER", font = ('Arial',20))
	pwr_label.place(x=200,y=12)


	mil_label = Label(root,text = "MIL", font = ('Arial',20))
	mil_label.place(x=10,y=72)
	mil_switch = Button(root, image = off, command = change_mil)
	mil_switch.place(x=90, y=70)


	speed = tk.DoubleVar()
	speed_label = Label(root,text = "SPEED", font = ('Arial',20))
	speed_label.place(x=10,y=140)
	speed_scale = Scale(root,variable = speed,length=300,
					 from_ = 1, to = 150,orient = HORIZONTAL )
	speed_scale.place(x=130,y=130)

	temp = tk.DoubleVar()
	temp.set(30)
	temp_label = Label(root,text = "TEMP", font = ('Arial',20))
	temp_label.place(x=10,y=180)
	temp_scale = Scale(root,variable = temp,length=300,
					 from_ = -40, to = 200,orient = HORIZONTAL )
	temp_scale.place(x=130,y=180)


	threading.Thread(target = can_continous_send).start()

	root.mainloop()