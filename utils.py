import os
import sys
import subprocess


def open_browser(url: str):
    """Open a list of urls with BROWSER env executable (chromium if unset)."""
    browser_cmd = os.environ["BROWSER"] or "chromium"
    subprocess.Popen([browser_cmd, url])


def open_pdf(data: bytes):
    """Open pdf using zathura."""
    pdf_view = subprocess.Popen(['zathura', '-'], stdin=subprocess.PIPE)
    pdf_view.communicate(input=data)


def read_stdin() -> bytes:
    """Read bytes from stdin."""
    with sys.stdin.buffer as buf:
        return b''.join(buf.readlines())


# TODO: unused
def write_stdout(b: bytes):
    """Write bytes to stdout."""
    with sys.stdout.buffer as buf:
        buf.write(b)
