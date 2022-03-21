
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import tkinter as tk
import numpy as np
from PIL import Image
from PIL import ImageTk
from threading import Thread
 
 
canvas = tk.Tk()
canvas.geometry("800x600")
b = tk.Label(canvas)
b.pack() 
 
def TAKEFOTO():
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(320, 240))
  
# allow the camera to warmup
    time.sleep(0.1)
 
# capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
 
        (width,height,other) = image.shape
     
 
     
        value = image.item(100,100,0)
    for x in range (0,width):
        if(image.item(x,100,0) < 10):
            cv2.rectangle(image,(x,height-100),(0,20),(255,255,255),2)
            break;
         
         
    print(value)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    b.image = image
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
 
 
 
#canvas.pack()
 
canvas.mainloop()
     
t = Thread (target=TAKEFOTO)
t.start()