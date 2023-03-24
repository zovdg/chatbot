from .base import DB

from typing import Any, Optional


class InMemoryDB(DB):
    def __init__(self):
        self.stores = {}

    def set(self, key: str, value: Any):
        """Set key/value to db."""
        self.stores[key] = value

    def get(self, key: str) -> Optional[Any]:
        """Get value from db by key."""
        return self.stores.get(key)

    def delete(self, key: str):
        """Delete value from db by key."""
        if key in self.stores:
            del self.stores[key]

    def update(self, key: str, value: Any):
        """Update value in db by key and new value."""
        self.stores[key] = value

    def exist(self, key: str) -> bool:
        """Check key is in db or not."""
        return key in self.stores
