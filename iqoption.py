import sys
from dotenv import load_dotenv
import os

from iqoptionapi.stable_api import IQ_Option

load_dotenv()


class Iq:
    def __init__(self) -> bool:
        self.iq = IQ_Option(os.getenv("USER"), os.getenv("PASSWD"))
        check, reason = self.iq.connect()
        if check:
            self.iq.change_balance("PRACTICE")

        else:
            sys.exit()

    def balance(self):
        return self.iq.get_balance()

    def type_balance(self):
        return self.iq.get_balance_mode()
