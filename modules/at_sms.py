from __future__ import print_function

import africastalking
from dotenv import load_dotenv
import streamlit as st
from os import getenv

load_dotenv()

# AT_API_KEY = getenv("AT_API_KEY")  # for local use
# AT_USERNAME = getenv("AT_USERNAME")
AT_API_KEY = st.secrets["AT_API_KEY"]  # both local and cloud deployment
AT_USERNAME = st.secrets["AT_USERNAME"]


class SMS:
    def __init__(self):
        # Get your app credentials from app.africastalking.com
        self.username = AT_USERNAME
        self.api_key = AT_API_KEY
        africastalking.initialize(self.username, self.api_key)  # Initialize the SDK
        self.sms = africastalking.SMS  # Initialize SMS service

    def send(self, recipients_message, message_recipients, sender=None):
        recipients = message_recipients  # should be a list of phone no.s in +2547xx/+25411xx format
        message = recipients_message  # type str

        # Set your shortCode or senderId
        # sender = "XXYYZZ" #* ...using ATI's default shortcode for one-way SMS
        try:
            # Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(
                message, recipients, sender
            )  # FIXME: Type checker warning: Cannot access member "send" for type "None" \n Member "send" is unknown
            print(response)
        except Exception as e:
            print("Encountered an error while sending: %s" % str(e))


if __name__ == "main":  # fmt: skip
    sms = SMS()  # fmt: skip
    sms.send("Hello, this is a test message", ["+254715987396"])  # fmt: skip
    print(type(AT_API_KEY))  # fmt: skip
    print(type(AT_USERNAME))  # fmt: skip
    print(AT_API_KEY)  # fmt: skip
    print(AT_USERNAME)  # fmt: skip
