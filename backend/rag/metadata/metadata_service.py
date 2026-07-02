from typing import Any
from typing import Dict

from rag.metadata.base_metadata import (
    BaseMetadata
)

from rag.metadata.metadata_factory import (
    MetadataFactory
)

from rag.metadata.metadata_validator import (
    MetadataValidator
)


class MetadataService:


    @staticmethod
    def create(

        source: str,

        **kwargs: Dict[str, Any]

    ) -> BaseMetadata:

        metadata = (

            MetadataFactory.create(

                source=source,

                **kwargs

            )

        )

        MetadataValidator.validate(

            metadata

        )

        return metadata


    @staticmethod
    def update(

        metadata: BaseMetadata,

        **kwargs: Dict[str, Any]

    ) -> BaseMetadata:

        for key, value in kwargs.items():

            if hasattr(

                metadata,

                key

            ):

                setattr(

                    metadata,

                    key,

                    value

                )

        metadata.update_timestamp()

        MetadataValidator.validate(

            metadata

        )

        return metadata


    @staticmethod
    def validate(

        metadata: BaseMetadata

    ) -> None:

        MetadataValidator.validate(

            metadata

        )


    @staticmethod
    def to_dict(

        metadata: BaseMetadata

    ) -> Dict[str, Any]:

        MetadataValidator.validate(

            metadata

        )

        return (

            metadata.to_dict()

        )


    @staticmethod
    def clone(

        metadata: BaseMetadata

    ) -> BaseMetadata:

        metadata_dict = (

            metadata.to_dict()

        )

        metadata_dict.pop(

            "created_at",

            None

        )

        metadata_dict.pop(

            "updated_at",

            None

        )

        metadata_dict.pop(

            "extra",

            None

        )

        return MetadataFactory.create(

            source=metadata.source,

            **metadata_dict

        )


    @staticmethod
    def add_extra(

        metadata: BaseMetadata,

        key: str,

        value: Any

    ) -> None:

        metadata.add_extra(

            key,

            value

        )


    @staticmethod
    def get_extra(

        metadata: BaseMetadata,

        key: str,

        default: Any = None

    ) -> Any:

        return (

            metadata.get_extra(

                key,

                default

            )

        )