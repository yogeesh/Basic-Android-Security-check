"""
Security evaluation:

Rating security based on the rules provided!
"""

import time
import datetime
import adb_manager


class rule_check:

    __slots__ = "adb", "LOW_SEC", "MEDIUM_SEC", "HIGH_SEC",\
                "security_level_monitor"
    
    def __init__(self):
        self.LOW_SEC = 1/3.0 * 100
        self.MEDIUM_SEC = 2/3.0 * 100
        self.HIGH_SEC = 3/3.0 * 100
        self.security_level_monitor = list()
        self.adb = adb_manager.adb()
        self.execute_rules()
        #print self.security_level_monitor

        result = self.eval_security()
        print "\n```````````````````````"
        print "Security level: " + str(result) + "%\n"
        print "\nThanks :)\n\n"
	
        

    def execute_rules(self):
        """
        - Check if USB debugging is enabled
        - Check if the phone is rooted
        - Check if phone is locked
        - If phone was locked check passcode strength
        """
        
        self.check_usb_debugging()
        self.adb._start()
        self.check_app_debug()
        self.check_rooted_android()
        self.check_phone_locked()
        self.check_lock_strength()
        self.check_security_patch()
        
        
    def check_usb_debugging(self):
	print "\nChecking if USB Debugging is enabled:"
        print "\tPlease disconnect other devices which are not included in security evaluation!"

        #Wait for 10 secs
        print "\tWaiting for 10 secs:"
        #time.sleep(10)
        
        if self.adb.get_devices() == []:
            print "\tusb debugging not enabled: Highly security\n"
            self.security_level_monitor.append(self.HIGH_SEC)
        else:
            print "\tusb debugging enabled: Medium Security\n"
            self.security_level_monitor.append(self.MEDIUM_SEC)

        
    def check_rooted_android(self):
        """
        Check if the phone is rooted. 
        And adds updates security effect
        """
        print "\nChecking if the phone is rooted:"
        if self.adb.check_root_premission():
            print "\tAndriod phone is rooted: low security"
            self.security_level_monitor.append(self.LOW_SEC)
        else:
            print "\tAndroid phone not rooted: high security"
            self.security_level_monitor.append(self.HIGH_SEC)

            
    def check_phone_locked(self):
        print "\nChecking if the phone is locked with passcode:"
        self.adb.run_command("input keyevent 26")
        self.adb.run_command("input touchscreen swipe 930 880 930 380")
        print "\tCheck if the screen is locked now and asking for:"
        print "\t1. passcode"
        print "\t2. pattern"
        print "\t3. None, no lock screen."
        for i in range(10):
            pass_type = int(raw_input("choose the type of passcode(1/2/3): "))
            if pass_type <=3 and pass_type >= 1:
                break
        if pass_type < 1 and pass_type > 3: pass_type = 3
        
        if pass_type == 3:
            print "\tAndroid phone lck screen security: low"
            self.security_level_monitor.append(self.LOW_SEC)
        elif pass_type == 2:
            print "\tAndroid phone lock screen security: high"
            self.security_level_monitor.append(self.HIGH_SEC)
        else:
            self.security_level_monitor.append(self.HIGH_SEC)
            print "\tAndroid phone lock screen security: high"

    def check_lock_strength(self):
        """
        Logically meant to be called after the function check_phone_locked.
        But it can be called without any depencies also.
        """
        print "\nChecking for passcode strength"
        passcode = raw_input("\tplease enter the passcode(if pattern, tell the number " + \
                                 "0-9(16) considering it has matrix): ")
        #TODO check if the passcode is correct, by unlocking through code!
        #TODO give an example for pattern passcode
        if len(passcode) >= 15:
            print "\tAndroid phone lock screen security: high"
            self.security_level_monitor.append(self.HIGH_SEC)
        elif len(passcode) >= 8:
            print "\tAndroid phone lock screen security: medium"
            self.security_level_monitor.append(self.MEDIUM_SEC)
        else:
            print "\tAndroid phone lock screen security: low"
            self.security_level_monitor.append(self.LOW_SEC)


    def check_security_patch(self):
        """
        Android release security updates/patches on monthly basis.
        There may be more than 1 release of update or patch in month
        but atleast 1 per month
        """
        print "\nChecking security patch upto date or atleast near to latest:"

        curr_month, curr_year = time.strftime("%m/%Y").split("/")
        status, output = self.adb.run_command("getprop ro.build.version.security_patch")
        if status:
            patch_year, patch_month, patch_day = output.split("-")
        else:
            print "Something went wrong! please submit this log to developer:\n", output
            
        if int(curr_year) == int(patch_year):
            diff_month = int(curr_month) - int(patch_month)
        else:
            diff_year = int(curr_year)-int(patch_year)-1
            diff_month = diff_year*12
            if int(curr_year)-1 == int(patch_year):
                diff_month = 0
            diff_month += int(curr_month)
            diff_month += (12 - int(patch_month))
            
        #evaluation of security
        if diff_month <= 2:
            print "\tAndroid almost upto date: high security"
            self.security_level_monitor.append(self.HIGH_SEC)
        elif diff_month <= 6:
            print "\tAndroid was not updated for few months: medium security"
            self.security_level_monitor.append(self.MEDIUM_SEC)
        else:
            print "\tAndroid was not updates for a long time: low security"
            self.security_level_monitor.append(self.LOW_SEC)


    def check_app_debug(self):
        """
        Developers run applications in debug mode while development, but before 
        publishing it to users developers should disbale debug mode. Else all 
        the files related to the application can be acessed by any user.
        """
        print "Checking for applications running in debug mode:"
        status, output = self.adb.run_command("pm list packages")
        if not status:
            print "\tCheck if phone is connected properly and re-run"
            return
        
        output = output.strip().replace("package:", "").split("\n")
        total_app = len(output)
        print "\tDetected %s installed applications", total_app

        app_debuggable = []
        app_debuggable_count = 0
        for app in output:
            print "\tTesting app: %s"%app
            status, output = self.adb.run_command("echo 'pwd' | run-as %s"%app)
            if "data" in output:
                print "\t\tapp debuggable: low security"
                #self.security_level_monitor.append(self.LOW_SEC)
                app_debuggable.append(app)
                app_debuggable_count += 1
            else:
                print "\t\tapp not debuggable: high security"
                #self.security_level_monitor.append(self.HIGH_SEC)
        
        print "\t\nTotal debugge mode enabled applications: %s"%app_debuggable_count
        print "\tApplication with debug mode enabled: "
        for debug_app in app_debuggable:
            print "\t\t%s"%debug_app


        if app_debuggable_count == 0:
            self.security_level_monitor.append(HIGH_SEC)
        elif app_debuggable_count >= total_app*0.1:
            self.security_level_monitor.append(self.MEDIUM_SEC)
        else:
            self.security_level_monitor.append(self.LOW_SEC)
            
            

    def secure_adb(self):
        """
        Checking if adb is running in secure mode.
        If not running in secure mode, phone can be connected to Debug Bridge 
        without acception RSA fingerprint check and adb can be acessed while in boot 
        and in recovery mode/boot.
        """
        #TODO
        pass

        
    def eval_security(self):
        """
        Weighted average of the all the securtity ratings
        """
        weighted_sum = 0
        weighted_total = len(self.security_level_monitor)*100
        for sec_rating in self.security_level_monitor:
            weighted_sum += sec_rating

        return (weighted_sum/weighted_total)*100

    
if __name__ == "__main__":
    rule_verify = rule_check()
    #rule_verify.check_security_patch()
