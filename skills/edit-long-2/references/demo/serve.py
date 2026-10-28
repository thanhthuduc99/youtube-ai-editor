# Static server for the demo with HTTP Range support (Chrome needs 206 responses to seek inside <video>).
# Usage: python serve.py [port]   ->  http://localhost:8765/
import os
import re
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class Range(SimpleHTTPRequestHandler):
    def send_head(self):
        m = re.match(r'bytes=(\d*)-(\d*)', self.headers.get('Range', ''))
        path = self.translate_path(self.path)
        if not m or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        a = int(m[1]) if m[1] else max(0, size - int(m[2]))
        b = min(int(m[2]), size - 1) if m[1] and m[2] else size - 1
        f = open(path, 'rb'); f.seek(a)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {a}-{b}/{size}')
        self.send_header('Content-Length', str(b - a + 1))
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        self.remaining = b - a + 1
        return f

    def copyfile(self, src, dst):
        n = getattr(self, 'remaining', None)
        if n is None:
            return super().copyfile(src, dst)
        while n > 0:
            chunk = src.read(min(1 << 16, n))
            if not chunk:
                break
            dst.write(chunk); n -= len(chunk)

    def log_message(self, *a):
        pass


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
print(f'http://localhost:{port}/', flush=True)
ThreadingHTTPServer(('127.0.0.1', port), partial(Range, directory=os.path.dirname(os.path.abspath(__file__)))).serve_forever()
