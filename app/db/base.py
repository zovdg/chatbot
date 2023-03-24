import abc

from typing import Any, Optional


class DB(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set(self, key: str, value: Any):
        """Set key/value to db."""

    @abc.abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value from db by key."""

    @abc.abstractmethod
    def delete(self, key: str):
        """Delete value from db by key."""

    @abc.abstractmethod
    def update(self, key: str, value: Any):
        """Update value in db by key and new value."""

    @abc.abstractmethod
    def exist(self, key: str) -> bool:
        """Check key is in db or not."""
