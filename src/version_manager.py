from pathlib import Path
from datetime import datetime
from .convert import Convert
import time

class versionManager:
    def __init__(self, backup_folder, deleted_folder):
        # Create backup and deleted folders if they don't exist
        self.backup_folder = Path(backup_folder)
        self.backup_folder.mkdir(parents=True, exist_ok=True)

        self.deleted_folder = Path(deleted_folder)
        self.deleted_folder.mkdir(parents=True, exist_ok=True)
        
        # Convert handles DOCX/XLSX → PDF
        self.convert = Convert()

        # Stores pending events for each file:
        # path -> {"deleted": bool, "modified": bool, "last_event_time": float}
        self.pending = {}

    def _normalize(self, path):
        #Normalizes a file path to an absolute resolved Path object. Helps avoid duplicates caused by relative paths.
        try:
            return Path(path).resolve()
        except Exception:
            return Path(path).absolute()

    def add_event(self, event):
       #Receives events from the file monitor and stores them in 'pending'. Handles created, modified, and deleted events.
        
        path = self._normalize(event["path"])

        # Ignore temporary Office files
        if path.name.startswith("~$") or path.suffix.lower() == ".tmp":
            return
        # Ensure entry exists 
        if path not in self.pending: 
            self.pending[path] = {"deleted": False, "modified": False, "last_event_time": 0.0}

    

        action = event["action"]
        self.pending[path]["last_event_time"] = event["timestamp"]

        if action == "deleted":
            # Mark as deleted
            self.pending[path]["deleted"] = True
        elif action in ("created", "modified"):
            # Mark as modified 
            self.pending[path]["modified"] = True
            # If a previous "deleted" was caused by Office temp moves, cancel it
            if self.pending[path].get("deleted"):
                self.pending[path]["deleted"] = False

    def _save_version(self, path: Path):
        
        # Converts a DOCX or XLSX file into a PDF version and stores it in the backup folder.

        time.sleep(0.5)# Small delay to ensure Office finished writing

        timestamp = datetime.now().strftime("%Y-%m-%d")
        pdf_name = f"{path.stem}_{timestamp}.pdf"
        dest = self.backup_folder / pdf_name

         # Ignore default empty Office templates
        stem = path.stem.lower()
        if stem.startswith("novo documento do microsoft word"):
            return
        if stem.startswith("novo folha de cálculo do microsoft excel"):
            return

         # Convert based on file type
        if path.suffix.lower() == ".docx":
            self.convert.docx_to_pdf(path, dest)
        elif path.suffix.lower() == ".xlsx":
            self.convert.xlsx_to_pdf(path, dest)

        print(f"[VersionManager] PDF created: {dest}")

    def _save_deleted(self, path: Path):
        
        #Creates a PDF record documenting that a file was deleted.

        timestamp = datetime.now().strftime("%Y-%m-%d")
        pdf_name = f"DELETED_{path.stem}_{timestamp}.pdf"
        dest = self.deleted_folder / pdf_name
        
        # Ignore default Office templates
        stem = path.stem.lower()
        if stem.startswith("novo documento do microsoft word"):
            return
        if stem.startswith("novo folha de cálculo do microsoft excel"):
            return
        
        # Only create deletion PDF if the file truly no longer exists
        if not path.exists():
            self.convert.create_deleted_pdf(path.name, timestamp, dest)
            print(f"[VersionManager] Delete PDF created: {dest}")
        else:
            print(f"[VersionManager] Ignore deleted: file still exists {path}")

    def flush(self):
        
        # Process pending events and decide whether to save a version or a deletion record
        print("[VersionManager] FLUSH started")
        now = time.time()
        # Iterate over a copy so we can safely delete entries
        for path, info in list(self.pending.items()):
            # Debounce: wait at least 1 second since the last event
            if now - info.get("last_event_time", 0) < 1.0:
                continue

            #Case 1: Marked deleted but file still exists → ignore deletion
            if info.get("deleted", False) and path.exists():
                print(f"[VersionManager] Ignore deleted: file still exists {path}")
                #If also modified, save version
                if info.get("modified", False):
                    print(f"_save_version {path}")
                    self._save_version(path) 
                
            elif info.get("deleted", False) and not path.exists():
                print(f"_save_deleted {path}")
                self._save_deleted(path)
            elif info.get("modified", False) and path.exists():
                print(f"_save_version {path}")
                self._save_version(path)

            # remover entrada processada
            del self.pending[path]

        self.convert.close()
        print("[VersionManager] FLUSH finished")
