from pathlib import Path

class DocumentProcessor:
    
    def extract_text(self, file_path: str):
        
        path = Path(file_path)

        suffix = path.suffix.lower()

        if suffix == ".txt":
            return self._extract_txt(path)
        if suffix == ".pdf":
            return self._extract_pdf(path)
        if suffix == ".docx":
            return self._extract_docx(path)
        
        raise ValueError(f"Unsupported file format: {suffix}")
    
    def _extract_txt(self, path: Path):

        return path.read_text(encoding="utf-8")
    
    def _extract_pdf(self, path: Path):
        pass
        import PyPDF2

        text = ""
        with open(path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def _extract_docx(self, path: Path):
        pass
        from docx import Document

        doc = Document(path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text