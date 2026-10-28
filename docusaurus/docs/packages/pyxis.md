# Pyxis Package

This package provides [Pyxis](https://github.com/NVIDIA/pyxis), NVIDIA's SPANK plugin for running containerized tasks in Slurm.

## Overview

Pyxis lets unprivileged cluster users run containerized tasks through `srun`. It is designed to work with [Enroot](https://github.com/NVIDIA/enroot) as the container runtime, so containers become part of an ordinary Slurm job submission.

## Why a Custom Package?

The custom Pyxis package in this repository:

- Builds against this repository's Slurm (`slurm_factory.slurm`), so `spank.h` matches the Slurm it is loaded into
- Installs the plugin as `lib/slurm/spank_pyxis.so` in its prefix, next to Slurm's own plugins in a view or tarball
- Adds `$ORIGIN/..` to the plugin's RPATH after install, so it finds Slurm's libraries in a relocated tree

:::note
The RPATH fixup uses whatever `patchelf` is on `PATH` during the build; the package does not declare it as a dependency. Without one, the fixup is skipped silently.
:::

## Available Versions

| Version | Status |
|---------|--------|
| `0.24.0` | Only version; used by Slurm Factory |

The package has no variants.

## Installation

```bash
spack install slurm_factory.pyxis@0.24.0
```

To build it against a specific Slurm:

```bash
spack install slurm_factory.pyxis@0.24.0 ^slurm_factory.slurm@26-05-5-1
```

## Usage with Slurm

Enable the plugin in Slurm's `plugstack.conf`, in the `sysconfdir` Slurm was built with:

```text
required /path/to/pyxis/lib/slurm/spank_pyxis.so
```

`spack location -i pyxis` gives the prefix. Enroot itself is not packaged here and must be installed on the compute nodes.

## Dependencies

- **Slurm** (`slurm_factory.slurm`, build and link): Slurm headers and libraries

## Package Source

- **Homepage**: [https://github.com/NVIDIA/pyxis](https://github.com/NVIDIA/pyxis)
- **Package Definition**: [`packages/pyxis/package.py`](https://github.com/vantagecompute/slurm-factory-spack-repo/blob/main/spack_repo/slurm_factory/packages/pyxis/package.py)

## License

Pyxis is licensed under the Apache License 2.0.

## See Also

- [Slurm Package](./slurm.md): Main Slurm package documentation
- [Getting Started](../getting-started.md): Installation guide
