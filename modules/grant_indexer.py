"""
Module for indexing grant descriptions using LlamaIndex.

This module handles the following tasks:

- Creating a LlamaIndex knowledge base from grant descriptions.
- Choosing appropriate index types (e.g., GPTIndex, GPTListIndex) based on the data structure and search requirements.
- Configuring embedding models (e.g., OpenAI's text-embedding-ada-002) for efficient search.
- Saving and loading the index for persistent storage.
"""
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import psycopg2
from pgvector.psycopg2 import register_vector

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="vectordb",
    user="testuser",
    password="testpwd",
)

# Register the pgvector extension
register_vector(conn)

# Create a cursor
cur = conn.cursor()
# Example: Create a table with a vector column
cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id SERIAL PRIMARY KEY,
        name TEXT,
        embedding vector(128)
    );
""")

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()

#cur.execute("""DROP TABLE items;""")

grants = SimpleDirectoryReader("./data/grants/").load_data()

print(grants)

index = VectorStoreIndex.from_documents(grants, show_progress=True)