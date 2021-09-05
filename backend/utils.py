"""
Provides utility functions specific for functionalities of the backends.
"""
import io
import functools
from pathlib import Path
from typing import Callable, Any

import requests as re  # type: ignore
import slugify  # type: ignore

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


def append_url(url: str, *path_params: str) -> str:
    """Helper function to append params to url path."""
    for param in path_params:
        url += '/' + param
    return url


def naming_convention(ref: str, extension: str = 'pdf') -> Path:
    """Slugify a filename and make it fit the chosen naming convention."""
    slug_file = slugify.slugify(ref)
    return Path(slug_file + '.' + extension)


def pipe_stream(in_stream_lzy: LazyInStream, out_stream_lzy: LazyOutStream):
    """Pipe in stream into out stream."""
    with in_stream_lzy() as reader, out_stream_lzy() as writer:
        for chunk in reader:
            writer.write(chunk)


def before_method(meth_before: Method) -> Callable[[Method], Method]:
    """Decorator to execute a passed method before another method."""
    def decorator(meth: Method) -> Any:
        @functools.wraps(meth)
        def inner(self, *args: Any, **kwargs: Any):
            meth_before(self)
            return meth(self, *args, **kwargs)

        return inner

    return decorator
