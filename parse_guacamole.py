import pyshark

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

def extract_guac_websocket(pcap_file):
    cap = pyshark.FileCapture(pcap_file, display_filter='websocket')

    for pkt in cap:
        try:
            ws_layer = pkt['websocket']
            payload = ws_layer.get_field_value('data')
            if payload:
                decoded = bytes.fromhex(payload).decode('utf-8', errors='replace')
                tokens = parse_guac_message(decoded)
                print(f"[Guacamole] Tokens: {tokens}")
        except Exception as e:
            print(f"Error: {e}")

# Run the parser
extract_guac_websocket('guac_decrypted.pcap')
