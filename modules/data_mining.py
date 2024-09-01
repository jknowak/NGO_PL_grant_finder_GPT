"""
Module for loading, cleaning, and preprocessing grant and project data.

This module handles the following tasks:

- Loading data from files (JSON, CSV, etc.).
- Cleaning data: removing irrelevant information, standardizing formatting, handling missing values.
- Preprocessing data: applying techniques like stemming, lemmatization, stop word removal to improve search accuracy.
- Transforming data into a format suitable for indexing and analysis.
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
