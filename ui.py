from core import get_my_ip, update_emulation_engine, init_iptables
from flask import Flask, send_from_directory, request
import json

app = Flask(__name__)

params = {
    'ip': get_my_ip(),
    'latency': '0',
    'jitter': '0',
    'dist': 'normal',
    'rate': '',
    'loss_model': 'random',
    'loss': '0',
    'P': 0, 'E_B': 10, 'rho': 0.99, 'P_isol': 0, 'E_GB': 60,
}

@app.route('/')
def index():
    return send_from_directory('.', 'ui.html')

@app.route('/<path:path>')
def static_(path):
    return send_from_directory('.', path)

@app.route('/params', methods=['GET','POST'])
def params_():
    global params
    if request.method == 'GET':
        return params
    else:
        params = json.loads(request.data)
        update_emulation_engine(params)
        return 'Good'

if __name__ == '__main__':
    init_iptables()
    print(f'\nEmulator IP: {params["ip"]}\nDashboard: http://{params["ip"]}:90/\n')
    app.run(host="0.0.0.0", port=90)
    