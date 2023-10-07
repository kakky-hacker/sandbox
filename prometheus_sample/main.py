from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import timeit
from urllib.parse import urlparse

from prometheus_client import start_http_server
from prometheus_client import Counter, Summary

get_method_counter = Counter('http_get_requests', 'HTTP GET Request Counter')
post_method_counter = Counter('http_post_requests', 'HTTP POST Request Counter')
access_counter = Counter('http_status', 'HTTP Access Counter', ['method', 'url', 'status_code'])
exception_conter = Counter('exceptions', 'HTTP Server Exception Counter')
get_request_time = Summary('http_get_request_processing_seconds', 'HTTP GET Request Time')
post_request_time = Summary('http_post_request_processing_seconds', 'HTTP POST Request Time', ['method', 'url'])

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    @exception_conter.count_exceptions()
    @get_request_time.time()
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path.endswith('/error'):
            raise Exception('Error')

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(f'Hello World!! from {self.path} as GET'.encode('utf-8'))

        get_method_counter.inc()
        access_counter.labels('GET', parsed_path.path, '200').inc()

    @exception_conter.count_exceptions()
    def do_POST(self):
        start = timeit.default_timer()
        
        parsed_path = urlparse(self.path)

        if parsed_path.path.endswith('/error'):
            raise Exception('Error')

        content_length = int(self.headers['content-length'])
        body = self.rfile.read(content_length).decode('utf-8')

        print(f'body = {body}')

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(f'Hello World!! from {self.path} as POST'.encode('utf-8'))

        elapsed_time = timeit.default_timer() - start

        post_method_counter.inc()
        access_counter.labels('POST', parsed_path.path, '200').inc()
        post_request_time.labels('POST', parsed_path.path).observe(elapsed_time)

if __name__ == '__main__':
    start_http_server(8000)

    with ThreadingHTTPServer(('0.0.0.0', 8080), MyHTTPRequestHandler) as server:
        print(f'[{datetime.now()}] Server startup.')
        server.serve_forever()