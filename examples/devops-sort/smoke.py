import argparse
import hashlib
import http.client
import json
from pathlib import Path
import socket
import subprocess
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('artifact')
args = parser.parse_args()
artifact = Path(args.artifact)
expected = artifact.with_suffix('.sha256').read_text().strip()
if hashlib.sha256(artifact.read_bytes()).hexdigest() != expected:
    raise SystemExit('artifact checksum mismatch')
with socket.socket() as socket_probe:
    socket_probe.bind(('127.0.0.1', 0))
    port = socket_probe.getsockname()[1]
process = subprocess.Popen([sys.executable, str(artifact), '--port', str(port)])


def request(method, path, body=None):
    connection = http.client.HTTPConnection('127.0.0.1', port, timeout=2)
    try:
        connection.request(method, path, body, {'Content-Type': 'application/json'})
        response = connection.getresponse()
        return response.status, json.loads(response.read())
    finally:
        connection.close()


try:
    for attempt in range(50):
        try:
            status, health = request('GET', '/health')
            break
        except OSError:
            if process.poll() is not None:
                raise SystemExit('service exited before health check')
            time.sleep(0.1)
    else:
        raise SystemExit('service did not become ready')
    if status != 200 or health != {'status': 'ok', 'version': artifact.stem}:
        raise SystemExit('health/version check failed')
    body = '{"products":[{"id":"a","price":10},{"id":"b","price":2},{"id":"c","price":1}]}'
    status, data = request('POST', '/sort', body)
    if status != 200 or [p['price'] for p in data['products']] != [1, 2, 10] or data['version'] != artifact.stem:
        raise SystemExit('sort smoke check failed')
    status, data = request('POST', '/sort', '{"products":[{"id":"a"}]}')
    if status != 400 or data.get('version') != artifact.stem:
        raise SystemExit('invalid-input smoke check failed')
    print('SMOKE OK version={} order=1,2,10 invalid=400'.format(artifact.stem))
finally:
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
