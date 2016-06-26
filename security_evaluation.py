"""
Security evaluation:

Rating security based on the rules provided!
"""

import time
import adb_manager

class rule_check:

    __slots__ = "adb", "LOW_SEC", "MEDIUM_SEC", "HIGH_SEC"

    def __init__(self):
        self.LOW_SEC = 1/3
        self.MEDIUM_SEC = 2/3
        self.HIGH_SEC = 3/3
        self.adb = adb_manager.adb()
        self.execute_rules()


    def execute_rules(self):
        """
        - Check if USB debugging is enabled
        - Check if the phone is rooted
        - If phone was locked check passcode strength
        """
        self.check_usb_debugging()
	
    def check_usb_debugging(self):
	print "\nChecking if USB Debugging is enabled:"
        print "\nPlease disconnect other devices which are not included in security evaluation!"

        #Wait for 10 secs
        print "Waiting for 10 secs:"
        time.sleep(10)
        
        if self.adb.get_devices() == []:
            print "\nusb debugging not enabled: Highly security"
        else:
            print "\nusb debugging enabled: Medium Security"

        
    def check_rooted_android():
        """
        Check if the phone is rooted. 
        And adds updates security effect
        """
        if self.adb.check_root_premission():
            print "Andriod phone is rooted: low security"
        else:
            print "Android phone not rooted: high security"


    def check_phone_locked():
        pass

if __name__ == "__main__":
    rule_verify = rule_check()
    #rule_verify.check_rooted_android()
