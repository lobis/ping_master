import tornado.ioloop
import tornado.web
import tornado.websocket

import json
import os

from ping import hosts_get, ping_host

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./templates/socket.html")

class SocketHandler(tornado.websocket.WebSocketHandler):
    def send_results(self):
        results_ping = {}
        for host in self.hosts:
            results_ping[host] = ping_host(host)
        data_json = json.dumps(results_ping)
        print(data_json)
        self.write_message(data_json)

    def send_hello(self):
        print("hello!")
    def open(self):
        print("WebSocket opened")
        self.hosts = hosts_get("./hosts")
        print("Hosts: %s" % self.hosts)

        #tornado.ioloop.PeriodicCallback(self.send_results(), 1000).start()
        #self.callback = tornado.ioloop.PeriodicCallback(self.send_hello(), 1000)
        #self.callback.start()

    def on_close(self):
        print("WebSocket closed")

    def on_message(self, message):
        print("Received message: %s" % message)
        self.send_results()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", SocketHandler),
        #(r"/static/(.*)", tornado.web.StaticFileHandler)],
        ]
    )
#"/home/luis/Desktop/ping_master"
#os.path.join(os.path.dirname(__file__))
def main():
    app = make_app()
    app.listen(8888)
    #tornado.ioloop.IOLoop.current().start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    print os.path.dirname(__file__)
    main()