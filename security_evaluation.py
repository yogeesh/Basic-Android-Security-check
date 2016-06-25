"""
Security evaluation:

Rating security based on the rules provided!
"""

import adb_manager

class rule_check:

    __slots__ == "adb", "LOW_SEC", "MEDIUM_SEC", "HIGH_SEC", \
        ""

    def __init__(self):
        #self.SEC_IMPACT_LOW = 1/3
        #self.SEC_IMPACT_MEDIUM = 2/3
        #self.SEC_IMPACT_HIGH = 3/3
        adb = adb_manager.adb()
        adb._start()

        
    def check_rooted_android():
        """
        Check if the phone is rooted. 
        And adds updates security effect
        """
        if adb.check_root_premission():
            print "Andriod phone is rooted: low security"
        else:
            print "Android phone not rooted: high security"


    def check_phone_locked():
        pass
