from sentence_transformers import SentenceTransformer
from db import get_connection

model = SentenceTransformer('all-MiniLM-L6-v2')

notes = [
    ("SAZEW", "SAZEW jumped sharply in early 2026 after reporting strong quarterly earnings and a new export contract announcement."),
    ("LUCK", "LUCK is Pakistan's largest cement producer, benefiting from increased construction demand and infrastructure spending."),
    ("MARI", "MARI Petroleum reported higher gas production volumes in its latest quarter, driving investor interest."),
]

connection = get_connection()
cursor = connection.cursor()

for ticker, content in notes:
    embedding = model.encode(content).tolist()
    cursor.execute(
        "INSERT INTO company_notes (ticker, content, embedding) VALUES (%s, %s, %s)",
        (ticker, content, embedding)
    )

connection.commit()
cursor.close()
connection.close()
print("Notes seeded.")