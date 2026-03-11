import re


class Cleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""

        text = re.sub(r"<[^>]+>", " ", text)

        text = re.sub(r"\r\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        text = re.sub(r"[ \t]+", " ", text)

        text = re.sub(r"[^\x20-\x7E\u00A0-\uFFFF\n]", " ", text)

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        return "\n".join(lines).strip()