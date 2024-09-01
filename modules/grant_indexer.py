"""
Module for indexing grant descriptions using LlamaIndex.

This module handles the following tasks:

- Creating a LlamaIndex knowledge base from grant descriptions.
- Choosing appropriate index types (e.g., GPTIndex, GPTListIndex) based on the data structure and search requirements.
- Configuring embedding models (e.g., OpenAI's text-embedding-ada-002) for efficient search.
- Saving and loading the index for persistent storage.
"""
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingMode, OpenAIEmbeddingModelType
from sqlalchemy import make_url

import psycopg2
import openai
import os

import log

# Set up global logging for the application
logger = log.setup_custom_logger("grant_indexer")
logger.debug("Logging set up for grant_indexer module")

def debug_db(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT table_name from information_schema.tables WHERE table_schema='public' AND table_type = 'BASE TABLE';")
        for row in cur.fetchall():
            print(row)

openai.api_key = os.environ["OPENAI_API_KEY"]

# Connect to your PostgreSQL database
connection_string = "postgresql://testuser:testpwd@localhost:5432/vectordb" # format: "postgresql://user:password@host:port"
db_name = "vectordb"
conn = psycopg2.connect(connection_string)
conn.autocommit = True

with conn.cursor() as cur:
    # Create a table for the items
    #cur.execute("DROP TABLE IF EXISTS grants;")
    # Embedding vector is a vector of 1536 dimensions
    #cur.execute("CREATE TABLE grants (id SERIAL PRIMARY KEY, embedding vector(1536), created_at TIMESTAMPTZ DEFAULT now());")
    pass

grants = SimpleDirectoryReader("./datasss/grants/").load_data()
logger.debug(f"Loaded {len(grants)} grants")
logger.debug(f"Document ID: {grants[0].doc_id}")

# Create a LlamaIndex from the grant descriptions
url = make_url(connection_string)
vector_store = PGVectorStore.from_params(
    database=db_name,
    host=url.host,
    password=url.password,
    port=url.port,
    user=url.username,
    schema_name='public',
    ##table_name="grants",

    embed_dim=512, # OpenAI's text-embedding-3-small model can be set to 512 dimensions
    hnsw_kwargs={ # HNSW parameters for efficient search, HNSW = Hierarchical Navigable Small World
        "hnsw_m" : 16,
        "hnsw_ef_construction" : 64,
        "hnsw_ef_search" : 40,
        "hnsw_dist_method" : "vector_cosine_ops",
    },
)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
debug_db(conn)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimensions=512)
debug_db(conn)
index = VectorStoreIndex.from_documents(grants, storage_context=storage_context, show_progress=True)
debug_db(conn)
# commit the transaction

query_engine = index.as_query_engine()

logger.debug("Indexing complete")

# Save the index to database

result = index.as_query_engine().query("Grant na ochrone środowiska")
print(result,"\n")
print(result.response)

# Query the database and return the top 4 results

