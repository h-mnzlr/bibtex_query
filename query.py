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
    for db in available_db:
        print(f"Backend {db=} ", end='')
        try:
            paper = db.get_paper(key, ref)
        except NotImplementedError as e:
            print(f"can't find the file:\n{e}")
            continue
        print(f"found {paper=}.")
        save_paper(paper)
        with paper.load() as buf:
            return b''.join(buf.readlines())
    raise ValueError("No suitable bibtex keys found.")


def save_paper(pa: backend.Paper):
    """High-level function to save a paper to all possible databases."""
    for db in available_db:
        print(f"Backend {db=} ", end='')
        try:
            db.post_paper(pa)
            print("saved succesfully.")
        except NotImplementedError as e:
            print(f"can't save:\n{e}")
