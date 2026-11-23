# What is IMAS?

The **Integrated Modelling & Analysis Suite (IMAS)** is ITER's framework for describing and
exchanging fusion data. Its central idea is simple: if every code and every diagnostic describes
its data in **the same, machine-independent structure**, codes can be chained, compared and
reused across devices without writing a converter for each pair of them.

IMAS has three layers: a **data model** (the Data Dictionary), a **data access library** (the
Access Layer) with interfaces for several languages, and **tools** built on top of them.

## The Data Dictionary and IDSs

The **Data Dictionary (DD)** is the data model. It defines a set of **Interface Data Structures
(IDSs)**, each describing one physical system or one kind of result. The current version
defines more than 80 IDSs, for example:

- plasma state: `equilibrium`, `core_profiles`, `edge_profiles`, `plasma_profiles`;
- machine description: `wall`, `pf_active`, `magnetics`, `tf`;
- diagnostics: `camera_ir`, `reflectometer_profile`, `thomson_scattering`, `bolometer`, ...;
- heating and current drive: `nbi`, `ec_launchers`, `waves`, `distributions`;
- overview: `summary`.

Inside an IDS, data is organised as a tree of structures, arrays of structures and leaves
(numbers, arrays, strings). Each leaf has documented **units** (SI, temperatures in eV),
**coordinates** (which other node gives its axis), and sometimes **identifiers**: standard lists
of allowed values with an index, a name and a description. Every IDS also has an
`ids_properties` structure (provenance, how time is stored) and a `time` vector.

The DD is versioned. Data always records which DD version it was written with, and IMAS-Python
can convert data between versions. Conventions such as COCOS (the sign and normalisation of
magnetic quantities) are fixed by the DD, so codes don't need to guess them.

Learn more:
- {external+imas-dd:doc}`Data Dictionary user guide <intro>`, with the browsable
  {external+imas-dd:doc}`IDS reference <reference_ids>`
- {external+imas-dd:doc}`Coordinates <coordinates>`, {external+imas-dd:doc}`units <units>`,
  {external+imas-dd:doc}`identifiers <identifiers>` and {external+imas-dd:doc}`COCOS <cocos>`
- {external+imas-dd:doc}`Glossary <data_dictionary_glossary>`

## The Access Layer: data entries, URIs and backends

IDSs are stored in **data entries**. A data entry holds any number of IDSs, and several
**occurrences** of the same IDS if needed (for instance two equilibrium reconstructions). A data
entry is identified by a **URI** that names the storage format, or **backend**, and its location:

```text
imas:hdf5?path=./my_run                  HDF5 files in the ./my_run folder
imas:mdsplus?path=/data/my_run           MDSplus files in the /data/my_run folder
imas:memory?path=scratch                 in memory only, lost when the entry is closed
imas://uda.example.org/uda?path=...      remote data, accessed through a UDA server
imas:hdf5?path=./my_run#equilibrium      a fragment can point at one IDS (or part of it)
```

The **Access Layer** reads and writes IDSs from and to data entries. It consists of:

- **IMAS-Core**, the low-level library implementing the backends and the URI scheme;
- a **high-level interface (HLI)** per language, which gives you IDSs as native objects:
  [IMAS-Python](https://imas-python.readthedocs.io/en/stable/),
  [C++](https://imas-cpp.readthedocs.io/en/stable/),
  [Fortran](https://imas-fortran.readthedocs.io/en/latest/),
  [MATLAB](https://imas-matlab.readthedocs.io/en/latest/) and
  [Java](https://imas-java.readthedocs.io/en/latest/).

In every language the pattern is the same: **open** a data entry from its URI, **get** an IDS,
work with it, **put** an IDS, **close** the entry. Time-dependent data can also be read or
written one time slice at a time (`get_slice` / `put_slice`).

IMAS-Python can additionally store IDSs in standalone **netCDF** files (`.nc`), handy for
sharing small datasets. Open-access IMAS data is published this way in the
[open-imas community on Zenodo](https://zenodo.org/communities/open-imas/).

Learn more:
- {external+imas-dd:doc}`IMAS URI scheme <IMAS-URI-scheme>` and
  {external+imas-dd:doc}`data entries and occurrences <dataentry_and_occurrence>`
- {external+imas-core:doc}`IMAS-Core backends <user_guide/backends_guide>`
- {external+imas-python:doc}`IMAS-Python introduction <intro>` and its
  {external+imas-python:doc}`netCDF support <netcdf>`

## Tools built on IMAS

Because all IMAS data share one structure, generic tools work on any of it:

- [IDStools](https://imas-idstools.readthedocs.io/en/latest/): command-line tools to list,
  print, plot, compare and manipulate IDS data;
- [IMAS-Validator](https://imas-validator.readthedocs.io/en/stable/): checks that IDS data
  follows the DD rules and physics consistency rules;
- [IMAS-ParaView](https://imas-paraview.readthedocs.io/en/stable/): 2D/3D visualisation of IDS
  data, including data on complex grids;
- [SimDB](https://simdb.readthedocs.io/en/latest/): catalogue to publish, search and retrieve
  simulations.

## Codes and workflows

A code that reads its inputs from IDSs and writes its outputs to IDSs can be connected to any
other such code. IMAS provides tools to go one step further and wrap codes as **actors** that
exchange IDSs in memory inside a **workflow**: [iWrap](https://iwrap.readthedocs.io/en/stable/)
generates actors from Fortran, C++ or Python codes, and
[IMAS-MUSCLE3](https://imas-muscle3.readthedocs.io/en/latest/) couples them with the MUSCLE3
coupling library. You don't need any of this to read and write IMAS data; it comes later.

## Where to go next

- You have a code and want it to speak IMAS: {doc}`../user-stories/adapting-a-code`.
- You want to try things in your browser: {doc}`../tutorials/index`.
- Your data lives on a mesh: {doc}`ggd`.
