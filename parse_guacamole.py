from scapy.all import rdpcap, TCP
import struct
import sys

def parse_websocket_frame(data):
    messages = []
    i = 0
    while i < len(data):
        if len(data) < i + 2:
            break

        byte1, byte2 = data[i], data[i+1]
        fin = byte1 >> 7
        opcode = byte1 & 0x0F
        masked = byte2 >> 7
        payload_len = byte2 & 0x7F
        i += 2

        if payload_len == 126:
            if len(data) < i + 2:
                break
            payload_len = struct.unpack(">H", data[i:i+2])[0]
            i += 2
        elif payload_len == 127:
            if len(data) < i + 8:
                break
            payload_len = struct.unpack(">Q", data[i:i+8])[0]
            i += 8

        if masked:
            if len(data) < i + 4:
                break
            masking_key = data[i:i+4]
            i += 4
        else:
            masking_key = None

        if len(data) < i + payload_len:
            break

        payload = bytearray(data[i:i+payload_len])
        i += payload_len

        if masked:
            for j in range(payload_len):
                payload[j] ^= masking_key[j % 4]

        if opcode == 0x1:  # text frame
            try:
                messages.append(payload.decode("utf-8"))
            except UnicodeDecodeError:
                pass  # ignore invalid UTF-8
    return messages

def extract_websocket_messages(pcap_file):
    packets = rdpcap(pcap_file)
    tcp_streams = {}

    for pkt in packets:
        if TCP in pkt:
            ip = pkt[IP].src, pkt[IP].dst
            ports = pkt[TCP].sport, pkt[TCP].dport
            stream_id = (ip, ports)
            payload = bytes(pkt[TCP].payload)
            if len(payload) > 0:
                if stream_id not in tcp_streams:
                    tcp_streams[stream_id] = b""
                tcp_streams[stream_id] += payload

    for stream_id, data in tcp_streams.items():
        print(f"\n--- Messages from stream {stream_id} ---")
        messages = parse_websocket_frame(data)
        for msg in messages:
            print(msg)

# Replace with your actual PCAP path
extract_websocket_messages(sys.argv[1])
