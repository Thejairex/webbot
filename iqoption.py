from iqoptionapi.stable_api import IQ_Option
import sys


class Iq:
    def __init__(self) -> bool:
        self.iq = IQ_Option("yairjesus777@gmail.com","Aiwa_2015")
        check, reason = self.iq.connect()
        if check:
            self.iq.change_balance("PRACTICE")
                    
        else:
            sys.exit()

    def balance(self):
        return self.iq.get_balance()

    def type_balance(self):
        return self.iq.get_balance_mode()