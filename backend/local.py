import os
from dataclasses import dataclass
from pathlib import Path

import backend
import backend.utils as utils

from typing import Callable

DEFAULT_DIR = Path(
    os.environ.get('XDG_CACHE_HOME', default='~/.cache')
) / 'bibtex_library'


@dataclass
class LocalBackend(backend.PaperSource):
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
    def post_paper(self, pa: backend.Paper):
        file_path = self.base_dir / self.naming_convention(pa.key, 'pdf')
        if file_path.exists():
            raise NotImplementedError(f"{file_path=} already exists.")
        utils.pipe_stream(pa.data_lzy, lambda: open(file_path, 'wb'))
