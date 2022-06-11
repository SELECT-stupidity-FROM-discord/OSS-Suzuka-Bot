from datetime import datetime
from functools import cache
from typing import Any, Dict, List, Optional, TypeVar, Union

from utils.helpers import Command
from utils.helpers.consts import MISSING


D = TypeVar('D', bound=Dict[Command, datetime])
P = TypeVar('P', bound=Dict[int, Optional[Union[List[str], MISSING]]])

class MainCache:
    def __init__(self, cache: Dict[str, Any]):
        self.cache = cache

    def get(self, key) -> Optional[Any]:
        return self.cache.get(key, None)

    def __getitem__(self, key: str) -> Any:
        return getattr(self.cache, key)

    def __getattribute__(self, __name: str) -> Any:
        return object.__getattribute__(self, 'cache')[__name]


class PrefixCache:
    def __init__(self, cache: P) -> None:
        self.cache = cache

    def get(self, key: int) -> Union[List[str], MISSING]:
        to_return = self.cache.get(key)
        if not to_return:
            to_return = MISSING
            self.cache[key] = to_return
        return to_return

    def __in__(self, key: str) -> bool:
        return key in self.cache



class HaremCache:
    def __init__(self, cache: Dict[str, Any]):
        self.cache = cache

    def get(self, key) -> Optional[Dict[str, Any]]:
        return self.cache.get(key)

    def set(self, key: str, value: Optional[Dict[str, Any]]):
        self.cache[key] = value

    def __in__(self, key: int) -> bool:
        return key in self.cache


class CooldownCache:
    def __init__(
        self, 
        cache: Dict[int, D]
        ):
        self.cache = cache

    def get(self, key: int) -> Optional[D]:
        return self.cache.get(key, None)

    def set(self, key: int, value: D):
        self.cache[key] = value

    def __in__(self, key: int) -> bool:
        return key in self.cache

class PPCache:
    def __init__(self, cache: Dict[int, int]):
        self.cache = cache

    def get(self, key) -> Optional[int]:
        return self.cache.get(key, None)

    def set(self, key: int, value: int):
        self.cache[key] = value

    def __in__(self, key: int) -> bool:
        return key in self.cache

class SubscriptionCache:
    def __init__(self, cache: Dict[int, int]):
        self.cache = cache

    def get(self, key) -> Optional[int]:
        return self.cache.get(key, None)

    def set(self, key: int, value: int):
        self.cache[key] = value

    def __in__(self, key: int) -> bool:
        return key in self.cache
