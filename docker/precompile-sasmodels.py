"""Precompile built-in sasmodels CPU kernels for the no-exec sandbox."""

from __future__ import annotations

from pathlib import Path

import sasmodels
from sasmodels.core import precompile_dlls


def main() -> None:
    # kerneldll checks the site-packages-level compiled_models directory before
    # its writable user cache. The latter lives under /mnt/data in the sandbox,
    # which is intentionally mounted no-exec.
    output_dir = Path(sasmodels.__file__).resolve().parent.parent / "compiled_models"
    single = precompile_dlls(str(output_dir), dtype="single")
    double = precompile_dlls(str(output_dir), dtype="double")
    if not single or not double:
        raise RuntimeError("sasmodels did not produce both kernel sets")
    print(
        f"Precompiled {len(single)} single-precision and "
        f"{len(double)} double-precision sasmodels kernels in {output_dir}"
    )


if __name__ == "__main__":
    main()
