from sentence_transformers import SentenceTransformer
from db import get_connection

model = SentenceTransformer('all-MiniLM-L6-v2')

def answer_company_question(question: str) -> str:
    question_embedding = model.encode(question).tolist()

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT ticker, content FROM company_notes ORDER BY embedding <-> %s::vector LIMIT 1",
        (question_embedding,)
    )
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if not result:
        return "I don't have any notes on that yet."

    ticker, content = result
    return f"Based on my notes about {ticker}: {content}"