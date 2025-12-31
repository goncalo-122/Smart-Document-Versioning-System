from watchdog.observers import Observer
from .document_event_handler import DocumentEventHandler

class FileMonitor:

    #It monitors a specific folder and sends all file events (creation, modification, deletion, or movement) to the queue used by the VersionManager, which then decides how to process each event.
    
    def __init__(self, folder_to_watch, queue):
        self.folder = folder_to_watch
        self.queue = queue
        self.observer = Observer()

    def start(self):
        # Creates the handler that the Watchdog will use to send events; the handler processes them and places them in the queue.
        event_handler = DocumentEventHandler(self.queue)
        
        # Monitor only the top-level folder (no recursion- because does not exists subfolders)
        self.observer.schedule(event_handler, self.folder, recursive=False)
        
        self.observer.start()
        print(f"[file_monitor] Monitoring: {self.folder}")



