import backend
import backend.utils as utils


class GScholarBackend(backend.PaperSource):
    G_SCHOLAR_QUERY = "https://scholar.google.com/scholar?hl=en&q={}"

    def _ensure_exists(self):
        try:
            utils.craft_request('http://8.8.8').__call__()
        except ConnectionError:
            raise NotImplementedError("No network connection.")
