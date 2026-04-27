from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path

IP = "127.0.0.1"
PORT = 8080

BASE_PATH = Path(__file__).resolve().parent / "html"


SEQUENCES = [
    "ATCGATCGATCG",
    "GCTAGCTAGCTA",
    "TTTTCCCCAAAA",
    "CGCGATATAGCG",
    "AGCTAGCTAGCTAGCT"
]

GENES = {
    "U5": "ACGTACGTGACG",
    "ADA": "GCTAGCTAGGCTA",
    "FRAT1": "TTTGGGCCCAAA",
    "RNU6_269P": "CGATCGATCGAT",
    "FXN": "ATGCGTAGCTAGCTAG"
}


def complement(seq):
    return seq.translate(str.maketrans("ATCG", "TAGC"))


def reverse(seq):
    return seq[::-1]


def info(seq):
    total = len(seq)
    return f"""
    <h2>Sequence: {seq}</h2>
    <p>Total length: {total}</p>
    <p>A: {seq.count('A')} ({seq.count('A')/total*100:.1f}%)</p>
    <p>C: {seq.count('C')} ({seq.count('C')/total*100:.1f}%)</p>
    <p>G: {seq.count('G')} ({seq.count('G')/total*100:.1f}%)</p>
    <p>T: {seq.count('T')} ({seq.count('T')/total*100:.1f}%)</p>
    """


class MyHandler(BaseHTTPRequestHandler):

    def load(self, file):
        return open(BASE_PATH / file).read()

    def do_GET(self):

        url = urlparse(self.path)
        path = url.path
        params = parse_qs(url.query)

        try:

            # ---------------- INDEX ----------------
            if path == "/" or path == "/index.html":
                body = self.load("index.html")

            # ---------------- PING ----------------
            elif path == "/ping":
                body = self.load("ping.html")

            # ---------------- GET ----------------
            elif path == "/get":
                n = int(params["n"][0])
                seq = SEQUENCES[n]

                body = self.load("get.html")
                body = body.replace("{{number}}", str(n)).replace("{{sequence}}", seq)

            # ---------------- GENE ----------------
            elif path == "/gene":
                name = params["name"][0]
                seq = GENES[name]

                body = self.load("gene.html")
                body = body.replace("{{gene}}", name).replace("{{sequence}}", seq)

            # ---------------- OPERATION ----------------
            elif path == "/operation":
                seq = params["seq"][0]
                op = params["op"][0]

                if op == "info":
                    result = info(seq)
                elif op == "comp":
                    result = complement(seq)
                    result = f"<h2>Complement</h2><p>{result}</p>"
                elif op == "rev":
                    result = reverse(seq)
                    result = f"<h2>Reverse</h2><p>{result}</p>"
                else:
                    raise Exception()

                body = self.load("operation.html")
                body = body.replace("{{result}}", result)

            # ---------------- ERROR ----------------
            else:
                self.send_response(404)
                body = self.load("error.html")
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(body.encode())
                return

            # ---------------- RESPONSE ----------------
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(body.encode())

        except:
            self.send_response(400)
            body = self.load("error.html")
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(body.encode())


server = HTTPServer((IP, PORT), MyHandler)

print(f"Server running at http://{IP}:{PORT}")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Stopped")
    server.server_close()

