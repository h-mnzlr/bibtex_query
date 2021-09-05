"""
Module providing utility functions for the high-level program flow.
"""
import os
import sys
import subprocess


def open_browser(url: str):
    """Open a list of urls with BROWSER env executable (chromium if unset)."""
    browser_cmd = os.environ["BROWSER"] or "chromium"
    with subprocess.Popen([browser_cmd, url]):
        pass


def open_pdf(data: bytes):
    """Open pdf using zathura."""
    with subprocess.Popen(['zathura', '-'], stdin=subprocess.PIPE) as proc:
        proc.communicate(input=data)


def read_stdin() -> bytes:
    """Read bytes from stdin."""
    with sys.stdin.buffer as buf:
        return b''.join(buf.readlines())
