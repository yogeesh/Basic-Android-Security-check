import subprocess

class adb:

    __slots__ = "selected_device"


    def __init__(self):
        if not self.check_adb_installed():
            print "\nPlease install \"Android Debug Bridge\"(ADB) " + \
                            "to proceed further."
            return 
        else:
            print "\nAndroid Debug Bridge is active!\n"

    
    def _start(self):
        """
        1. Check ADB installed.
        2. Get devices and status
        3. Choose device:
           Single device - Automatic
           Multiple device - Manual
        """

        devices = self.get_devices()
        
        if devices == []:
            print "Connect your android device/phone to the computer" + \
                     "and turn ON developer mode on the device"
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
        
        self.selected_device = self.selected_device[0]

        #print self.check_root_premission()
        
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
        try:
            cmd = subprocess.Popen(["adb", "devices"], stdout=subprocess.PIPE)
            output, error = cmd.communicate()
        except:
            print "Seems like ADB is not working properly! recheck 'adb devices' manually."
            return []
            
        #Process the output for getting devices
        devices = list()
        for output_line in output.split('\n'):
            if output_line.startswith("*") or output_line.startswith("List") \
                    or output_line == "":
                continue
            else:
                devices.append(output_line.split())
        
        return devices



    def run_commnad(self, command, shell=True):
        """
        commnad: adb shell command, takes as a string
        shell: Tells if it is a shell command or not
        returns: the output of the command
        """
        adb_command = ["adb", "-s", self.selected_device]
        if shell: adb_command.append("shell")
        adb_command += command.split()

        try:
            cmd = subprocess.Popen(adb_command, stdout=subprocess.PIPE)
            output, error = cmd.communicate()
        except Exception as e:
            print "Something super weird, please contact developer " + \
                "with the log: %s\n"%e
            return False
            
        if error == "":
            return False, error
        return True, output
    

    def check_root_premission(self):
        status, output = self.run_commnad("su")
        if "not found" in output:
            return False
        return True
            

    def check_phone_passcode_enabled():
        """
        Check if the passcode is enabled:
        1. PIN lock
        2. Pattern lock
        3. Swipe lock
        4. None, No lock!
        """
        pass
        
        
if __name__ == "__main__":
    adb()._start()
    print "\nThanks!!!\n"
