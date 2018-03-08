from flask import Flask
from flask import render_template
from flask_sockets import Sockets

import time

app = Flask(__name__)
sockets = Sockets(app)

hosts = []
with open('hosts') as f:
    for line in f:
        hosts.append([x for x in line.split()])

@app.route('/')
def main():
    #return render_template('pingman.html', ping=ping, hosts=hosts)
    return render_template("socket.html")

@sockets.route('/echo')
def echo_socket(ws):
    while True:
        ws.send("test")
        print("sending...")
        time.sleep(2)

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
