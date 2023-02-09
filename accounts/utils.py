import requests as req
import re
from django import forms

def email_checker(email):
    status = False
    url = 'https://login.microsoftonline.com/common/GetCredentialType'
    body = '{"Username":"%s"}' % email
    request = req.post(url, data=body)
    response = request.text
    valid = re.search('"IfExistsResult":0,', response)
    if valid:
        status = True
    return status

def validate_email_string(email):
    if re.findall(r'\w+[.]\w', email):
        return True