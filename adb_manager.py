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
        if not check_adb_installed():
            print "Please install \"Android Debug Bridge\"(ADB) \
                            to proceed further."
        
        devices = get_devices()
        
        if devices == 0:
            print "Connect your android device/phone to the computer\
                     and turn ON developer mode on the device"
            return False
    
        elif devices == 1:
            self.selected_device = devices[0]

        else:
            print "Multiple devices where detected, please choose:"
            for device_num in len(devices):
                print "%s. %s"%(device_num, devices[i])
            self.selected_device = devices[int(raw_input("Choose \
                                                  any device: "))]
        
            
    def check_adb_installed(self):
        """
        Checks if adb is installed and it should added in PATH.
        """



        pass


    def get_devices(self):
        """
        Gets all the devices attached to the host machine.
        """
        devList = self.call("devices")
        return devList


    
if __name__ == "__main__":
    adb()
    print "\n\n\nThanks!!!"
