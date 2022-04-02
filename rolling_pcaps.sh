#!/bin/bash

# this stupid script just grabs a full pcap every 15 seconds and deletes out pcaps that are greater than a day old...
# it will take up gigs of HD space...so...know that

while :
    do
        for i in {1..240}
            do echo $i ;
            tcpdump -i enp2s0 -G 15 -W 1 -s0 -w $(date --date='-1 hour' +\%Y-\%m-\%d-\%s).pcap ;
        done;
        find . -name \*.pcap -type f -mtime 1 -delete;
    done


