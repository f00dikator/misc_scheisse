import requests
import json
import logging
import time
import pdb

class urlscan_client:
    def __init__(self, api_key, visibility="public", verify=True):
        self.init_base_url = "https://urlscan.io/api/v1/scan/"
        # https://urlscan.io/api/v1/result/$uuid/
        self.results_base_url = "https://urlscan.io/api/v1/result/"
        self.session = requests.Session()
        self.session.verify = verify
        self.visibility = visibility
        self.known = {}
        if api_key:
            self.api_key = api_key
            self.session.headers = {'API-Key': self.api_key, 'Content-Type': 'application/json'}
        else:
            logging.info("Error. No API Key presented. Exiting")
            exit(0)

    def init_scan(self, url):
        ret = {}
        try:
            return self.known['url']
        except:
            logging.info('New URL submitted to urlscan. Evaluating {}'.format(url))

        if url:
            data = {"url": url, "visibility": self.visibility}
            logging.info("Requesting urlscan intel for {}".format(url))
            try:
                response = self.session.post(self.init_base_url, data=json.dumps(data)).json()
                if response:
                    logging.info("Retrieved Urlscan UUID of {}".format(response['uuid']))
                    intel = self.wait_for_results(response['uuid'])
                    self.known['url'] = intel
                    return intel
            except Exception as e:
                #pdb.set_trace()
                logging.error("Failed to initialize scan. Error: {}".format(e))
                
        return ret

    def wait_for_results(self, uuid):
        #https://urlscan.io/api/v1/result/$uuid/
        ret = {}

        sleep_counter = 0
        while sleep_counter < 120:
            try:
                req = "{}{}".format(self.results_base_url, uuid)
                logging.info("Requesting {}".format(req))
                response = self.session.get(req)
                #pdb.set_trace()
                if response.status_code == 200:
                    return response.json()
                else:
                    logging.info("response to results returned {}".format(response.status_code))
                    time.sleep(5)
                    sleep_counter += 5
                if response.status_code == 429:
                    logging.error("You are out of API credits. No results to be had")
                    return ret
            except Exception as e:
                logging.error("Failed to retrieve results for uuid {}. Error: {}".format(uuid, e))
                         
        logging.error("Failed to retrieve results for uuid {} within 30 seconds".format(uuid))
        return ret
