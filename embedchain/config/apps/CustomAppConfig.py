import logging
from typing import Any

from chromadb.api.types import Documents, Embeddings
from dotenv import load_dotenv

from embedchain.models import EmbeddingFunctions, Providers

from .BaseAppConfig import BaseAppConfig
from embedchain.models import Providers

load_dotenv()


class CustomAppConfig(BaseAppConfig):
    """
    Config to initialize an embedchain custom `App` instance, with extra config options.
    """

    def __init__(
        self,
        log_level=None,
        embedding_fn: EmbeddingFunctions = None,
        embedding_fn_model = None,
        db=None,
        host=None,
        port=None,
        id=None,
        provider: Providers = None,
        model=None,
        open_source_app_config=None
    ):
        """
        :param log_level: Optional. (String) Debug level
        ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'].
        :param embedding_fn: Optional. Embedding function to use.
        :param embedding_fn_model: Optional. Model name to use for embedding function.
        :param db: Optional. (Vector) database to use for embeddings.
        :param id: Optional. ID of the app. Document metadata will have this id.
        :param host: Optional. Hostname for the database server.
        :param port: Optional. Port for the database server.
        :param provider: Optional. (Providers): LLM Provider to use.
        :param open_source_app_config: Optional. Config instance needed for open source apps.
        """
        if provider:
            self.provider = provider
        else:
            raise ValueError("CustomApp must have a provider assigned.")

        self.model = model

        self.open_source_app_config = open_source_app_config

        super().__init__(
            log_level=log_level,
            embedding_fn=CustomAppConfig.embedding_function(embedding_function=embedding_fn),
            db=db,
            host=host,
            port=port,
            id=id,
        )

    @staticmethod
    def langchain_default_concept(embeddings: Any):
        """
        Langchains default function layout for embeddings.
        """

        def embed_function(texts: Documents) -> Embeddings:
            return embeddings.embed_documents(texts)

        return embed_function

    @staticmethod
    def embedding_function(embedding_function: EmbeddingFunctions, model: str = None):
        if not isinstance(embedding_function, EmbeddingFunctions):
            raise ValueError(
                f"Invalid option: '{embedding_function}'. Expecting one of the following options: {list(map(lambda x: x.value, EmbeddingFunctions))}"  # noqa: E501
            )

        if embedding_function == EmbeddingFunctions.OPENAI:
            from langchain.embeddings import OpenAIEmbeddings

            embeddings = OpenAIEmbeddings()
            return CustomAppConfig.langchain_default_concept(embeddings)

        elif embedding_function == EmbeddingFunctions.HUGGING_FACE:
            from langchain.embeddings import HuggingFaceEmbeddings

            embeddings = HuggingFaceEmbeddings()
            return CustomAppConfig.langchain_default_concept(embeddings)

        elif embedding_function == EmbeddingFunctions.VERTEX_AI:
            from langchain.embeddings import VertexAIEmbeddings

            embeddings = VertexAIEmbeddings()
            return CustomAppConfig.langchain_default_concept(embeddings)
        
        elif embedding_function == EmbeddingFunctions.GPT4ALL:
            from chromadb.utils import embedding_functions
            return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model)
