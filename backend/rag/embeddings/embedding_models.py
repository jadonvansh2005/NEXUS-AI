import os
from dataclasses import dataclass
from typing import Optional, Dict

# Dynamically resolve project root: D:\UPSS\backend
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Hugging Face cache directories globally to keep C: drive clean
os.environ["HF_HOME"] = os.path.join(PROJECT_ROOT, "models", "huggingface")
os.environ["SENTENCE_TRANSFORMERS_HOME"] = os.path.join(PROJECT_ROOT, "models", "sentence_transformers")


@dataclass
class EmbeddingModelConfig:

    model_name: str

    provider: str

    dimension: int

    max_tokens: int

    supports_dense: bool

    supports_sparse: bool

    supports_multivector: bool

    multilingual: bool

    local_model: bool

    cache_folder: Optional[str] = None


SUPPORTED_MODELS: Dict[

    str,

    EmbeddingModelConfig

] = {

    "bge_m3": EmbeddingModelConfig(

        model_name="BAAI/bge-m3",

        provider="huggingface",

        dimension=1024,

        max_tokens=8192,

        supports_dense=True,

        supports_sparse=True,

        supports_multivector=True,

        multilingual=True,

        local_model=True,

        cache_folder=os.path.join(PROJECT_ROOT, "models", "embeddings")

    ),

    "bge_base": EmbeddingModelConfig(

        model_name="BAAI/bge-base-en-v1.5",

        provider="huggingface",

        dimension=768,

        max_tokens=512,

        supports_dense=True,

        supports_sparse=False,

        supports_multivector=False,

        multilingual=False,

        local_model=True,

        cache_folder=os.path.join(PROJECT_ROOT, "models", "embeddings")

    )

}


DEFAULT_MODEL = "bge_m3"