# AGENTS.md

Guidance for AI coding assistants working in this repository.

## What this repo is

Source of the open-access IMAS documentation hub, published to GitHub Pages
(`https://olivhoenen.github.io/IMAS-docs/`). It is a Sphinx site written in MyST Markdown
(`docs/`), organised around user stories. It links to the documentation of each IMAS component
rather than duplicating it. The hands-on notebooks are **not** stored here: `scripts/fetch_tutorials.sh`
copies them from the `IMAS-tutorial` repo into `docs/tutorials/notebooks/` (git-ignored) at build time.

## Build

```bash
pip install -r requirements-docs.txt
scripts/fetch_tutorials.sh
sphinx-build -W --keep-going -b html docs _build/html          # same as CI: warnings are errors
sphinx-build -b html -D nb_execution_mode=off docs _build/html  # fast, skips code execution
sphinx-build -b linkcheck -D nb_execution_mode=off docs _build/linkcheck
```

- `{code-cell}` blocks in `.md` pages with the `file_format: mystnb` header, and the tutorial
  notebooks, are executed by myst-nb (`nb_execution_mode = "cache"`, cache in
  `_build/.jupyter_cache`, run in a temporary directory). `05_SimDB` is excluded (needs ITER auth).
- CI (`.github/workflows/docs.yml`) builds on every PR (preview under `pr-preview/` on gh-pages)
  and deploys `main` to the `gh-pages` branch. It also runs weekly and on `repository_dispatch`
  from IMAS-tutorial.

## Conventions

- Content rules (see CONTRIBUTING.md): only PyPI packages and open data; no site-specific setup
  (no cluster paths, modules or internal servers); link out to component docs instead of copying.
- Links to other IMAS docs use intersphinx with explicit roles, e.g.
  `{external+imas-python:doc}` or `{external+imas-dd:doc}`. Plain `{py:class}` roles do not
  resolve externally (`intersphinx_disabled_reftypes = ["*"]`). Inventory names are in
  `docs/conf.py`.
- User-story pages copy `docs/_templates/user-story.md` and are listed in `docs/user-stories/index.md`.
- Python examples must be executable `{code-cell}`s. C++, Fortran and MATLAB examples are static and
  must follow the official samples in the IMAS-Cpp, IMAS-Fortran and IMAS-MATLAB repos
  (`doc/code_samples/tutorial/`).
- `sphinx_immaterial` must stay in `extensions` as well as `html_theme`: it merges its default
  theme options at `config-inited`, and without it the build crashes (`KeyError: 'font'`).
- IMAS-Python logs INFO messages at import; pages hide them with a `remove-cell` that sets
  `os.environ["IMAS_LOGLEVEL"] = "WARNING"` before `import imas`.
- IMAS-Python 2.3: use `imas.identifiers.<name>` (attribute access); `from imas.identifiers import ...`
  fails. netCDF data entries do not support `get_slice`.
