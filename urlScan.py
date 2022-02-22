import requests
import json
import logging
import time

class urlscan_client:
    def __init__(self, api_key, visibility="public", verify=False):
        self.init_base_url = "https://urlscan.io/api/v1/scan/"
        self.results_base_url = "https://urlscan.io/api/v1/result/"
        self.session = requests.Session()
        self.session.verify = verify
        self.visibility=visibility
        if api_key:
            self.api_key = api_key
            self.session.headers = {'API-Key': self.api_key, 'Content-Type': 'application/json'}
        else:
            logging.info("Error. No API Key presented. Exiting")
            exit(0)

    def init_scan(self, url):
        ret = {}
        if url:
            data = {"url": url, "visibility": self.visibility}
            try:
                response = self.session.post(self.init_base_url, data=json.dumps(data)).json()
                if response:
                    return self.wait_for_results(response['uuid'])
            except Exception as e:
                logging.error("Failed to initialize scan. Error: {}".format(e))
                
        return ret

    def wait_for_results(self, uuid):
        ret = {}

        sleep_counter = 0
        while sleep_counter < 30:
            try:
                response = self.session.get(self.results_base_url)
                if response.status_code == "200":
                    return response.json()
                else:
                    time.sleep(5)
                    sleep_counter += 5
            except Exception as e:
                logging.error("Failed to retrieve results for uuid {}. Error: {}".format(uuid, e))
                         
        logging.error("Failed to retrieve results for uuid {} within 30 seconds".format(uuid))
        return ret
