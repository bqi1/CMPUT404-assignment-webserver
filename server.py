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
        if self.data == b"": return
        root_path = os.getcwd()+"/www" # The webserver can serve files from ./www

        # print ("Got a request of: %s\n" % self.data)
        
        # Return a status code of “405 Method Not Allowed” for any method you cannot handle (POST/PUT/DELETE)
        if "GET" not in self.data.decode("utf-8").split()[0]:
            self.request.sendall(bytearray("""HTTP/1.1 405 Method Not Allowed\n""",'utf-8'))
            return
        url = self.data.decode("utf-8").split()[1] # From Ethan Hill on https://stackoverflow.com/questions/53163366/python-simple-socket-get-url-from-client-request at 2021-01-27
        # The webserver can server 404 errors for paths not found
        if not os.path.exists(root_path+url):
            print(f"{root_path+url} DOES NOT EXIST\n")
            self.request.sendall(bytearray(f"""HTTP/1.1 404 Not Found\n""",'utf-8')) # 404 errors for paths not found
            return
        
        if url[-1] != "/" and os.path.isdir(root_path+url+"/"):
            self.request.sendall(bytearray(f"""HTTP/1.1 301 Moved Permanently\nLocation: {url}/\n""",'utf-8')) # Must use 301 to correct paths
            return

        # The webserver can return index.html from directories (paths that end in /)
        if url[-1] == "/" and os.path.isdir(root_path+url):
            self.request.sendall(bytearray("""HTTP/1.1 200 OK\n""",'utf-8'))
            self.request.sendall(bytearray("""Content-Type: text/html\n""",'utf-8'))
            self.request.sendall(bytearray("""\n""",'utf-8'))
            self.request.sendall(bytearray(self.getContent(url+"/index.html",root_path),'utf-8'))

        # The webserver supports mime-types for HTML
        if ".html" in url:
            self.request.sendall(bytearray("""HTTP/1.1 200 OK\n""",'utf-8'))
            self.request.sendall(bytearray("""Content-Type: text/html\n""",'utf-8'))
            self.request.sendall(bytearray("""\n""",'utf-8'))
            self.request.sendall(bytearray(self.getContent(url,root_path),'utf-8'))

        # The webserver supports mime-types for CSS
        # The webserver can serve CSS properly so that the front page has an orange h1 header.
        if ".css" in url:
            self.request.sendall(bytearray("""HTTP/1.1 200 OK\n""",'utf-8'))
            self.request.sendall(bytearray("""Content-Type: text/css\n""",'utf-8'))
            self.request.sendall(bytearray("""\n""",'utf-8'))
            self.request.sendall(bytearray(self.getContent(url,root_path),'utf-8'))
            return

    def getContent(self,name,path):
        return open(path+name).read()


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8080 #  The webserver works with Firefox and Chromium

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()