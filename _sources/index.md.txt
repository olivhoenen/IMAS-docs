# IMAS documentation hub

**IMAS**, the Integrated Modelling & Analysis Suite, is the set of standards and open-source
software used by ITER and the fusion community to describe, store and exchange experimental and
simulation data in a common, machine-independent way.

This site is the entry point: it explains the main ideas, shows short working examples, and
points you to the full documentation of each IMAS component. Pick the path that matches what you
want to do.

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} New to IMAS?
:link: background/what-is-imas
:link-type: doc

Learn what IMAS, IDSs, the Data Dictionary and the Access Layer are, and how they fit together.
:::

:::{grid-item-card} Adapt your code to IMAS
:link: user-stories/adapting-a-code
:link-type: doc

You have a working code and want it to read and write IMAS data. Start here.
:::

:::{grid-item-card} Hands-on tutorials
:link: tutorials/index
:link-type: doc

Jupyter notebooks you can run in your browser on Google Colab.
:::

:::{grid-item-card} IMAS software
:link: software/index
:link-type: doc

Catalogue of IMAS components, with links to their documentation and repositories.
:::
::::

Everything here uses public packages from PyPI and open data, so you can follow along from
your own laptop.

```{admonition} Missing your use case?
:class: tip
This hub is built around **user stories**. Tell us what you are trying to do by
[opening a user story](https://github.com/olivhoenen/IMAS-docs/issues/new?template=user_story.yml),
or [contribute a page](contributing.md).
```

```{toctree}
:hidden:
:maxdepth: 2

background/index
user-stories/index
tutorials/index
software/index
contributing
```
