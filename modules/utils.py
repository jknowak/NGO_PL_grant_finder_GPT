"""
Module for utility functions used throughout the project.

This module contains helper functions for:

- File handling (reading, writing, and processing files).
- Data manipulation (cleaning, transforming, and formatting data).
- Logging (recording events and debugging information).
- Other common tasks that are used in multiple parts of the project.
"""

import json

class Grant():
    def __init__(self, doc_id, text):
        self.doc_id = doc_id
        self.text = text
        self.embedding = None
        self.embedding_dim = None

    def from_dict(self, data):
        self.doc_id = data.get("doc_id")
        self.text = data.get("text")
        self.embedding = data.get("embedding")
        self.embedding_dim = data.get("embedding_dim")
    
    def from_json(self, json_str):
        data = json.loads(json_str)
        self.from_dict(data)