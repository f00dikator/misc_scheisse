from tenable.io import TenableIO
import requests
import json

# FILL IN
a_key = ''
s_key = ''

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-apikeys" : "accessKey={};secretKey={}".format(a_key, s_key)
}


pdata = {}
pdata['query'] = {}
pdata['query']['or'] = []


counter = 0
#Ensure our keys are good
tio = TenableIO(access_key=a_key,
                secret_key=s_key)

if not tio:
    print("T.io Keys are no bueno. Fix")
    exit(0)

file = open('UUIDs.txt', 'r')

for line in file:
    pdata['query']['or'].append({"field": "host.id", "operator": "eq", "value": '{}'.format(line.strip())})
    counter += 1
    if (counter % 512) == 0:
        print("{}\n".format(counter))
        results = requests.request(method='POST', url="https://cloud.tenable.com/api/v2/assets/bulk-jobs/delete", headers=headers, data=json.dumps(pdata))
        if results.status_code == 202:
            print("Deleted chunk {}-{}".format(counter, counter-512))
        else:
            print("Error deleting chunk {}-{}".format(counter, counter-512))
        pdata['query']['or'] = []

results = requests.request(method='POST', url="https://cloud.tenable.com/api/v2/assets/bulk-jobs/delete", headers=headers, data=json.dumps(pdata))

