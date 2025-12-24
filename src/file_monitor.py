from watchdog.observers import Observer
from .document_event_handler import DocumentEventHandler

class FileMonitor:
    def __init__(self, folder_to_watch, queue):
        self.folder = folder_to_watch
        self.queue = queue
        self.observer = Observer()

    def start(self):
        event_handler = DocumentEventHandler(self.queue)
        self.observer.schedule(event_handler, self.folder, recursive=False)
        self.observer.start()
        print(f"[file_monitor] A monitorizar: {self.folder}")



