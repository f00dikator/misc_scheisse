# -*- coding: utf-8 -*-
# This script is Copyright (C) 2020 Tenable Inc.

__author__ = 'John Lampe'
__version__ = '1.0.0'


class ipv4_network:
    def __init__(self):
        self.ip_mapped = []
        self.dupe_msg = "This IP has already been evaluated"


    def ip_in_cidr(self, ip, cidr):
        net, mask = cidr.split('/')
        if not self.is_mapped(ip):
            ip_integer = self.ip_to_num(ip)
            cidr_integer = self.ip_to_num(net)

            if ip_integer >> (32-int(mask)) == cidr_integer >> (32-int(mask)):
                return True
            else:
                return False
        else:
            return self.dupe_msg

    def ip_to_num(self, ip):
        sum = 0
        octets = ip.split('.')
        i = 3
        for oct in octets:
            if i > 0:
                sum += int(oct) * (256**i)
            else:
                sum += int(oct)
            i -= 1
        return sum

    def ip_in_range(self, ip, ip_range):
        if not self.is_mapped(ip):
            ip = self.ip_to_num(ip)
            start, finish = ip_range.split('-')
            start = self.ip_to_num(start)
            finish = self.ip_to_num(finish)
            if start <= ip <= finish:
                return True
            else:
                return False
        else:
            return self.dupe_msg

    def ip_in_list(self, ip, ip_list):
        if not self.is_mapped(ip):
            if ip in ip_list:
                return True
            else:
                return False
        else:
            return self.dupe_msg

    def is_mapped(self, ip):
        if ip in self.ip_mapped:
            return True
        else:
            self.ip_mapped.append(ip)
            return False


