import re


def split_text(text: str, chunk_size: int = 1000, overlap: int = 0):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid overlap")

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text)
        if p.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:

        if len(paragraph) <= chunk_size:
            candidate = (
                current + "\n\n" + paragraph
                if current else paragraph
            )

            if len(candidate) <= chunk_size:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                current = paragraph

            continue

        if current:
            chunks.append(current)
            current = ""

        sentences = re.split(r"(?<=[.!?])\s+", paragraph)

        for sentence in sentences:
            if len(sentence) > chunk_size:
                if current:
                    chunks.append(current)
                    current = ""

                words = sentence.split()
                for word in words:
                    candidate = (
                        current + " " + word
                        if current else word
                    )

                    if len(candidate) <= chunk_size:
                        current = candidate
                    else:
                        chunks.append(current)
                        current = word

            else:
                candidate = (
                    current + " " + sentence
                    if current else sentence
                )

                if len(candidate) <= chunk_size:
                    current = candidate
                else:
                    chunks.append(current)
                    current = sentence

    if current:
        chunks.append(current)

    return chunks
