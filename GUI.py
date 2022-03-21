import tkinter as tk
from tkinter import Button, Label,PhotoImage
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#Ignition Inital Setup
ign_pin = 17
gpio.setup(ign_pin,gpio.OUT)
gpio.output(ign_pin,gpio.HIGH)
ign_switch_on = True

root = tk.Tk()
on = PhotoImage(file = "on.png")
off = PhotoImage(file = "off.png")

def ign_switch_pressed():
    
    global ign_switch, ign_switch_on
    
    if ign_switch_on:
        ign_switch.configure(image = on)
        ign_switch_on = False
        gpio.output(ign_pin, gpio.LOW)
    else:
        ign_switch.configure(image = off)
        ign_switch_on = True
        gpio.output(ign_pin, gpio.HIGH) 
    
    

if __name__ =="__main__":
    
    #root.geometry("700x700")
    root.attributes('-zoomed',True)
    
    ign_label = Label(root, text = "Ignition Status", font=("Arial", 20))
    ign_label.place(x=10,y=30)
    
    ign_switch = Button(root, image = off, command = ign_switch_pressed)
    ign_switch.place(x=200, y = 20)
    
    
    
    
    
    root.mainloop()
    