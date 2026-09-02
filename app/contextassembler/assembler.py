from app.contextassembler.base import ContextAssembler
from app.retrieval.models import RetrievedChunk


class DefaultContextAssembler(ContextAssembler):

    def assemble(
        self,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:

        seen = set()
        result = []
        print("assembler called",len(chunks))

        for chunk in chunks:

            content = chunk.content.strip()

            if not content:
                continue

            if content in seen:
                continue

            seen.add(content)
            result.append(chunk)

        return result