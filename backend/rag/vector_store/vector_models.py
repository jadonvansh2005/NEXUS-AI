from dataclasses import dataclass

from typing import Dict


@dataclass
class CollectionConfig:

    name: str

    vector_size: int

    distance: str


COLLECTIONS: Dict[

    str,

    CollectionConfig

] = {

    "conversation": CollectionConfig(

        name="conversation_vectors",

        vector_size=1024,

        distance="Cosine"

    ),

    "document": CollectionConfig(

        name="document_vectors",

        vector_size=1024,

        distance="Cosine"

    ),

    "semantic": CollectionConfig(

        name="semantic_vectors",

        vector_size=1024,

        distance="Cosine"

    ),

    "project": CollectionConfig(

        name="project_vectors",

        vector_size=1024,

        distance="Cosine"

    ),

    "knowledge": CollectionConfig(

        name="knowledge_vectors",

        vector_size=1024,

        distance="Cosine"

    ),

    "code": CollectionConfig(

        name="code_vectors",

        vector_size=1024,

        distance="Cosine"

    ),

    "episodic": CollectionConfig(

        name="episodic_vectors",

        vector_size=1024,

        distance="Cosine"

    )

}