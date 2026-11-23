---
file_format: mystnb
kernelspec:
  name: python3
  display_name: Python 3
---

# Data on grids: the GGD

Many codes don't work on simple 1D profiles but on **meshes**: 2D edge grids, 3D wall
surfaces, camera pixels, finite-element meshes... The Data Dictionary describes all of them
with one structure, the **Generalized Grid Description (GGD)**. It is used, for example, in
`edge_profiles`, `edge_sources`, `wall`, `equilibrium` and `plasma_profiles`.

## The idea in three parts

A GGD has two halves, stored side by side in an IDS:

1. **The grid** (`grid_ggd`) describes the mesh. Inside one or more **spaces**, it lists the
   grid **objects** per dimension: nodes (0D) with their coordinates, then edges (1D), 2D cells,
   3D cells, each defined by the objects of lower dimension that bound them (or directly by
   their nodes).
2. **Grid subsets** (`grid_subset`) name groups of objects: "all nodes", "all cells", "the
   separatrix", "the inner target"... Standard subsets have an identifier from the Data
   Dictionary, so tools can recognise them.
3. **Quantities on the grid** (`ggd`) store values, e.g. `ggd[t].electrons.temperature[i]`,
   each pointing to a grid (`grid_index`) and a grid subset (`grid_subset_index`). The
   `values` array has one value per object of that subset.

Because grids and values are separate, a grid can be written once and shared by many
quantities and time slices.

## A first GGD, written and read back

The smallest useful example: two quadrilateral cells in the poloidal (R, Z) plane, and an
electron temperature value on each cell, stored in `edge_profiles`.

```{code-cell} python
:tags: [remove-cell]
# keep IMAS-Python's informational log messages out of the rendered page
import os
os.environ["IMAS_LOGLEVEL"] = "WARNING"
```

```{code-cell} python
import numpy as np
import imas

identifiers = imas.identifiers  # standard identifier lists from the Data Dictionary

ep = imas.IDSFactory().edge_profiles()
ep.ids_properties.homogeneous_time = imas.ids_defs.IDS_TIME_MODE_HOMOGENEOUS
ep.ids_properties.comment = "My first GGD: two quadrilateral cells"
ep.time = [0.0]

# --- 1. the grid: one space with nodes (dimension 1) and 2D cells (dimension 3)
ep.grid_ggd.resize(1)
grid = ep.grid_ggd[0]
grid.time = 0.0
grid.identifier = identifiers.ggd_identifier.linear
grid.space.resize(1)
space = grid.space[0]
space.identifier = identifiers.ggd_space_identifier.primary_standard
space.coordinates_type.resize(2)
space.coordinates_type[0] = identifiers.coordinate_identifier.r
space.coordinates_type[1] = identifiers.coordinate_identifier.z
space.objects_per_dimension.resize(3)  # nodes, edges, 2D cells

# 6 nodes on a 3 x 2 lattice, coordinates (R, Z) in metres
r, z = np.meshgrid([6.0, 6.1, 6.2], [0.0, 0.1])
nodes = space.objects_per_dimension[0].object
nodes.resize(r.size)
for i, (ri, zi) in enumerate(zip(r.ravel(), z.ravel())):
    nodes[i].geometry = [ri, zi]

# 2 cells, each defined by its 4 nodes, anti-clockwise (indices start at 1)
cells = space.objects_per_dimension[2].object
cells.resize(2)
cells[0].nodes = [1, 2, 5, 4]
cells[1].nodes = [2, 3, 6, 5]

# --- 2. a grid subset grouping all the cells
grid.grid_subset.resize(1)
subset = grid.grid_subset[0]
subset.identifier = identifiers.ggd_subset_identifier.cells
subset.dimension = 3
subset.element.resize(len(cells))
for i, element in enumerate(subset.element):
    element.object.resize(1)
    element.object[0].space = 1
    element.object[0].dimension = 3
    element.object[0].index = i + 1

# --- 3. a quantity on that subset: one temperature value per cell
ep.ggd.resize(1)
ep.ggd[0].time = 0.0
ep.ggd[0].electrons.temperature.resize(1)
te = ep.ggd[0].electrons.temperature[0]
te.grid_index = 1
te.grid_subset_index = subset.identifier.index
te.values = [120.0, 95.0]  # eV

ep.validate()
with imas.DBEntry("imas:hdf5?path=./my_first_ggd", "w") as entry:
    entry.put(ep)
```

Reading it back, any code can rebuild the mesh and the values:

```{code-cell} python
with imas.DBEntry("imas:hdf5?path=./my_first_ggd", "r") as entry:
    ep_in = entry.get("edge_profiles")

space_in = ep_in.grid_ggd[0].space[0]
for i, cell in enumerate(space_in.objects_per_dimension[2].object):
    corners = [space_in.objects_per_dimension[0].object[n - 1].geometry.value for n in cell.nodes]
    print(f"cell {i + 1}: corners (R, Z) = {np.round(corners, 2).tolist()}")
print("Te per cell:", ep_in.ggd[0].electrons.temperature[0].values.value, "eV")
```

A complete grid usually also lists the edges and their boundaries, which lets tools find
neighbouring cells. The guides below explain how.

## Learn more

- {external+imas-dd:doc}`GGD guide <ggd_guide/doc>` and
  {external+imas-dd:doc}`GGD examples <ggd_guide/examples>` in the Data Dictionary docs;
- the [GGD library](https://github.com/iterorganization/GGD), helpers to build and use GGD
  grids;
- [IMAS-ParaView](https://imas-paraview.readthedocs.io/en/stable/) to visualise GGD data in
  2D and 3D.
