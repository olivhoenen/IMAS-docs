---
file_format: mystnb
kernelspec:
  name: python3
  display_name: Python 3
---

# Adapting your code to IMAS

:::{admonition} Who is this for?
:class: note
**You** are new to IMAS but an expert in your own field. You have a working code (a
synthetic diagnostic, a physics model, an analysis tool...), perhaps with its own meshes and
file formats.

**You want** your code to read IMAS data (scenarios, experimental data, machine descriptions)
and to write results that any other IMAS-aware code or tool can use.

**This page** walks you from the concepts to a first program that reads and writes IMAS data,
then shows how to check, validate and extend it. Connecting codes into workflows is not
needed for this, and comes {ref}`at the end <next-workflows>`.
:::

## 1. Understand the concepts

Read {doc}`../background/what-is-imas` first (10 minutes). The essentials:

- data is described by the **Data Dictionary** as **IDSs** (e.g. `core_profiles`, `camera_ir`);
- IDSs are stored in **data entries**, identified by a **URI** such as `imas:hdf5?path=./run1`;
- your code uses the **Access Layer high-level interface** of its language to `get` IDSs from
  and `put` IDSs to data entries.

## 2. Map your data to IDSs

Before writing code, find where your inputs and outputs live in the Data Dictionary:

- Browse the {external+imas-dd:doc}`IDS reference <reference_ids>` for IDSs covering your
  system. Diagnostics usually have a dedicated IDS (for example `camera_ir`,
  `reflectometer_profile`, `reflectometer_fluctuation`, `interferometer`). Plasma inputs
  usually come from `equilibrium`, `core_profiles`, `edge_profiles` or `plasma_profiles`, and
  machine geometry from `wall`, `pf_active` and similar IDSs.
- For each quantity, check its **units**, its **coordinates** (which node gives its axis, see
  {external+imas-dd:doc}`coordinates`) and whether it is **time-dependent**.
- If your data lives on an unstructured or complex mesh, it goes into a **GGD** (generic grid
  description), see {doc}`../background/ggd`.
- If something you need is missing in the Data Dictionary, ask on the
  [Data Dictionary issue tracker](https://github.com/iterorganization/IMAS-Data-Dictionary/issues).

:::{tip}
You don't have to rewrite your code around IDSs. A common and safe approach is to keep your
internal data structures, and add a thin **IMAS input/output layer** at the boundary: read IDSs
and convert them to your structures at start-up, convert your results to IDSs at the end. Your
existing file format can keep working side by side while you migrate.
:::

## 3. Install

::::{tab-set}
:::{tab-item} Python
```bash
pip install "imas-python[netcdf]" imas-core
```
`imas-python` is the high-level interface. `imas-core` adds the HDF5 backend (the PyPI package
doesn't include MDSplus). See {external+imas-python:doc}`installing`.
:::
:::{tab-item} C++ / Fortran / MATLAB
These interfaces are built from source on top of IMAS-Core and the Data Dictionary. Follow the
build instructions of each one:
[C++](https://imas-cpp.readthedocs.io/en/stable/building_installing.html),
[Fortran](https://imas-fortran.readthedocs.io/en/latest/building_installing.html),
[MATLAB](https://imas-matlab.readthedocs.io/en/latest/building_installing.html), and
{external+imas-core:doc}`IMAS-Core <user_guide/installation>`.
Your institute may already provide them, e.g. as environment modules.
:::
::::

## 4. Your first code: read, modify, write

The task: open an existing data entry, read the electron temperature profile from
`core_profiles`, modify it (here we scale it by 10%, in your case your code computes
something), and write the result to a new data entry.

As input we use an open-access ITER scenario simulation published on
[Zenodo](https://zenodo.org/records/17062700) as a netCDF file.

```{code-cell} python
:tags: [remove-cell]
# keep IMAS-Python's informational log messages out of the rendered page
import os
os.environ["IMAS_LOGLEVEL"] = "WARNING"
```

```{code-cell} python
import urllib.request

url = "https://zenodo.org/records/17062700/files/iter_scenario_53298_seq1_DD4.nc"
path, _ = urllib.request.urlretrieve(url, "iter_scenario.nc")
```

Read the IDS from the input data entry:

```{code-cell} python
import imas

with imas.DBEntry("iter_scenario.nc", "r") as entry_in:
    cp = entry_in.get("core_profiles")

te = cp.profiles_1d[0].electrons.temperature
print("time slices:", cp.time.value)
print("Te units:", te.metadata.units, "| coordinate:", te.coordinates[0].metadata.name)
print("Te on axis:", te[0])
```

Modify it, check it against the Data Dictionary rules, and write it to a new data entry (here
using the HDF5 backend):

```{code-cell} python
cp.profiles_1d[0].electrons.temperature = 1.1 * te.value
cp.validate()  # raises an error if, e.g., coordinate sizes are inconsistent

with imas.DBEntry("imas:hdf5?path=./my_output", "w") as entry_out:
    entry_out.put(cp)
```

Read it back to check:

```{code-cell} python
with imas.DBEntry("imas:hdf5?path=./my_output", "r") as entry:
    te_new = entry.get("core_profiles").profiles_1d[0].electrons.temperature
print("Te on axis now:", te_new[0])
```

The same program in the other languages looks like this. Their tutorial samples use HDF5 or
MDSplus data entries: netCDF files are only supported by IMAS-Python, so first convert the
input with `imas convert iter_scenario.nc 4.1.1 "imas:hdf5?path=./scenario"`, then run the
program with `imas:hdf5?path=./scenario` as input URI.

::::{tab-set}
:::{tab-item} C++
```cpp
#include "ALClasses.h"
using namespace IdsNs;

int main(int argc, char* argv[])
{
    const char* uri_in  = argv[1];   // e.g. "imas:hdf5?path=./scenario"
    const char* uri_out = argv[2];   // e.g. "imas:hdf5?path=./my_output"

    IdsNs::IDS entry_in;
    entry_in.open(uri_in, OPEN_PULSE);
    entry_in._core_profiles.get();
    IdsNs::IDS::core_profiles cp = entry_in._core_profiles;

    // arrays are Blitz++ arrays; arrays of structures are indexed from 0
    cp.profiles_1d(0).electrons.temperature *= 1.1;

    IdsNs::IDS entry_out;
    entry_out.open(uri_out, FORCE_CREATE_PULSE);
    cp.setPulseCtx(entry_out.getPulseCtx());
    cp.put();

    entry_out.close();
    entry_in.close();
    return 0;
}
```
Docs: {external+imas-cpp:doc}`load_store_ids`, {external+imas-cpp:doc}`use_ids`,
{external+imas-cpp:doc}`examples <examples/examples_ToC>`.
:::
:::{tab-item} Fortran
```fortran
program first_imas_code
    use ids_routines
    implicit none

    type(ids_core_profiles) :: cp
    integer(ids_int)        :: entry_in, entry_out, status
    character(len=1024)     :: uri_in, uri_out

    call get_command_argument(1, uri_in)    ! e.g. imas:hdf5?path=./scenario
    call get_command_argument(2, uri_out)   ! e.g. imas:hdf5?path=./my_output

    call imas_open(trim(uri_in), OPEN_PULSE, entry_in, status)
    call ids_get(entry_in, 'core_profiles', cp)
    call imas_close(entry_in, status)

    ! arrays of structures are indexed from 1
    cp%profiles_1d(1)%electrons%temperature = 1.1_ids_real * cp%profiles_1d(1)%electrons%temperature

    call imas_open(trim(uri_out), FORCE_CREATE_PULSE, entry_out, status)
    call ids_put(entry_out, 'core_profiles', cp)
    call imas_close(entry_out, status)

    call ids_deallocate(cp)
end program first_imas_code
```
Docs: {external+imas-fortran:doc}`load_store_ids`, {external+imas-fortran:doc}`use_ids`,
{external+imas-fortran:doc}`error handling <error_handling>`,
{external+imas-fortran:doc}`examples <examples/examples_ToC>`.
:::
:::{tab-item} MATLAB
```matlab
function first_imas_code(uri_in, uri_out)
    % e.g. first_imas_code('imas:hdf5?path=./scenario', 'imas:hdf5?path=./my_output')
    OPEN_PULSE = 40;
    FORCE_CREATE_PULSE = 43;

    ctx = imas_open(uri_in, OPEN_PULSE);
    cp = ids_get(ctx, 'core_profiles');
    imas_close(ctx);

    % arrays of structures are cell arrays, indexed from 1
    cp.profiles_1d{1}.electrons.temperature = 1.1 * cp.profiles_1d{1}.electrons.temperature;

    ctx = imas_open(uri_out, FORCE_CREATE_PULSE);
    ids_put(ctx, 'core_profiles', cp);
    imas_close(ctx);
end
```
Docs: {external+imas-matlab:doc}`load_store_ids`, {external+imas-matlab:doc}`use_ids`,
{external+imas-matlab:doc}`examples <examples/examples_ToC>`.
:::
::::

:::{note}
Only the Python version is executed when this site is built. The C++, Fortran and MATLAB
versions follow the official tutorial samples of each interface. If you spot a problem,
please [report it](https://github.com/olivhoenen/IMAS-docs/issues/new?template=doc_page.yml).
:::

Going further with the language of your choice:
{external+imas-python:doc}`IMAS-Python training <courses/basic_user_training>` ·
[C++](https://imas-cpp.readthedocs.io/en/stable/) ·
[Fortran](https://imas-fortran.readthedocs.io/en/latest/) ·
[MATLAB](https://imas-matlab.readthedocs.io/en/latest/) ·
[Java](https://imas-java.readthedocs.io/en/latest/).

## 5. Check what you wrote

[IDStools](https://imas-idstools.readthedocs.io/en/latest/) (`pip install imas-idstools`) gives
you command-line tools that work on any data entry, whatever code wrote it:

```bash
idslist -u "imas:hdf5?path=./my_output"          # which IDSs and time slices are there
idsprint -u "imas:hdf5?path=./my_output#core_profiles/profiles_1d[0]/electrons/temperature"
plotkineticprofiles -u "imas:hdf5?path=./my_output"   # plot the kinetic profiles
```

See the {external+idstools:doc}`IDStools cheat sheet <cheatsheet>` for the many `print*` and
`plot*` tools, and the {doc}`IDStools tutorial notebook <../tutorials/index>`.

## 6. Validate your data

Data that other codes will use must follow the Data Dictionary rules. Two levels of checks:

- **Structure**: `validate()` in IMAS-Python (used above) checks, among other things, that
  coordinate sizes are consistent. See {external+imas-python:doc}`validation`.
- **Content**: [IMAS-Validator](https://imas-validator.readthedocs.io/en/stable/)
  (`pip install imas-validator`) runs rule sets on a data entry, for example to detect
  unphysical values, and you can write your own rules:

  ```bash
  imas_validator validate "imas:hdf5?path=./my_output"
  ```

  See {external+imas-validator:doc}`usage` and
  {external+imas-validator:doc}`defining your own rules <defining_rules>`.

## 7. Data on meshes: GGD

If your code works with meshes (camera pixels on a 3D wall, a 2D edge grid, a reflectometer
beam path...), the Data Dictionary describes them with the **generic grid description (GGD)**.
Continue with {doc}`../background/ggd`.

(next-workflows)=
## 8. Next step: workflows

Once your code reads and writes IDSs, it can be connected to other IMAS codes. To run it as an
**actor** exchanging IDSs in memory inside a workflow, see
[iWrap](https://iwrap.readthedocs.io/en/stable/) (start with
{external+iwrap:doc}`its introduction <documentation/iWrap_intro>`) and
[IMAS-MUSCLE3](https://imas-muscle3.readthedocs.io/en/latest/).

---

*Story contributed by Paulo Abreu. Tested with the latest PyPI releases of IMAS-Python and
IMAS-Core on every build.*
