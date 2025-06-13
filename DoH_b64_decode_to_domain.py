import base64
import sys
import pdb

def clean_bytes(my_stream):
    fqdn = []
    buf_len = my_stream[0]
    ptr = 1
    while (ptr != 0):
        tmp_nam = my_stream[ptr:ptr+buf_len]
        fqdn.append(tmp_nam)
        if (my_stream[ptr + len(tmp_nam)] == 0):
            return fqdn
        ptr = ptr + len(tmp_nam) + 1
        buf_len = my_stream[ptr-1]

    return fqdn

# when you see traffic to/from a DoH server, it will look like /dns-query?dns=<base64>
# Just cat|awk that field into a single file called DOH.csv and then run this
with open('DOH.csv', 'r') as file:
    for line in file:
        encoded_str = line.strip()
        padding = '=' * (-len(encoded_str) % 4)

        try:
            decoded_bytes = base64.urlsafe_b64decode(encoded_str + padding)
            result = clean_bytes(decoded_bytes[12:])
            print(result)
        except Exception as e:
            result = ""



