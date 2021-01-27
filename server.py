#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/
import os

class MyWebServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        if b"POST" in self.data or b"PUT" in self.data or b"DELETE" in self.data:
            self.request.sendall(bytearray("""HTTP/1.1 405 Method Not Allowed\n""",'utf-8'))
            # self.request.sendall(bytearray("""Content-Type: text/html\n""",'utf-8'))
            # self.request.sendall(bytearray("""\n""",'utf-8'))
            # self.request.sendall(bytearray("""
            #         <html>
            #         <body>
            #         <h1>405 Method Not Allowed!</h1>
            #         </body>
            #         </html>
            # """,'utf-8'))
            return

        # self.request.sendall(bytearray("OK",'utf-8'))
        # print(os.path.realpath("www//index.html").encode())
        # self.request.sendall(os.path.realpath("www//index.html").encode())
        self.request.sendall(bytearray("""HTTP/1.1 200 OK\n""",'utf-8'))
        self.request.sendall(bytearray("""Content-Type: text/html\n""",'utf-8'))
        self.request.sendall(bytearray("""\n""",'utf-8'))
    #     self.request.sendall(bytearray("""
    # <html>
    # <body>
    # <h1>Hello World</h1> this is my server!
    # </body>
    # </html>
    #     """,'utf-8'))

        # Generic index.html file sent
        generic_file = open(os.getcwd()+"""\\www\\index.html""").read()
        self.request.sendall(bytearray(generic_file,'utf-8'))

        # if os.path.exists(os.getcwd()+'\\www\\index.html'):
        #     print("I found something?")
        # else:
        #     print("na")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

