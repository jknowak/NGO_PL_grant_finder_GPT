from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings, StorageContext
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingMode, OpenAIEmbeddingModelType
from sqlalchemy import make_url
from llama_index.core import (
    load_index_from_storage,
    load_indices_from_storage,
    load_graph_from_storage,
)

import psycopg2
import os
from dotenv import load_dotenv

import log
import config
import db

# Set up global logging for the application
logger = log.setup_custom_logger("vector_store")
logger.debug("Logging set up for vector_store module")

load_dotenv()


class MyVectorStoreIndex(VectorStoreIndex):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage_context = None
        if config.VECTOR_STORE_TYPE == "postgres":
            self.vector_store = self.create_pg_vs()
            self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        index = VectorStoreIndex.from_documents(documents=[], storage_context=self.storage_context)

        return index

    def create_pg_vs():
        """ 
        Create a vector store from grant descriptions.

        This function creates a vector store from grant descriptions and
        returns the vector store object.

        Returns:
            VectorStoreIndex: A vector store object containing grant descriptions.
        """
    
        raise NotImplementedError("This function is not implemented yet.")

        vector_store = PGVectorStore(
            url=make_url(os.environ["DATABASE_URL"]),
            vector_size=512,
            insert_batch_size=1000,
        )

        return vector_store



