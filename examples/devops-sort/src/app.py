import argparse
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from sorting import sort_products
from version import VERSION


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print(json.dumps({'version': VERSION, 'path': self.path,
                          'status': status,
                          'duration_ms': round((time.perf_counter() - self.started) * 1000, 2)}),
              flush=True)

    def do_GET(self):
        self.started = time.perf_counter()
        if self.path == '/health':
            self.reply(200, {'status': 'ok', 'version': VERSION})
        else:
            self.reply(404, {'error': 'not found'})

    def do_POST(self):
        self.started = time.perf_counter()
        if self.path != '/sort':
            self.reply(404, {'error': 'not found'})
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 65536:
                raise ValueError('body must be 1..65536 bytes')
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError('body must be an object')
            products = sort_products(data.get('products'))
        except (ValueError, UnicodeDecodeError) as error:
            self.reply(400, {'error': str(error), 'version': VERSION})
            return
        self.reply(200, {'products': products, 'version': VERSION})

    def log_message(self, *args):
        pass  # reply() writes the structured request log instead.


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    with HTTPServer(('127.0.0.1', args.port), Handler) as server:
        print('Serving version {} on port {}'.format(VERSION, args.port), flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
