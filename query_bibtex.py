#!/usr/bin/python3.10
"""Short script too open an url from a bibtex object passed via stdin."""

import bibtexparser  # type: ignore

import query
import utils

G_SCHOLAR_QUERY = "https://scholar.google.com/scholar?hl=en&q={}"


def read_bib_stdin() -> bibtexparser.bibdatabase.BibDatabase:
    """Read stdin into a BibDatabase object."""
    bib_string = utils.read_stdin().decode('utf-8')
    bibtex = bibtexparser.loads(bib_string)
    return bibtex


def main():
    bib_db = read_bib_stdin()
    for key, ref in bib_db.get_entry_dict().items():
        try:
            paper_data = query.aquire_paper(key, ref)
            utils.open_pdf(paper_data)
        except NotImplementedError:
            print("Unable to guess path to pdf url.")
            utils.open_browser(ref['url'])
        except ValueError:
            print("No url entry found.")
            utils.open_browser(G_SCHOLAR_QUERY.format(ref['title']))


if __name__ == "__main__":
    main()
