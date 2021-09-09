"""
Provide a Backend that tries to guess pdf location from the ref provided.
"""
import requests as re
import functools


import backend
from backend import utils
from backend.utils import craft_request


class GuessingBackend(backend.PaperSource):
    """Backend that tries to guess a paper location on internet."""

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

    @staticmethod
    def guess_pdf_location(url: str) -> functools.partial:
        """Use structural pattern matching to guess pdf location given url."""
        body = url.split('//')[-1]
        match body.split('/'):
            case['doi.org', *_] | ['dx.doi.org', *_] | ['link.aps.org', 'doi', *_]:
                # redirected url
                return GuessingBackend.guess_pdf_location(re.get(url).url)
            case['dl.acm.org', 'doi', *params]:
                return craft_request('https://dl.acm.org/doi/pdf', *params)
            case['aip.scitation.org', 'doi', *params]:
                return craft_request('https://aip.scitation.org/doi/pdf', *params)
            case['epubs.siam.org', 'doi', 'abs', *params]:
                return craft_request('https://epubs.siam.org/doi/pdf', *params)
            case['journals.aps.org', 'prl', 'abstract', *params]:
                return craft_request('https://journals.aps.org/prl/pdf', *params)
            case['journals.aps.org', 'pre', 'abstract', *params]:
                return craft_request('https://journals.aps.org/pre/pdf', *params)
            case['link.springer.com', 'article', *params]:
                return craft_request('https://link.springer.com/content/pdf', *params)
            case _:
                raise NotImplementedError

    @staticmethod
    def guess_ref_location(url: str) -> functools.partial:
        """Use structural pattern matching to guess pdf location given url."""
        body = url.split('//')[-1]
        match body.split('/'):
            case['doi.org', *_] | ['dx.doi.org', *_]:
                # redirected url
                return GuessingBackend.guess_ref_location(re.get(url).url)
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
