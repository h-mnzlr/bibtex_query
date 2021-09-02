# bibtex_query

This started as a simple script to automate the workflow of manual downloading
papers. Note that this is _not_ a means to download papers in bulk but a simple
script to automate downloading single pdf's at a time. Consult the TOS for
your respective providers to find out what they allow and what they do not
want you to do!

# Usage:

Simply pipe some bibtex string into the script, and let it try to retrieve the
paper for you. Doing so the script employs different (extendable) backends, like
caching them as pdf files in a local library folder or downloading them from
various sites (that you need access to).
We employ structural pattern matching to guess the correct url's to download
the papers directly, so this script _needs_ python 3.10 to function properly. Note
that this makes it easy to get a particular website supported: Simply match
your url properly and craft a request to retrieve the pdf directly.

# Install:

For now you need to manually install the script so do
`pip install -r requirements.txt` and link `query_bibtex.py` into your `PATH`.

# Dependencies:

- _Python 3.10 !_
- To open pdf's automatically you will need a pdf viewer capable of reading from
  stdin, as the downloaded pdf will be directly piped into the reader. `zathura`
  is used in this implementation. You can change the binary by editing
  `utils.open_pdf()`.

# Future:

- We aim to support a Web of Science backend using their api which can also help
  you to download cited references for a paper, to enable you to _manually_ (!)
  look up references cited in your paper.
- Neovim plugin to search directly from your `.bib` file.
