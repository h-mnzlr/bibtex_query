import backend
import backend.utils as utils


class WOSBackend(backend.PaperSource):
    def _ensure_exists(self):
        if not utils.has_internet():
            raise NotImplementedError("Currently not online.")

    @utils.before_method(_ensure_exists)
    def get_paper(self, key: str, ref: dict[str, str]) -> backend.Paper:
        raise NotImplementedError("Not implemented YET.")

    def post_paper(self, pa: backend.Paper):
        raise NotImplementedError("Unable to post to read-only database.")
