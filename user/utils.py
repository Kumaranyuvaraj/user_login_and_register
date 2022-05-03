from email import message
from http import client
import os
from twilio.rest import Client


account_sid = 'AC54ccd06aeff24927d82ade4e017d1b64'
auth_token = 'f5de8d34639f6cca31b13bc433ab845d'

client = Client(account_sid,auth_token)

def send_sms(user_code,phone_number):
    message = client.messages.create(body=f'Hi! Your user and verification code is {user_code}',from_='+19032731757',to=f'{phone_number}')
    print(message.sid)