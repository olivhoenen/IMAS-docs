# Contributing

Contributions of all sizes are welcome: a user story, a typo fix, a new page.
Please follow the [Code of Conduct](https://github.com/olivhoenen/IMAS-docs/blob/main/CODE_OF_CONDUCT.md).

## From a user story to a page

1. **Open or find a user story.** Search the
   [issues labelled `user-story`](https://github.com/olivhoenen/IMAS-docs/issues?q=label%3Auser-story);
   if yours isn't there, [open one](https://github.com/olivhoenen/IMAS-docs/issues/new?template=user_story.yml).
2. **Triage.** Maintainers discuss the story in the issue, then label it `accepted` and assign it
   (to you if you offered to write it).
3. **Write the page.** Copy `docs/_templates/user-story.md` to `docs/user-stories/<short-name>.md`,
   fill it in, and add it to the list in `docs/user-stories/index.md`.
4. **Open a pull request** that says `Closes #<issue>`. A bot comments a link to a preview of
   the rendered site, updated at every push.
5. **Review and merge.** Once merged, the page is published automatically.

Small fixes don't need an issue: use the pencil icon on any page of the site to edit it on
GitHub and open a pull request directly.

## Content rules

- **Open to everyone.** Install from PyPI, use open data (e.g. the
  [open-imas community on Zenodo](https://zenodo.org/communities/open-imas/)). No instructions
  specific to one computing site (cluster paths, environment modules, internal servers).
- **Hub, not copy.** Explain the idea, show a short example, then link to the documentation of
  the relevant software. Don't duplicate API or reference documentation.
- **Examples must run.** Python examples are `{code-cell}` blocks, executed at every build.
  Examples in other languages are plain code blocks, checked against the docs of that
  interface; say which versions you tested in the "Tested with" line.

## Writing pages (MyST Markdown cheat sheet)

Pages are Markdown with a few [MyST](https://mystmd.org/guide/syntax-overview) extensions:

````md
# Page title

Link to another page: {doc}`../background/what-is-imas`

Link into the docs of an IMAS component (checked at build time):
{external+imas-python:doc}`intro`, {external+imas-dd:doc}`coordinates`,
{external+imas-python:py:class}`imas.db_entry.DBEntry`

:::{note}
A highlighted note. Also: tip, warning, important.
:::

```{code-cell} python
# executed at build time; the output is shown on the page
import imas
print(imas.__version__)
```
````

A page containing `{code-cell}` blocks needs this header at the very top (see the template):

```yaml
---
file_format: mystnb
kernelspec:
  name: python3
  display_name: Python 3
---
```

Available intersphinx names: `imas-python`, `imas-core`, `imas-dd`, `imas-cpp`, `imas-fortran`,
`imas-matlab`, `imas-java`, `idstools`, `imas-validator`, `simdb`, `iwrap`, `imas-muscle3`,
`imas-paraview` (see `docs/conf.py`). To list the pages of one of them:
`python -m sphinx.ext.intersphinx https://imas-python.readthedocs.io/en/stable/objects.inv`.

## Previewing locally (optional)

The PR preview is enough for most changes. To build locally (Python 3.10+):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-docs.txt
scripts/fetch_tutorials.sh          # copies the IMAS-tutorial notebooks into docs/tutorials/
sphinx-autobuild docs _build/html   # live preview at http://127.0.0.1:8000
```

The first build runs all examples and notebooks, which takes a few minutes; later builds reuse
the results of unchanged pages. Use `-D nb_execution_mode=off` to skip execution entirely.
