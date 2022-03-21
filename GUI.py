import tkinter as tk
from tkinter import Button, Label
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#Ignition Inital Setup
ign_pin = 17
gpio.setup(ign_pin,gpio.OUT)
gpio.output(ign_pin,gpio.HIGH)
switch_on = True

root = tk.Tk()

if __name__ =="__main__":
    
    #root.geometry("700x700")
    root.attributes('-zoomed',True)
    
    ign_label = Label(root, text = "Ignition Status", font=("Arial", 20))
    ign_label.place(x=10,y=30)
    
    ign_switch = Button(root, )
    
    
    
    
    
    root.mainloop()
    