import subprocess

class adb:

    __slots__ = "selected_device"


    def __init__(self):
        pass

    
    def _start(self):
        """
        1. Check ADB installed.
        2. Get devices and status
        3. Choose device:
           Single device - Automatic
           Multiple device - Manual
        """
        if not self.check_adb_installed():
            print "\nPlease install \"Android Debug Bridge\"(ADB) \
                            to proceed further."
        else:
            print "\nAndroid Debug Bridge is active!\n"


        devices = self.get_devices()
        
        if devices == []:
            print "Connect your android device/phone to the computer\
                     and turn ON developer mode on the device"
            return False
    
        elif len(devices) == 1:
            self.selected_device = devices[0]

        else:
            print "Multiple devices where detected, please choose:"
            
            for device_num in range(len(devices)):
                print_str = "%s. %s %s"%(device_num, devices[device_num][0]\
                                             , devices[device_num][1])
                if not devices[device_num][1].startswith("device"):
                    print_str += " (This device can NOT acessed please check!)"
                print print_str
            self.selected_device = devices[int(raw_input("\nChoose " + \
                                                  "any device: "))]
        if self.selected_device[1] != "device":
            print "ADB can not access the device as the status of the device: %s"%self.selected_device[1]
        else:
            print "Selected Device: %s\n"%self.selected_device[0]
            
    def check_adb_installed(self):
        """
        Checks if adb is installed and it should added in PATH.
        """
        try:
            cmd = subprocess.Popen(["adb"], stdout=subprocess.PIPE\
                                       , stderr=subprocess.PIPE)
            output, error = cmd.communicate()
        except:
            return False

        #Process the output and check if Android Debug Bridge is present
        if error.startswith("Android Debug Bridge"):
            return True
        return False


    def get_devices(self):
        """
        Gets all the devices attached to the host machine.
        """
        cmd = subprocess.Popen(["adb", "devices"], stdout=subprocess.PIPE)
        output, error = cmd.communicate()
        
        #Process the output for getting devices
        devices = list()
        for output_line in output.split('\n'):
            if output_line.startswith("*") or output_line.startswith("List") \
                    or output_line == "":
                continue
            else:
                devices.append(output_line.split())
        
        return devices

    
if __name__ == "__main__":
    adb()._start()
    print "\nThanks!!!\n"
