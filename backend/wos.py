"""
Module that provides a class to retrieve papers from the Web of Science api.
"""
import backend
from backend import utils


class WOSBackend(backend.PaperSource):
    """Backend that retrieves papers from the Web of Science api."""
    def _ensure_exists(self):
        """Ensure that there is a stable connection to the WOS api."""
        if not utils.has_internet():
            raise NotImplementedError("Currently not online.")

    @utils.before_method(_ensure_exists)
    def get_paper(self, key: str, ref: dict[str, str]) -> backend.Paper:
        """."""
        raise NotImplementedError("Not implemented YET.")

    def post_paper(self, papr: backend.Paper):
        """."""
        raise NotImplementedError("Unable to post to read-only database.")
