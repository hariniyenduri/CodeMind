from src.embeddings.embedding_generator import (
    EmbeddingGenerator,
)


# ==========================================
# CREATE EMBEDDING GENERATOR
# ==========================================

generator = EmbeddingGenerator()


# ==========================================
# TEST TEXT
# ==========================================

text = """
def login(username, password):
    if username == "admin":
        return True

    return False
"""


# ==========================================
# GENERATE EMBEDDING
# ==========================================

embedding = generator.generate_embedding(
    text
)


# ==========================================
# DISPLAY RESULT
# ==========================================

print(
    "\n========== EMBEDDING TEST =========="
)

print(
    f"Embedding length: {len(embedding)}"
)

print(
    f"First 10 values: {embedding[:10]}"
)