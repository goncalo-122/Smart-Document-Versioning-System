from pathlib import Path
from datetime import datetime
from .converter import Converter

class versionManager:
    def __init__(self, backup_folder, deleted_folder):
        
        self.backup_folder = Path(backup_folder)
        self.backup_folder.mkdir(parents=True, exist_ok=True)

        self.deleted_folder = Path(deleted_folder)
        self.deleted_folder.mkdir(parents=True, exist_ok=True)

        self.converter = Converter()

        # path -> {deleted: bool}
        self.pending = {}

    # ---------------------------------------------------------
    #   RECEBER EVENTOS (created, modified, deleted)
    # ---------------------------------------------------------
    def add_event(self, event):
        path = Path(event["path"])
        if path.name.startswith("~$"):
            return

        if path not in self.pending:
            self.pending[path] = {"deleted": False}

        if event["action"] == "deleted":
            self.pending[path]["deleted"] = True

    # ---------------------------------------------------------
    #   GUARDAR VERSÃO
    # ---------------------------------------------------------
    def _save_version(self, path):
        timestamp = datetime.now().strftime("%Y-%m-%d")
        pdf_name = f"{path.stem}_{timestamp}.pdf"
        dest = self.backup_folder / pdf_name
        stem = path.stem.lower()
        if stem.startswith("novo documento do microsoft word"):
            return
        if stem.startswith("novo folha de cálculo do microsoft excel"):
            return
        if path.suffix.lower() == ".docx":
            self.converter.docx_to_pdf(path, dest)
        elif path.suffix.lower() == ".xlsx":
            self.converter.xlsx_to_pdf(path, dest)

        print(f"[VersionManager] PDF criado: {dest}")

    # ---------------------------------------------------------
    #   GUARDAR DELETE
    # ---------------------------------------------------------
    def _save_deleted(self, path):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pdf_name = f"DELETED_{path.stem}_{timestamp}.pdf"
        dest = self.deleted_folder / pdf_name
        stem = path.stem.lower()
        if stem.startswith("novo documento do microsoft word"):
            return
        if stem.startswith("novo folha de cálculo do microsoft excel"):
            return
        if not path.exists():
            self.converter.create_deleted_pdf(path.name, timestamp, dest)
            print(f"[VersionManager] PDF de eliminação criado: {dest}")
      

    # ---------------------------------------------------------
    #   FLUSH FINAL — GUARDA TUDO
    # ---------------------------------------------------------
    def flush(self):
        print("[VersionManager] FLUSH iniciado")

        for path, info in list(self.pending.items()):
            if info["deleted"]:
                self._save_deleted(path)
            else:
                if path.exists():
                    self._save_version(path)

            del self.pending[path]

        # fechar Word/Excel no fim
        self.converter.close()
        print("[VersionManager] FLUSH terminado")
