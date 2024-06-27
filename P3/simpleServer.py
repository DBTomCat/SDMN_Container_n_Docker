import http.server
import socketserver
import json

PORT = 8000

status = 'ok'

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global status
        if self.path == "/api/v1/status" :
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {'status': status}
            self.wfile.write(json.dumps(response).encode())
        else :
            self.send_error(404, "Not found")

    def do_POST(self):
        global status
        if self.path == "/api/v1/status" :
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            status = data.get('status')
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {'status': status}
            self.wfile.write(json.dumps(response).encode())
        else :
            self.send_error(404, "Not found")

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
