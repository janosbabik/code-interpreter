# ScienceChat neutron-scattering Python environment

This fork provides a general-purpose, network-isolated Python environment for
custom analysis alongside ScienceChat. It is not an instrument reduction
service and does not claim official support for any ESS instrument data
pipeline.

The package selection follows the technique groups published at
<https://ess.eu/instruments>:

- **Diffraction and imaging:** BEER, DREAM, HEIMDAL, MAGIC, and ODIN.
- **Large-scale structures:** ESTIA and FREIA reflectometry, LOKI and SKADI
  SANS, and NMX macromolecular diffraction.
- **Spectroscopy:** BIFROST, CSPEC, MIRACLES, T-REX, and VESPA.

## Installed package groups

### Common neutron and NeXus data

- `scipp`, `scippnexus`, `scippneutron`
- `nexusformat`, `h5py`, `hdf5plugin`
- `periodictable`, `NCrystal`

### ESS instrument reduction packages

- `essreduce` common workflow infrastructure
- `esssans` for LOKI and SKADI
- `essdiffraction` for BEER and DREAM
- `essimaging` for ODIN and related imaging workflows
- `essnmx` for NMX
- `essreflectometry` for ESTIA and FREIA
- `essspectroscopy` for inelastic spectroscopy workflows
- `esspolarization`, required by the reflectometry stack

These distributions expose modules below the `ess` namespace, for example
`ess.sans`, `ess.diffraction`, and `ess.reflectometry`. Importability does not
make an instrument workflow self-contained: users must provide the relevant
raw NeXus, calibration, geometry, normalization, and metadata inputs. Examples
or reference files normally fetched from the network are unavailable unless
explicitly baked into the image or uploaded through LibreChat.

### SANS

- `sans-fitter`, `sasmodels`, `sasdata`, `bumps`
- built-in sasmodels CPU kernels precompiled in single and double precision

### Reflectometry

- `orsopy`
- `refnx`

`refl1d` is excluded because its current release requires BUMPS 1.0.4 while
the pinned SANS stack uses BUMPS 1.0.3.

### Diffraction, imaging, and crystallography

- `gemmi`
- `diffpy.structure`, `diffpy.srfit`
- `pyFAI`, `fabio`, `silx`
- `spglib`, `ase`, `biopython`

### Spectroscopy and lattice dynamics

- `euphonic`
- `phonopy`

`dynasor` is excluded from the default image because its MDAnalysis dependency
requires additional OpenMP runtime support. It can be evaluated in a separate
molecular-dynamics image.

### Units, uncertainty, optimization, and posterior analysis

- `pint`, `uncertainties`
- `lmfit`, `iminuit`
- `emcee`, `dynesty`, `arviz`, `corner`

### Larger and chunked datasets

- `xarray`, `dask[array]`
- `zarr`, `numcodecs`

## Deliberately separate applications

- **Mantid:** large application/runtime with its own release and environment
  requirements; deploy separately rather than embedding it in this sandbox.
- **McStas:** requires the simulation engine and data installation, not only a
  Python wrapper.
- **SasView GUI:** the sandbox already contains its non-GUI scientific
  dependencies.
- **GPU/OpenCL and MPI stacks:** require device, process, and networking access
  that is not enabled for the default sandbox.

## Scientific provenance

Code Interpreter results are generated custom code. They must be distinguished
from values produced by the `sans-pilot` MCP adapter. The presence of a package
does not validate a workflow, make it appropriate for a particular instrument,
or authorize scientific interpretation.

Packages are installed only at image build time. Runtime package installation
and general network access remain disabled.
