import requests as re
import functools


import backend
import backend.utils as utils
from .utils import craft_request


class GuessingBackend(backend.PaperSource):
    def _ensure_exists(self):
        if not utils.has_internet():
            raise NotImplementedError("No internet available.")


    @utils.before_method(_ensure_exists)
    def get_paper(self, key: str, ref: dict[str, str]) -> backend.Paper:
        if not (url := ref.get('url')):
            raise NotImplementedError(f"No key url found in {ref=}.")
        req_part = self.guess_pdf_location(url)
        return backend.Paper(key, ref, lambda: req_part(stream=True).raw)

    def post_paper(self, _: backend.Paper):
        raise NotImplementedError("Unable to post to read-only database.")

    @classmethod
    def guess_pdf_location(cls, url: str) -> functools.partial:
        """Employ structural pattern matching to guess pdf location given url."""
        body = url.split('//')[-1]
        match body.split('/'):
            case ['doi.org', *_] | ['dx.doi.org', *_] | ['link.aps.org', 'doi', *_]:
                return cls.guess_pdf_location(re.get(url).url)  # redirected url
            case ['dl.acm.org', 'doi', *params]:
                return craft_request('https://dl.acm.org/doi/pdf', *params)
            case ['aip.scitation.org', 'doi', *params]:
                return craft_request('https://aip.scitation.org/doi/pdf', *params)
            case ['journals.aps.org', 'prl', 'abstract', *params]:
                return craft_request('https://journals.aps.org/prl/pdf', *params)
            case ['journals.aps.org', 'pre', 'abstract', *params]:
                return craft_request('https://journals.aps.org/pre/pdf', *params)
            case ['link.springer.com', 'article', *params]:
                return craft_request('https://link.springer.com/content/pdf', *params)
            case _:
                raise NotImplementedError

    @classmethod
    def guess_ref_location(cls, url: str) -> functools.partial:
        """Employ structural pattern matching to guess pdf location given url."""
        body = url.split('//')[-1]
        match body.split('/'):
            case ['doi.org', *_] | ['dx.doi.org', *_]:
                return cls.guess_ref_location(re.get(url).url)  # redirected url
            # case ['link.springer.com', 'article', *params]:
            #     return append_url('https://citation-needed.springer.com/content/pdf', *params)
            # case ['dl.acm.org', 'doi', *params]:
            #     return append_url('https://dl.acm.org/doi/pdf', *params)
            # case ['aip.scitation.org', 'doi', *params]:
            #     return append_url('https://aip.scitation.org/doi/pdf', *params)
            # case ['journals.aps.org', 'prl', 'abstract', *params]:
            #     return append_url('https://journals.aps.org/prl/export', *params)
            case _:
                raise NotImplementedError
