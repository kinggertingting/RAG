class Agentic:

    def decide(self, query: str):

        q = query.lower()

        if any(x in q for x in [
            "tóm tắt",
            "tóm lược",
            "nói về gì",
            "nội dung chính",
            "tài liệu này nói gì",
            "summary",
            "summarize",
            "overview",
            "what is this document about",
            "main idea"
        ]):
            return "summary"

        if any(x in q for x in [
            "là gì",
            "cái gì",
            "định nghĩa",
            "what is",
            "define",
            "definition"
        ]):
            return "definition"

        if any(x in q for x in [
            "mục tiêu",
            "để làm gì",
            "nhằm mục đích gì",
            "purpose",
            "goal",
            "objective",
            "aim"
        ]):
            return "purpose"

        if any(x in q for x in [
            "tại sao",
            "vì sao",
            "giải thích",
            "how does",
            "how does it work",
            "why",
            "explain"
        ]):
            return "explain"

        if any(x in q for x in [
            "so sánh",
            "khác gì",
            "so với",
            "compare",
            "difference",
            "what is the difference",
            "versus"
        ]):
            return "compare"

        if any(x in q for x in [
            "liệt kê",
            "những gì",
            "các loại",
            "what are",
            "list",
            "types of"
        ]):
            return "list"

        return "qa"