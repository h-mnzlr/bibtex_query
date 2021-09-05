"""
Module that supplies base classes to deal with sources and papers.
"""
import io
import contextlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generator

from backend import utils


@dataclass
class Paper:
    """Implements an abstract representation of a paper to resolve later."""
    key: str = ''
    ref: dict = field(default_factory=lambda: {})
    data_lzy: utils.LazyInStream = lambda: io.BufferedReader(io.RawIOBase())

    @contextlib.contextmanager
    def load(self) -> Generator[io.BufferedReader, None, None]:
        """Load data for a paper as a I/O stream."""
        data_stream = self.data_lzy()
        if not data_stream.readable():
            raise NotImplementedError("Paper data cannot be read.")
        try:
            yield data_stream
        finally:
            data_stream.close()


class PaperSource(ABC):
    """Implements an interface to retrieve papers from a particular source."""
    @abstractmethod
    def _ensure_exists(self):
        """Ensure that the source is available."""

    @abstractmethod
    def get_paper(self, key: str, ref: dict[str, str]) -> Paper:
        """Retrieve a paper from source."""

    @abstractmethod
    def post_paper(self, papr: Paper):
        """Post a paper to source or raise a NotImplementedError if unable."""
