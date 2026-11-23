# IMAS software

The main open-source IMAS components. Each card links to the full documentation; the source
code is on [GitHub](https://github.com/iterorganization).

## Data model

::::{grid} 1 2 2 2
:gutter: 2

:::{grid-item-card} Data Dictionary
:link: https://imas-data-dictionary.readthedocs.io/en/latest/

Definition of all IDSs, with units, coordinates and identifiers.
`pip install imas-data-dictionary`
:::
:::{grid-item-card} GGD
:link: https://github.com/iterorganization/GGD

Library to build and use generalized grid descriptions. See {doc}`../background/ggd`.
:::
::::

## Reading and writing IMAS data (Access Layer)

::::{grid} 1 2 3 3
:gutter: 2

:::{grid-item-card} IMAS-Python
:link: https://imas-python.readthedocs.io/en/stable/

Python interface, also handles netCDF files and DD version conversion.
`pip install imas-python`
:::
:::{grid-item-card} IMAS-Core
:link: https://imas-core.readthedocs.io/en/latest/

Low-level library and storage backends (HDF5, MDSplus, UDA, ...) used by all interfaces.
`pip install imas-core`
:::
:::{grid-item-card} C++
:link: https://imas-cpp.readthedocs.io/en/stable/

C++ interface (IMAS-Cpp).
:::
:::{grid-item-card} Fortran
:link: https://imas-fortran.readthedocs.io/en/latest/

Fortran interface (IMAS-Fortran).
:::
:::{grid-item-card} MATLAB
:link: https://imas-matlab.readthedocs.io/en/latest/

MATLAB interface (IMAS-MATLAB).
:::
:::{grid-item-card} Java
:link: https://imas-java.readthedocs.io/en/latest/

Java interface (IMAS-Java).
:::
::::

## Exploring, checking and visualising data

::::{grid} 1 2 3 3
:gutter: 2

:::{grid-item-card} IDStools
:link: https://imas-idstools.readthedocs.io/en/latest/

Command-line tools to list, print, plot, compare and manipulate IDS data.
`pip install imas-idstools`
:::
:::{grid-item-card} IMAS-Validator
:link: https://imas-validator.readthedocs.io/en/stable/

Rule-based validation of IDS data.
`pip install imas-validator`
:::
:::{grid-item-card} IMAS-ParaView
:link: https://imas-paraview.readthedocs.io/en/stable/

ParaView plugins to visualise IDS data, including GGD grids.
:::
::::

## Managing simulations

::::{grid} 1 2 2 2
:gutter: 2

:::{grid-item-card} SimDB
:link: https://simdb.readthedocs.io/en/latest/

Catalogue to publish, search and retrieve simulations.
`pip install imas-simdb`
:::
::::

## Building workflows

::::{grid} 1 2 2 2
:gutter: 2

:::{grid-item-card} iWrap
:link: https://iwrap.readthedocs.io/en/stable/

Wraps Fortran, C++ and Python codes into actors for IMAS workflows.
:::
:::{grid-item-card} IMAS-MUSCLE3
:link: https://imas-muscle3.readthedocs.io/en/latest/

Generic actors and helpers to couple IMAS codes with MUSCLE3.
:::
::::

```{admonition} Something missing?
:class: tip
Software listed here is open source and installable without access to a specific site.
To propose another component, [open an issue](https://github.com/olivhoenen/IMAS-docs/issues/new?template=doc_page.yml).
```
