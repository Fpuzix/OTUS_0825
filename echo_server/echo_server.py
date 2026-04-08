import socket
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs


HOST = "127.0.0.1"
PORT = 8080


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        conn, client_address = server.accept()

        with conn:
            request_data = b""

            while b"\r\n\r\n" not in request_data:
                part = conn.recv(4096)
                if not part:
                    break
                request_data += part

            request_text = request_data.decode("utf-8", errors="replace")
            lines = request_text.split("\r\n")

            request_line = lines[0]
            parts = request_line.split()

            method = parts[0] if len(parts) > 0 else "GET"
            path = parts[1] if len(parts) > 1 else "/"

            parsed = urlparse(path)
            params = parse_qs(parsed.query)
            raw_status = params.get("status", [None])[0]

            try:
                if raw_status:
                    status = HTTPStatus(int(raw_status))
                else:
                    status = HTTPStatus.OK
            except ValueError:
                status = HTTPStatus.OK

            body_lines = [
                f"Request Method: {method}",
                f"Request Source: {client_address}",
                f"Response Status: {status.value} {status.phrase}",
            ]

            for line in lines[1:]:
                if line == "":
                    break
                if ":" in line:
                    body_lines.append(line)

            body = "\r\n".join(body_lines)
            body_bytes = body.encode("utf-8")

            response = (
                f"HTTP/1.1 {status.value} {status.phrase}\r\n"
                f"Content-Type: text/plain; charset=utf-8\r\n"
                f"Content-Length: {len(body_bytes)}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            ).encode("utf-8") + body_bytes

            conn.sendall(response)


if __name__ == "__main__":
    run_server()
