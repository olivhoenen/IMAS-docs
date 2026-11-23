---
file_format: mystnb   # keep: lets the {code-cell} blocks below run at build time
kernelspec:
  name: python3
  display_name: Python 3
---

# <Title: what the user achieves, e.g. "Adapting your code to IMAS">

:::{admonition} Who is this for?
:class: note
**You** are <who: experience with IMAS, field of expertise>.

**You want** <goal>, **so that** <benefit>.

**This page** <what the reader will have at the end>.
:::

## Background

<Concepts the reader needs. Keep it short and link to the background pages,
e.g. {doc}`../background/what-is-imas`, or to the docs of the relevant software.>

## How IMAS addresses it

<Which IMAS components solve the problem and how, in a few paragraphs.>

## Quick example

<A short, complete example. Python code-cells are executed when the site is built;
use open data (e.g. from https://zenodo.org/communities/open-imas/), never site-specific paths.>

```{code-cell} python
import imas
```

## Going further

- <Links into the docs of the relevant software, preferably with intersphinx roles, e.g.
  {external+imas-python:doc}`intro`>
- <Related tutorial notebook in {doc}`../tutorials/index`>

---

*Story from <issue link>. Tested with <package versions, or "the latest PyPI releases on every build">.*
