import tkinter as tk
from tkinter import Button, Label,PhotoImage, Frame
from picamera import PiCamera
import RPi.GPIO as gpio

import threading, time
from picamera.array import PiRGBArray
from PIL import Image, ImageTk
import io

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#Ignition Inital Setup
ign_pin = 17
gpio.setup(ign_pin,gpio.OUT)
gpio.output(ign_pin,gpio.HIGH)
ign_switch_on = True

#Fuel Sensor pin
fuel_pin = 22
gpio.setup(fuel_pin,gpio.OUT)
gpio.output(fuel_pin,gpio.HIGH)
fuel_switch_on = True


root = tk.Tk()
on = PhotoImage(file = "on.png")
off = PhotoImage(file = "off.png")
white = PhotoImage(file = "on.png",)

#Camera
camera = PiCamera()
camera_on = True
seperate_camera_on = True
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

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

def fuel_switch_pressed():

    global fuel_switch, fuel_switch_on

    if fuel_switch_on:
        fuel_switch.configure(image = on)
        fuel_switch_on = False
        gpio.output(fuel_pin, gpio.LOW)
    else:
        fuel_switch.configure(image = off)
        fuel_switch_on = True
        gpio.output(fuel_pin, gpio.HIGH)

def thread_for_image():
    global camera_on, image_frame
    j = "a0"
    stream = io.BytesIO()

    while not camera_on:
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        image = Image.open(stream)
        image2 = ImageTk.PhotoImage(image)
        image_frame.config(image = image2)
        time.sleep(0.3)
        stream.seek(0)
        stream.truncate(0)

    """
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = Image.fromarray(frame.array)
        image2 = ImageTk.PhotoImage(image)
    # show the frame
        image_frame.config(image = image2)
    # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
        if not camera_on:
            break
        """
def seperate_camera_switch():

    global seperate_camera_on, seperate_camera_button

    if seperate_camera_on:
        camera.start_preview(fullscreen=False, window = (680, 280, 640, 480))
        seperate_camera_button.config(text = " Stop Seperate Camera")
        seperate_camera_on = False
    else:
        camera.stop_preview()
        seperate_camera_on = True
        seperate_camera_button.config(text = "Start Seperate Camera")



def camera_switch():
    global camera_button, camera_on

    if camera_on:
        camera_on = False
        camera_button.config(text = "Stop Camera")
        #camera.start_preview()
        threading.Thread(target = thread_for_image).start()
        #time.sleep(10)
        #camera.stop_preview

    else:
        camera_on = True
        #camera.stop_preview()
        camera_button.config(text = "Start Camera")

if __name__ =="__main__":

    #root.geometry("700x700")
    root.attributes('-zoomed',True)

    ign_label = Label(root, text = "Ignition Status", font=("Arial", 20))
    ign_label.place(x=10,y=30)

    ign_switch = Button(root, image = off, command = ign_switch_pressed)
    ign_switch.place(x=200, y = 20)

	fuel_label = Label(root, text = "Fuel switch", font=("Arial", 20))
    fuel_label.place(x=10,y=60)

    fuel_switch = Button(root, image = off, command = fuel_switch_pressed)
    fuel_switch.place(x=200, y = 50)

    camera_button  =Button (root, text = "Start Camera", font=("Arial", 20),command = camera_switch)
    camera_button.place(x= 10, y= 150)
    seperate_camera_button  =Button (root, text = "Start Camera Seperately", font=("Arial", 20),command = seperate_camera_switch)
    seperate_camera_button.place(x= 200, y= 150)



    root.mainloop()
