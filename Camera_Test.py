from picamera import PiCamera

import time

cam = PiCamera()
cam.resolution = (640, 480)
cam.start_preview()
time.sleep(10)
cam.stop_preview()