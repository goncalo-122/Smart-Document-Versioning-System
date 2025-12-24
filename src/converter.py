import win32com.client as win32
from pathlib import Path
from reportlab.pdfgen import canvas

class Converter:
    def __init__(self):
        self.word = None
        self.excel = None

    def _ensure_word(self):
        if self.word is None:
            self.word = win32.gencache.EnsureDispatch("Word.Application")
            self.word.Visible = False
            self.word.DisplayAlerts = 0  # não bloquear com popups

    def _ensure_excel(self):
        if self.excel is None:
            self.excel = win32.Dispatch("Excel.Application")
            self.excel.Visible = False
            self.excel.DisplayAlerts = 0

    def docx_to_pdf(self, src, dest):
        self._ensure_word()
        doc = self.word.Documents.Open(str(src))
        doc.SaveAs(str(dest), FileFormat=17)
        doc.Close()

    def xlsx_to_pdf(self, src, dest):
        self._ensure_excel()
        wb = self.excel.Workbooks.Open(str(src))
        wb.ExportAsFixedFormat(0, str(dest))
        wb.Close()

    def close(self):
        if self.word:
            self.word.Quit()
            self.word = None
        if self.excel:
            self.excel.Quit()
            self.excel = None

    def create_deleted_pdf(self, filename, timestamp, dest):
        c = canvas.Canvas(str(dest))
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, f"File: {filename}")
        c.drawString(100, 730, f"Deleted at: {timestamp}")
        c.save()
