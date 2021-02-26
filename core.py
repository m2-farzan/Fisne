import subprocess
import re

def get_my_ip():
    response = subprocess.Popen(['ip', 'addr', 'show'],
        stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    ips = re.findall(r'10\.\d+\.\d+\.\d+', response)
    return ips[0]

def update_emulation_engine(params):
    if params['loss_model'] == 'random':
        loss_cmd = '' if params["loss"] == '0' else f'loss random {params["loss"]}'
    elif params['loss_model'] == 'gi':
        P = float(params['P'])
        E_B = float(params['E_B'])
        rho = float(params['rho'])
        P_isol = float(params['P_isol'])
        E_GB = float(params['E_GB'])
        p31 = 100 * 1 / (E_B * rho)
        p13 = 100 * (P - P_isol)/(E_B * (1 - P_isol) * (rho - P))
        p23 = 100 * 1 / (E_GB)
        p32 = 100 * (1 - rho) / (rho * E_GB)
        p14 = 100 * P_isol / (1 - P_isol)
        loss_cmd = f'loss state {p13} {p31} {p32} {p23} {p14}'
    cmd = [
        'tc qdisc replace dev eth0 root netem',
        f'delay {params["latency"]}ms',
        '' if params["jitter"] == '0' else f'{params["jitter"]}ms distribution {params["dist"]}',
        loss_cmd,
        '' if params["rate"] == '' else f'rate {params["rate"]}kbit'
    ]
    subprocess.run(' '.join(cmd), shell=True)

def init_iptables():
    my_ip = get_my_ip()
    host_ip = re.sub(r'\d+$', '2', my_ip)
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
