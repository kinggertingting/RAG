from typing import List
from config.settings import CHUNK_SIZE, OVERLAP
import nltk


class Chunker:
    def __init__(self, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP):
        self.chunk_size = chunk_size if chunk_size > 0 else CHUNK_SIZE
        self.overlap = overlap if overlap >= 0 else OVERLAP

    def chunking(self, text: str) -> List[str]:

        sentences = nltk.sent_tokenize(text)

        chunks = []
        current = []

        for sentence in sentences:

            length = sum(len(s) for s in current) + len(sentence)

            if length <= self.chunk_size:
                current.append(sentence)

            else:
                chunks.append(" ".join(current))

                current = current[-self.overlap:]
                current.append(sentence)

        if current:
            chunks.append(" ".join(current))

        return chunks