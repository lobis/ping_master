from flask import Flask
from flask import render_template
from flask_sockets import Sockets

import time
import json

from ping import hosts_get, ping_host

app = Flask(__name__)
sockets = Sockets(app)

hosts = []
with open('hosts') as f:
    for line in f:
        hosts.append([x for x in line.split()])

@app.route('/')
def main():
    #return render_template('pingman.html', ping=ping, hosts=hosts)
    return render_template("socket.html", hosts=hosts)

@sockets.route('/echo')
def echo_socket(ws):
    hosts = hosts_get("hosts")
    while True:
        results_ping = {}
        for host in hosts:
            results_ping[host] = ping_host(host)
            #print ping_host('192.168.0.1')
        #print(results_ping)
        data_json = json.dumps(results_ping)
        print data_json
        ws.send(data_json)
        time.sleep(1)
        #print("sending...")


if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
