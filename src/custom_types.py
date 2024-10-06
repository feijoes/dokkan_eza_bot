from typing import NamedTuple, Union


class ImageLocation(NamedTuple):
    found: bool
    x: Union[int, None]
    y: Union[int, None]


class DuelImageLocation(NamedTuple):
    which: int
    x: Union[int, None]
    y: Union[int, None]
