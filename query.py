"""
Module that is responsible for defining backends and calling them appropriatly.
"""
import base_classes
import backend

available_db: list[base_classes.Library] = [
    base_classes.Library(bck=backend.LocalBackend()),
    base_classes.Library(bck=backend.WOSBackend()),
    base_classes.Library(bck=backend.GuessingBackend())
]


# TODO: This is a really bad function at this point. Refactor so that
# paper.load does not have to be called and saving the paper has to be called
# from somewhere else.
def aquire_paper(key: str, ref: dict) -> bytes:
    """High-level function to retrieve paper or raise an Error."""
    for dtb in available_db:
        print(f"Backend {dtb=} ", end='')
        try:
            paper = dtb.get_paper(key, ref)
        except NotImplementedError as err:
            print(f"can't find the file:\n{err}")
            continue
        print(f"found {paper=}.")
        save_paper(paper)
        with paper.load() as buf:
            return b''.join(buf.readlines())
    raise ValueError("No suitable bibtex keys found.")


def save_paper(papr: backend.Paper):
    """High-level function to save a paper to all possible databases."""
    for dtb in available_db:
        print(f"Backend {dtb=} ", end='')
        try:
            dtb.post_paper(papr)
            print("saved succesfully.")
        except NotImplementedError as err:
            print(f"can't save:\n{err}")
