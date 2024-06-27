# Problem 3

## 1: Creating the server
I've chosen http.server lib to create a simple http server handling get & post requests.

```python 
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

```

## 2: Creating Dockerfile
Now we should write a dockerfile that creates an image that runs the python script inside itself.

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY app.py /app
RUN pip install flask
EXPOSE 8000
CMD ["python", "app.py"]
```

## 3: Build and Run
1. **Build the Docker Image**:
   - Run `docker build -t myhttpserver .`

2. **Run the Docker Container**:
   - Run `docker run -p 8000:8000 myhttpserver`

## 4: Test
We can simply check its working by sending get requests from another shell using python like below:

```python
>>> import requests
>>> requests.get('http://localhost:8000/api/v1/status').content # Test Get
>>> requests.post('http://localhost:8000/api/v1/status', json={'status':'not ok'}).content # Test post
b'{"status": "not ok"}'

b'{"status": "ok"}'
>>> requests.get('http://localhost:8000/anything/else').content # Handling incorrect path
b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
            <title>Error response</title>
                </head>
                <body>
                    <h1>Error response</h1>S
                    <p>Error code: 404</p>
                    <p>Message: Not found.</p>
                    <p>Error code explanation: 404 - Nothing matches the given URI.</p>
                </body>
        </html>
'
```
