from watchdog.events import FileSystemEventHandler
from pathlib import Path
from time import time

class DocumentEventHandler(FileSystemEventHandler):
    def __init__(self, queue):
        self.queue = queue

    def _is_valid(self, path: Path):
        # IGNORAR temporários e lixo do Word
        if path.name.startswith("~"):
            return False
        if path.suffix.lower() == ".tmp":
            return False
        if path.suffix.lower() not in (".docx", ".xlsx"):
            return False
        return True

    def _enqueue(self, action, path):
        self.queue.put({
            "action": action,
            "path": str(path),
            "timestamp": time()
        })

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if not self._is_valid(path):
            return
        print(f"[Monitor] Criado: {path}")
        self._enqueue("created", path)

    def on_modified(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if not self._is_valid(path):
            return
        print(f"[Monitor] Modificado: {path}")
        self._enqueue("modified", path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if not self._is_valid(path):
            return
        print(f"[Monitor] Eliminado: {path}")
        self._enqueue("deleted", path)

    def on_moved(self, event):
        if event.is_directory:
            return

        src = Path(event.src_path)
        dest = Path(event.dest_path)

        print(f"[Monitor] Movido: {src} -> {dest}")

        if self._is_valid(src):
            self._enqueue("deleted", src)

        if self._is_valid(dest):
            self._enqueue("created", dest)
