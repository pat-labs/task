from typing import NamedTuple

from src.domain.enum.LinkedMetadataKey import LinkedMetadataKey
from src.domain.enum.TaskLinkedKey import TaskLinkedKey


class LinkedItem(NamedTuple):
    linked_key: TaskLinkedKey
    url: str
    metadata_type: LinkedMetadataKey
    value: str
