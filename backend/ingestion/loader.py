from config.settings import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
import PyPDF2
import docx
class Loader:

    def check_file_extension(self, file):
        filename = file.filename

        if "." not in filename:
            raise ValueError("File không hợp lệ")

        extension = "." + filename.split(".")[-1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Không hỗ trợ file {extension}")

        return extension


    def check_max_size_file(self, file):
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size > MAX_FILE_SIZE:
            raise ValueError("File vượt quá giới hạn cho phép")


    def load_pdf(self, file):
        reader = PyPDF2.PdfReader(file.file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        file.file.seek(0)
        return text.strip()


    def load_doc(self, file):
        document = docx.Document(file.file)
        text = ""

        for para in document.paragraphs:
            if para.text:
                text += para.text + "\n"

        file.file.seek(0)
        return text.strip()


    def load_txt(self, file):
        content = file.file.read().decode("utf-8", errors="ignore")
        file.file.seek(0)
        return content.strip()


    def load_file(self, file):
        self.check_max_size_file(file)

        extension = self.check_file_extension(file)

        if extension == ".pdf":
            return self.load_pdf(file)

        elif extension == ".docx":
            return self.load_doc(file)

        elif extension == "txt":
            return self.load_txt(file)

        else:
            raise ValueError("Unsupported file type")