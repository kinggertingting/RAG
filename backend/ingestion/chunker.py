from typing import List
from config.settings import CHUNK_SIZE, OVERLAP
import nltk


class Chunker:
    def __init__(self, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP):
        self.chunk_size = chunk_size if chunk_size > 0 else CHUNK_SIZE
        self.overlap = overlap if overlap >= 0 else OVERLAP

    def chunking(self, text: str) -> List[str]:

        paragraphs = text.split("\n\n")
        chunks: List[str] = []
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current_chunk) + len(para) <= self.chunk_size:
                current_chunk += (" " + para) if current_chunk else para

            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())

                if len(para) > self.chunk_size:
                    sentences = nltk.sent_tokenize(para)
                    temp_chunk = ""

                    for sentence in sentences:
                        if len(temp_chunk) + len(sentence) <= self.chunk_size:
                            temp_chunk += " " + sentence
                        else:
                            if temp_chunk:
                                chunks.append(temp_chunk.strip())
                            temp_chunk = sentence

                    current_chunk = temp_chunk.strip()

                else:
                    current_chunk = para

        if current_chunk:
            chunks.append(current_chunk.strip())

        overlapped_chunks = []

        for i, chunk in enumerate(chunks):
            if i > 0 and self.overlap > 0:
                prev_chunk = chunks[i - 1]
                overlap_text = prev_chunk[-self.overlap:]
                chunk = overlap_text + " " + chunk

            overlapped_chunks.append(chunk.strip())

        return overlapped_chunks