# interact with circl

import requests
import pdb
import logging
import json
import time
import base64
import string

class Circl:
    def __init__(self, uid=None, key=None, verify=True):

        if not uid or not key:
            logging.error("No UID or Key presented to class. Check your yaml config. Exiting")
            exit(0)

        self.token = base64.b64encode(f"{uid}:{key}".encode('utf-8')).decode("ascii")
        self.pdns_url = "https://www.circl.lu/pdns/query/"
        self.ssl_url = "https://www.circl.lu/v2pssl/query/"
        self.ssl_cert_fetch_url = 'https://www.circl.lu/v2pssl/cfetch/'
        self.ssl_cert_query_url = 'https://www.circl.lu/v2pssl/cquery/'
        self.previous_requests = []

        try:
            self.session = requests.Session()
            self.session.verify = verify
            self.session.headers = {"Accept": "application/json",
                                    "Authorization": "Basic {}".format(self.token),
                                    "User-Agent" : "JohnLampeCirclClient"}

            self.generic_session = requests.Session()
            self.generic_session.verify = verify
            self.generic_session.headers = {"Accept": "*/*"}

        except Exception as e:
            logging.error("Failed to create session. Error: {}".format(e))
            print("Failed to create session. Error: {}".format(e))
            exit(0)


    def query_pdns(self, fqdn):
        if not fqdn:
            logging.error("Failed to supply a fqdn. Returning NULL")
            return None

        try:
            query = "{}{}".format(self.pdns_url, fqdn)
            if self.find_dupe(query):
                return "Query has already been executed"
            ret = self.session.get(query)

            if ret.text:
                return ret.text
            else:
                return "No Result"
        except Exception as e:
            logging.error("Failed to fetch results. Error: {}".format(e))

    def query_ssl_ip(self, ip):
        if not ip:
            logging.error("Failed to supply a fqdn. Returning NULL")
            return None

        try:
            query = "{}{}".format(self.ssl_url, ip)
            if self.find_dupe(query):
                return "Query has already been executed"
            ret = self.session.get(query)

            if ret.text:
                return ret.text
            else:
                return "No Result"
        except Exception as e:
            logging.error("Failed to fetch results. Error: {}".format(e))

    def query_ssl_cidr(self, ip_block):
        if not ip_block:
            logging.error("Failed to supply a fqdn. Returning NULL")
            return None

        try:
            query = "{}{}".format(self.ssl_url, ip_block)
            if self.find_dupe(query):
                return "Query has already been executed"
            ret = self.session.get(query)

            if ret.text:
                return ret.text
            else:
                return "No Result"
        except Exception as e:
            logging.error("Failed to fetch results. Error: {}".format(e))

    def certificate_fetch(self, sha_hash):
        if not sha_hash:
            logging.error("Failed to supply a sha256 hash. Returning NULL")
            return None

        try:
            query = "{}{}".format(self.ssl_cert_fetch_url, sha_hash)
            if self.find_dupe(query):
                return "Query has already been executed"
            ret = self.session.get(query)

            if ret.text:
                return ret.text
            else:
                return "No Result"
        except Exception as e:
            logging.error("Failed to fetch results. Error: {}".format(e))

    def certificate_query(self, sha_hash):
        if not sha_hash:
            logging.error("Failed to supply a sha256 hash. Returning NULL")
            return None

        try:
            query = "{}{}".format(self.ssl_cert_query_url, sha_hash)
            if self.find_dupe(query):
                return "Query has already been executed"
            ret = self.session.get(query)

            if ret.text:
                return ret.text
            else:
                return "No Result"
        except Exception as e:
            logging.error("Failed to fetch results. Error: {}".format(e))

    def find_dupe(self, query):
        if query in self.previous_requests:
            return True
        else:
            self.previous_requests.append(query)
            return False
