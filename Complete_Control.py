from uiautomator import Device
import RPi.GPIO as gpio
import subprocess,time

d = Device("9ef1d3f60904")  # Redmi Note 5 Mobile

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

ign_pin = 17
gpio.setup(ign_pin,gpio.OUT)
gpio.output(ign_pin,gpio.HIGH)
ign_switch_on = True


def ign_switch_pressed():
#To toggle between on/off of ignition switch
    global ign_switch, ign_switch_on

    if ign_switch_on:
        ign_switch_on = False
        gpio.output(ign_pin, gpio.LOW)
    else:
        ign_switch_on = True
        gpio.output(ign_pin, gpio.HIGH)
        
        
class Adb():
    
    def __init__(self, device = None):
        self.device = None
        self.device_list = []
        
    def raw_command(self, command):
        p = subprocess.Popen("adb "+command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            res = self.raw_command("-s "+self.device+" "+command)#
            
        return res

    def unlock_device(self):
        #Specific to Redmi Phone (logic can be derived here)
        #For pin kepad touch points can be traced to press for particular model
        self.send_command("shell input keyevent 26")
        time.sleep(1)
        self.send_command("shell input swipe 500 1600 500 200 100")
    
    def tap_at_point(self,x,y):
        self.send_command("shell input tap "+str(int(x))+" "+str(int(y)))
        
    def open_tvs_connect(self):
        self.send_command("shell am start com.tvsm.connect/com.tvsm.connect.SplashActivity")

    def find_pid(self):
        res = self.send_command("shell pidof com.tvsm.connect")
        try:
            pid = res.split()[0]
        except:
            pid = None
        return pid

    def get_current_activity(self):

        res = self.send_command("shell dumpsys activity activities | findstr mResumedActivity")
        result = res.split("\r\n")
        return result[0]

    def _logcat(self, pid):

        p = subprocess.Popen(self.adb+" logcat | findstr " + str(pid), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p
    
    def clear_apps(self):
        
        self.send_command("shell input keyevent KEYCODE_APP_SWITCH")
        time.sleep(2)
        self.send_command("shell input keyevent DEL")
    
    def kill_tvs_app(self):
        
        self.send_command("shell am force-stop com.tvsm.connect")


def main_loop():
    
    adb_obj.unlock_device()
    time.sleep(2)
    #Unlock Device and wait for 2 seconds
    
    #clear all recent apps
    adb_obj.kill_tvs_app()
    
    
    
    
adb_obj = Adb()
main_loop()
