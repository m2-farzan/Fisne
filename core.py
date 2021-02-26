import subprocess
import re

def get_my_ip():
    response = subprocess.Popen(['ip', 'addr', 'show'],
        stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    ips = re.findall(r'172\.\d+\.\d+\.\d+', response)
    return ips[0]

def update_emulation_engine(params):
    subprocess.run(
        f'tc qdisc replace dev eth0 root netem latency {params["latency"]}ms',
        shell=True
    )

def init_iptables():
    my_ip = get_my_ip()
    host_ip = re.sub(r'\d+$', '1', my_ip)
    subprocess.run(
        f'iptables -t nat -A PREROUTING -p tcp --dport 90 -j RETURN',
        shell=True
    )
    subprocess.run(
        f'iptables -t nat -A PREROUTING -d {my_ip}/32 -j DNAT --to-destination {host_ip}',
        shell=True
    )
    subprocess.run(
        f'iptables -t nat -A POSTROUTING -s {host_ip}/32 -j SNAT --to-source {my_ip}',
        shell=True
    )