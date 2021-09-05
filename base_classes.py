"""
Provides a library class that is an abstraction layer for an backend.
"""
from dataclasses import dataclass

import backend
import backend.utils


@dataclass
class Library:
    """Abstract base class to interface a database for papers."""
    bck: backend.PaperSource = backend.LocalBackend()

    def get_paper(self, key: str, ref: dict) -> backend.Paper:
        """Retrieve a paper from the database or None if unable."""
        return self.bck.get_paper(key, ref)

    def post_paper(self, papr: backend.Paper):
        """Save a paper to the database."""
        self.bck.post_paper(papr)
