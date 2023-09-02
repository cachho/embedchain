from typing import Callable

from embedchain.config.vectordbs.BaseVectorDbConfig import BaseVectorDbConfig
from embedchain.embedder.embedder import Embedder


class BaseVectorDB:
    """Base class for vector database."""

    def __init__(self):
        self.client = self._get_or_create_db()
        self._get_or_create_collection()
        self.config: BaseVectorDbConfig

    def _get_or_create_db(self):
        """Get or create the database."""
        raise NotImplementedError

    def _get_or_create_collection(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def add(self):
        raise NotImplementedError

    def query(self):
        raise NotImplementedError

    def count(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def set_collection_name(self, name: str):
        self.config.collection_name = name

    def _set_embedder(self, embedder: Embedder):
        self.embedder = embedder
