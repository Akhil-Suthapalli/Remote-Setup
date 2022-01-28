from picamera import PiCamera
import time
a = PiCamera()

a.start_preview()
time.sleep(10)
a.stop_preview()