import tornado.ioloop
import tornado.web
import tornado.websocket

import json

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

    def open(self):
        print("WebSocket opened")
        self.hosts = hosts_get("./hosts")
        print self.hosts

        #main_loop = tornado.ioloop.IOLoop.instance()
        #self.loop = tornado.ioloop.PeriodicCallback(self.send_results(), 1000)#, io_loop=main_loop)
        #self.loop.start()
        #main_loop.start()

    def on_close(self):
        print("WebSocket closed")

    '''
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
   '''
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws", SocketHandler),
    ])






def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()