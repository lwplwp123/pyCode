# -*- coding:utf-8 -*-

from http import HTTPStatus
import http.server
import socketserver 



PORT = 80

# Case 1. it works.

# with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()


#Case 2. use baseHTTPRequestHandler.
# this got an error, still not found the root cause.

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print('do get.')
        print("path:",self.path)
        print("path--end")

        stext='''0 SFC_OK tsid::LXKS_A02-1FT-03_1_GATEKEEPER::unit_process_check=--OK'''
                
        self.send_response(HTTPStatus.OK)
        self.send_header("Server", "web Server")
        self.end_headers()
        self.wfile.write(stext.encode())

        # self.request.sendall(b'hello from get\r\n')

    def do_HEAD(self):
        print(" do HEAD..............")

    def do_POST(self):
        print('do post=====')
        print("path:",self.path)
        data = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        # count, self.client_address, self.command, self.path, self.request_version, str(self.headers).strip(), data))
        data = data.decode()
        print("data:",data)

        # stext="hello from Post. you've post data:"  + data + '\r\n'
        stext='''0 SFC_OK tsid::LXKS_A02-1FT-03_1_GATEKEEPER::unit_process_check=--OK'''

        self.send_response(HTTPStatus.OK)
        self.send_header("Server", "web Server")
        self.end_headers()
        self.wfile.write(stext.encode())

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()


#case 3 use BaseRequestHandler.

# class MyTCPHandler(socketserver.BaseRequestHandler):
#     """
#     The request handler class for our server.

#     It is instantiated once per connection to the server, and must
#     override the handle() method to implement communication to the
#     client.
#     """
   
#     def do_GET(self):
#         self.request.send(b'good..\r\n')
#         print('do get.............')

#     def handle(self):
#         # self.request is the TCP socket connected to the client
#         self.data = self.request.recv(1024).strip()
#         print("{} wrote:".format(self.client_address[0]))
#         print(self.data)
#         # just send back the same data, but upper-cased
#         self.request.send(self.data.upper())
#         self.request.send(b'\r\n')
#         print( self.request)


# with socketserver.TCPServer(("", PORT), MyTCPHandler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()




