"""
Module for indexing grant descriptions using LlamaIndex.

This module handles the following tasks:

- Creating a LlamaIndex knowledge base from grant descriptions.
- Choosing appropriate index types (e.g., GPTIndex, GPTListIndex) based on the data structure and search requirements.
- Configuring embedding models (e.g., OpenAI's text-embedding-ada-002) for efficient search.
- Saving and loading the index for persistent storage.
"""
import os

import openai
from llama_index.core import SimpleDirectoryReader, Settings, OpenAIEmbedding, OpenAIEmbeddingMode, OpenAIEmbeddingModelType
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI

import log
import config
import modules.vector_store_index as vsi


# Set up global logging for the application
logger = log.setup_custom_logger("grant_indexer")
logger.debug("Logging set up for grant_indexer module")

openai.api_key = os.environ["OPENAI_API_KEY"]


grants = SimpleDirectoryReader("./data/grants/").load_data()
logger.debug(f"Loaded {len(grants)} grants")
logger.debug(f"Document ID: {grants[0].doc_id}")

# Set up the OpenAI embedding model
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
Settings.num_output = 512
Settings.context_window = 3900
# commit the transaction

index = vsi.create_vector_store_index()

# Add grants to the index as nodes
for grant in grants:
    index.add_document(grant)

# Index the grants
index.index()

logger.debug("Indexing complete")

# Save the index to storage folder
index.save("./data/index/")
logger.debug("Index saved in data/index/")

# Query the database and return the top 4 results

