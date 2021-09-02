import io
import contextlib
import functools
import slugify  # type: ignore
import requests as re  # type: ignore
from pathlib import Path

from typing import Callable, Any

LazyInStream = Callable[[], io.BufferedReader]
LazyOutStream = Callable[[], io.BufferedWriter]
Method = Callable[..., Any]


def has_internet() -> bool:
    """Check if internet connection is available."""
    try:
        _ = re.head('http://google.com', timeout=5)
        return True
    except ConnectionError:
        return False


def craft_request(base: str, *append: str, **params: Any) -> functools.partial:
    """Craft a request partial, that can be invoked to execute the request."""
    url = append_url(base, *append)
    return functools.partial(re.get, url, params=params)


# TODO: This is unused
def download_file(req_partial: functools.partial, target_path: Path):
    """Download a file with proper exeption handling."""
    with contextlib.ExitStack() as stack:
        r = stack.enter_context(req_partial(stream=True))
        r.raise_for_status()
        try:
            f = stack.enter_context(open(target_path, 'wb'))
            for chunk in r.iter_content():
                f.write(chunk)
        except ConnectionError:
            print("Connection failed. Removing brocken download file.")
            target_path.unlink(missing_ok=True)


# TODO: This is unused
def download_file_prepare(file_url: str, target_path: Path, **payload):
    """Download a file to target path."""
    req_part = craft_request(file_url, **payload)
    return download_file(req_part, target_path)


def append_url(url: str, *path_param: str) -> str:
    """Helper function to append params to url path."""
    for p in path_param:
        url += '/' + p
    return url


def naming_convention(ref: str, extension: str = 'pdf') -> Path:
    """Slugify a filename and make it fit the chosen naming convention."""
    slug_file = slugify.slugify(ref)
    return Path(slug_file + '.' + extension)


def pipe_stream(in_stream_lzy: LazyInStream, out_stream_lzy: LazyOutStream):
    with contextlib.ExitStack() as stack:
        reader = stack.enter_context(in_stream_lzy())
        writer = stack.enter_context(out_stream_lzy())
        for chunk in reader:
            writer.write(chunk)


def before_method(meth_before: Method) -> Callable[[Method], Method]:
    def decorator(meth: Method) -> Any:
        @functools.wraps(meth)
        def inner(self, *args: Any, **kwargs: Any):
            meth_before(self)
            return meth(self, *args, **kwargs)

        return inner

    return decorator
