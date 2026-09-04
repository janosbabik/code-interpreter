"""Smoke test for the baked ScienceChat scientific Python package tree."""

from __future__ import annotations

from importlib.metadata import version
from pathlib import Path

import sasmodels
from sans_fitter import SANSFitter, examples

EXPECTED_VERSIONS = {
    "sans-fitter": "0.3.0",
    "bumps": "1.0.3",
    "sasmodels": "1.1.0",
    "sasdata": "0.12.2",
    "scipp": "26.8.0",
    "scippnexus": "26.1.1",
    "scippneutron": "26.9.0",
    "essreduce": "26.8.0",
    "esssans": "26.6.0",
    "essdiffraction": "26.8.1",
    "essimaging": "26.9.0",
    "essnmx": "26.6.0",
    "essreflectometry": "26.6.0",
    "essspectroscopy": "26.7.0",
    "esspolarization": "25.10.0",
    "nexusformat": "2.0.3",
    "h5py": "3.16.0",
    "hdf5plugin": "7.1.0",
    "periodictable": "2.1.0",
    "NCrystal": "4.4.6",
    "pint": "0.25.3",
    "uncertainties": "3.2.3",
    "lmfit": "1.3.4",
    "emcee": "3.1.6",
    "arviz": "1.3.0",
    "corner": "2.3.0",
    "iminuit": "2.32.0",
    "dynesty": "3.1.0",
    "xarray": "2026.7.0",
    "dask": "2026.8.0",
    "zarr": "3.3.0",
    "numcodecs": "0.16.5",
    "orsopy": "1.2.3",
    "refnx": "0.1.67",
    "gemmi": "0.7.5",
    "diffpy.structure": "3.5.0",
    "diffpy.srfit": "3.3.1",
    "pyFAI": "2026.5.0",
    "fabio": "2026.6.0",
    "silx": "3.1.2",
    "spglib": "2.6.0",
    "ase": "3.29.0",
    "biopython": "1.88",
    "euphonic": "2.1.0",
    "phonopy": "4.4.0",
}

IMPORTS = [
    "scipp",
    "scippnexus",
    "scippneutron",
    "ess.reduce",
    "ess.sans",
    "ess.diffraction",
    "ess.imaging",
    "ess.nmx",
    "ess.reflectometry",
    "ess.spectroscopy",
    "ess.polarization",
    "nexusformat",
    "hdf5plugin",
    "periodictable",
    "NCrystal",
    "pint",
    "uncertainties",
    "lmfit",
    "emcee",
    "arviz",
    "corner",
    "iminuit",
    "dynesty",
    "xarray",
    "dask",
    "zarr",
    "numcodecs",
    "orsopy",
    "refnx",
    "gemmi",
    "diffpy.structure",
    "diffpy.srfit",
    "pyFAI",
    "fabio",
    "silx",
    "spglib",
    "ase",
    "Bio",
    "euphonic",
    "phonopy",
]


def main() -> None:
    import importlib

    actual = {name: version(name) for name in EXPECTED_VERSIONS}
    if actual != EXPECTED_VERSIONS:
        raise RuntimeError(f"Unexpected scientific package versions: {actual}")
    for module in IMPORTS:
        importlib.import_module(module)

    import NCrystal
    import gemmi
    import periodictable
    import scipp as sc

    variable = sc.array(
        dims=["q"],
        values=[1.0, 2.0],
        variances=[0.1, 0.2],
        unit="1/angstrom",
    )
    if variable.sizes["q"] != 2:
        raise RuntimeError("Scipp labeled-array smoke test failed")
    if NCrystal.createInfo("Al_sg225.ncmat").getStructureInfo()["spacegroup"] != 225:
        raise RuntimeError("NCrystal material smoke test failed")
    if periodictable.H.neutron.b_c is None:
        raise RuntimeError("periodictable neutron data smoke test failed")
    if round(gemmi.UnitCell(5, 5, 5, 90, 90, 90).volume, 1) != 125.0:
        raise RuntimeError("Gemmi crystallography smoke test failed")

    compiled = Path(sasmodels.__file__).resolve().parent.parent / "compiled_models"
    single = list(compiled.glob("sas32_*.so"))
    double = list(compiled.glob("sas64_*.so"))
    if not single or len(single) != len(double):
        raise RuntimeError(
            f"Incomplete sasmodels precompile: single={len(single)}, double={len(double)}"
        )

    data = examples.simulate(
        "sphere",
        radius=50.0,
        noise=0.02,
        seed=3,
        npoints=30,
        sld=4.0,
        sld_solvent=1.0,
        scale=1.0,
        background=0.001,
    )
    fitter = SANSFitter()
    fitter.set_data(data)
    fitter.set_model("sphere")
    for name, value in {
        "sld": 4.0,
        "sld_solvent": 1.0,
        "scale": 1.0,
        "background": 0.001,
    }.items():
        fitter.set_param(name, value=value, vary=False)
    fitter.set_param("radius", value=30.0, min=3.0, max=300.0, vary=True)
    result = fitter.fit(engine="bumps", method="amoeba")
    fitted_radius = float(result["parameters"]["radius"]["value"])
    if not 45.0 < fitted_radius < 55.0:
        raise RuntimeError(f"Unexpected fitted radius: {fitted_radius}")

    print(
        "ScienceChat scientific runtime smoke test passed: "
        f"radius={fitted_radius:.3f}, kernels={len(single) + len(double)}"
    )


if __name__ == "__main__":
    main()
