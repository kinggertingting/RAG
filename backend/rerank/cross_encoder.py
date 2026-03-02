from sentence_transformers import CrossEncoder
from config.settings import RERANK_MODEL


class CrossEncoderModel:

    def __init__(self, model_name: str = None):
        self.model_name = model_name or RERANK_MODEL
        self.model = CrossEncoder(self.model_name)

    def predict(self, query: str, passages: list[str]):

        pairs = [(query, passage) for passage in passages]

        scores = self.model.predict(pairs)

        return scores