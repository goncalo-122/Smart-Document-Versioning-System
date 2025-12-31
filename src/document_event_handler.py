from watchdog.events import FileSystemEventHandler
from pathlib import Path
from time import time

class DocumentEventHandler(FileSystemEventHandler):
    def __init__(self, queue):
        # Queue where events will be pushed for the VersionManager to process
        self.queue = queue

    def _is_valid(self, path: Path):

      #Determines whether a file should be processed. Ignore: - Temporary Office files (start with "~") - .tmp files - Any file that is not .docx or .xlsx

        if path.name.startswith("~"):
            return False
        if path.suffix.lower() == ".tmp":
            return False
        if path.suffix.lower() not in (".docx", ".xlsx"):
            return False
        return True

    def _enqueue(self, action, path):
        
        #Sends an event to the queue with: - action: created / modified / deleted - path: file path as string - timestamp: event time (used for debounce logic)

        self.queue.put({
            "action": action,
            "path": str(path),
            "timestamp": time()
        })

    def on_created(self, event):

       #Triggered when a file is created. Only valid .docx/.xlsx files are processed. 

        if event.is_directory:
            return
        path = Path(event.src_path)
        if not self._is_valid(path):
            return
        print(f"[document_event_handler] on_created: {path}")
        self._enqueue("created", path)

    def on_modified(self, event):

        #Triggered when a file is modified. Word/Excel often trigger MANY of these during save operations.

        if event.is_directory:
            return
        path = Path(event.src_path)
        if not self._is_valid(path):
            return
        print(f"[document_event_handler] on_modified: {path}")
        self._enqueue("modified", path)

    def on_deleted(self, event):

        #Triggered when a file is deleted. Note: Word/Excel sometimes delete and recreate files internally.

        if event.is_directory:
            return
        path = Path(event.src_path)
        if not self._is_valid(path):
            return
        print(f"[document_event_handler] on_deleted: {path}")
        self._enqueue("deleted", path)

    def on_moved(self, event):
       
       #Triggered when a file is moved or renamed. Word/Excel use this heavily during save operations: - They move the original file to a temp file - Then move a temp file back to the original name This looks like: deleted + created
        
        if event.is_directory:
            return

        src = Path(event.src_path)
        dest = Path(event.dest_path)

        print(f"[document_event_handler] on_moved: {src} -> {dest}")
        
        #Treat the old file as deleted (Treat the old file as deleted. Renaming a file makes the original path count as deleted).

        
        if self._is_valid(src):
            self._enqueue("deleted", src)

        # Treat the new file as created (if it will be created a new file with a new path)

        if self._is_valid(dest):
            self._enqueue("created", dest)
