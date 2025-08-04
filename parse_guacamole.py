import subprocess
import binascii
import csv
import sys
import pdb

PCAP_FILE = "guac_decrypted.pcap"
TSHARK_FIELDS = ["frame.number", "ip.src", "ip.dst", "tcp.payload"]
TSHARK_FILTER = "websocket"

def run_tshark(pcap_file):
    cmd = [
        "tshark", "-r", pcap_file,
        "-Y", TSHARK_FILTER,
        "-T", "fields"
    ]
    for field in TSHARK_FIELDS:
        cmd += ["-e", field]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"TShark failed: {result.stderr}")
    return result.stdout.strip().splitlines()

def parse_guac_message(raw_msg):
    tokens = []
    i = 0
    parts = raw_msg.split(';')
    while i < len(parts) - 1:
        try:
            length = int(parts[i])
            token = parts[i + 1][:length]
            tokens.append(token)
            i += 2
        except ValueError:
            break
    return tokens

def decode_payload(hex_payload):
    try:
        raw_bytes = binascii.unhexlify(hex_payload.replace(':', ''))
        decoded = raw_bytes.decode('utf-8', errors='replace')
        return parse_guac_message(decoded)
    except Exception as e:
        return [f"Error decoding: {e}"]

def process_frames(lines):
    decoded_frames = []
    for line in lines:
        fields = line.split('\t')
        if len(fields) != len(TSHARK_FIELDS):
            continue
        frame_num, ip_src, ip_dst, hex_payload = fields
        tokens = decode_payload(hex_payload)
        decoded_frames.append({
            "frame": frame_num,
            "src": ip_src,
            "dst": ip_dst,
            "tokens": tokens
        })
    return decoded_frames

def save_to_csv(decoded_frames, output_file="guac_tokens.csv"):
    with open(output_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Frame", "Source IP", "Destination IP", "Tokens"])
        for frame in decoded_frames:
            writer.writerow([
                frame["frame"],
                frame["src"],
                frame["dst"],
                "|".join(frame["tokens"])
            ])

def main():
    PCAP_FILE = sys.argv[1]
    print(f"Running TShark on {PCAP_FILE}...")
    lines = run_tshark(PCAP_FILE)
    print(f"Processing {len(lines)} frames...")
    decoded = process_frames(lines)
    save_to_csv(decoded)
    print(f"Saved decoded tokens to guac_tokens.csv")

if __name__ == "__main__":
    main()
