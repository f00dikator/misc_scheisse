#no clue if this works, wrote this from the disassembly posted by sandflysecurity.com
# {john.lampe|dmitry.chan}@gmail.com

include("network_func.inc");
  
# bpf filter
pfilter = string("udp and (src ", get_host_ip(), ") and (dst ", this_host(), ")");

ip_id = raw_string(rand() % 255, rand() % 255);

# 2 bytes magic byte
# 2 bytes padding
# 4 bytes IP addr
# 2 bytes port/padding
data = raw_string(0x72, 0x55, 0, 0, 98, 18, 129, 13, 0, 0);

ip = forge_ip_packet(   ip_v : 4,
                        ip_hl : 5,
                        ip_tos : 0,
                        ip_len : 20,
                        ip_id : ip_id,
                        ip_p : IPPROTO_ICMP,
                        ip_ttl : 32,
                        ip_off : 0,
                        ip_src : this_host());

bpfdoor = forge_icmp_packet(ip:ip, icmp_type:8, icmp_code:0, icmp_seq:64, icmp_id:64, data:data);

result = send_packet(bpfdoor, pcap_active:TRUE, pcap_filter:pfilter, pcap_timeout:3);
# if it's infected, it should send a udp packet with data set to "1"

if (result)
{
    display("Got a result\n");
    exit(0);
} else {
    display("No results\n");
}
