"""
Provide a class representing a backend based on the local filesystem.
"""
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import backend
from backend import utils

DEFAULT_DIR = Path(
    os.environ.get('XDG_CACHE_HOME', default='~/.cache')
) / 'bibtex_library'


@dataclass
class LocalBackend(backend.PaperSource):
    """Papersource that uses a local file-based structure to save papers."""
    base_dir: Path = DEFAULT_DIR
    naming_convention: Callable[[str, str], Path] = utils.naming_convention

    def _ensure_exists(self):
        if self.base_dir.exists():
            return
        self.base_dir.mkdir(parents=True)

    @utils.before_method(_ensure_exists)
    def get_paper(self, key: str, ref: dict[str, str]) -> backend.Paper:
        file_path = self.base_dir / self.naming_convention(key, 'pdf')
        if not file_path.exists():
            raise NotImplementedError(f"{file_path=} does not exist.")
        return backend.Paper(key, ref, lambda: open(file_path, 'rb'))

    @utils.before_method(_ensure_exists)
    def post_paper(self, papr: backend.Paper):
        file_path = self.base_dir / self.naming_convention(papr.key, 'pdf')
        if file_path.exists():
            raise NotImplementedError(f"{file_path=} already exists.")
        utils.pipe_stream(papr.data_lzy, lambda: open(file_path, 'wb'))
