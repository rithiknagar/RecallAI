import re

from app.citations.models import Citation


class CitationService:

    def build_citations(
        self,
        chunks,
    ) -> list[Citation]:

        citations = []

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):
            citations.append(
                Citation(
                    source_id=f"S{index}",
                    document_id=chunk.document_id,
                    chunk_id=chunk.chunk_id,
                    source=chunk.metadata.get("filename"),
                    page=chunk.metadata.get("page"),
                )
            )

        return citations

    def get_valid_source_ids(
        self,
        citations: list[Citation],
    ) -> set[str]:

        return {
            citation.source_id
            for citation in citations
        }

    def extract_source_ids(
        self,
        answer: str,
    ) -> set[str]:

        return set(
            re.findall(
                r"\[S\d+\]",
                answer,
            )
        )

    def validate_answer_citations(
        self,
        answer: str,
        citations: list[Citation],
    ) -> set[str]:

        valid_source_ids = (
            self.get_valid_source_ids(
                citations
            )
        )

        answer_source_ids = (
            self.extract_source_ids(
                answer
            )
        )

        return (
            answer_source_ids
            & valid_source_ids
        )
    def clean_invalid_citations(
    self,
    answer: str,
    citations: list[Citation],
) -> str:

        valid_source_ids = {
            f"[{citation.source_id}]"
            for citation in citations
        }

        def replace(match):
            source_id = match.group(0)

            if source_id in valid_source_ids:
                return source_id

            return ""

        return re.sub(
            r"\[S\d+\]",
            replace,
            answer,
        )