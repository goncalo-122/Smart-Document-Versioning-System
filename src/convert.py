import win32com.client as win32
from pathlib import Path
from reportlab.pdfgen import canvas
import time


class Convert:
    def __init__(self):
        self.word = None
        self.excel = None

    def _ensure_word(self):
        
        #Ensures that a Word  instance is created. Only initializes Word once and keeps it open for performance.
        if self.word is None:
            self.word = win32.gencache.EnsureDispatch("Word.Application")
            self.word.Visible = False   # Run Word in the background
            self.word.DisplayAlerts = 0 # Disable pop‑ups and warnings
        

    def _ensure_excel(self):

        #Ensures that an Excel  instance is created. Only initializes Excel once and keeps it open for performance.
        if self.excel is None:
            self.excel = win32.Dispatch("Excel.Application")
            self.excel.Visible = False
            self.excel.DisplayAlerts = 0


    def wait_until_unlocked(self, path, timeout=5):
    
       # Waits until a file is no longer locked by Word/Excel.
       #This prevents errors or empty PDFs caused by converting a file
       #while the Office application is still writing to it.
        path = Path(path)
        start = time.time()

        # Try repeatedly until the timeout is reached
        while time.time() - start < timeout:
            try:
                # If the file opens successfully, it is not locked
                with open(path, "rb"):
                    return True
            except PermissionError:
                # File is still locked — wait a bit and try again
                time.sleep(0.2)
        print(f"[Convert] File locked for too long: {path}")
        return False


    def docx_to_pdf(self, src, dest):

       #Converts a .docx file to PDF using Word's  interface.
        src = Path(src)
        dest = Path(dest)

        if not self.wait_until_unlocked(src):
            return
        self._ensure_word()
        doc = self.word.Documents.Open(str(src), ReadOnly=True)
        doc.SaveAs(str(dest), FileFormat=17)  # 17 = PDF format
        doc.Close()
        print(f"[Convert] DOCX -> PDF: {src} -> {dest}")


    def xlsx_to_pdf(self, src, dest):
        #Converts an .xlsx file to PDF using Excel's interface.
        src = Path(src)
        dest = Path(dest)

        # Ensure the file is not locked before converting
        if not self.wait_until_unlocked(src):
            return
        self._ensure_excel()
        wb = self.excel.Workbooks.Open(str(src), ReadOnly=True)
        wb.ExportAsFixedFormat(0, str(dest))  # 0 = PDF format
        wb.Close()
        print(f"[Convert] XLSX -> PDF: {src} -> {dest}")

    def create_deleted_pdf(self, filename, timestamp, dest):
        #Creates a simple PDF documenting that a file was deleted. Used when a .docx or .xlsx file is removed from the watched folder.
        
        dest = Path(dest)
        c = canvas.Canvas(str(dest))
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, f"File: {filename}")
        c.drawString(100, 730, f"Deleted at: {timestamp}")
        c.save()
        print(f"[Convert] PDF of the deletion document created: {dest}")

    def close(self):
        #Closes Word and Excel COM instances if they were opened. Prevents background processes from staying alive.
        
        if self.word:
            self.word.Quit()
            self.word = None
        if self.excel:
            self.excel.Quit()
            self.excel = None
        print("[Convert] Word/Excel closed")
