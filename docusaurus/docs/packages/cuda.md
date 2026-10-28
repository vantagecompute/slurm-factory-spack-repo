# cuda Package

The `slurm_factory.cuda` package is the builtin Spack `cuda` recipe with NVIDIA releases added that the builtin recipe does not list yet. It subclasses the builtin package, so every variant, build step and older version is the builtin one.

Slurm links CUDA for NVML GPU autodetection (`+nvml`). Slurm Factory's GPU builds use the latest release.

## Available Versions

| Version | Status |
|---------|--------|
| `13.4.3` | Latest; added here, used by Slurm Factory |
| `13.4.2` and older | From the builtin Spack recipe |

Each version is NVIDIA's local runfile installer for `x86_64` (`cuda_<version>_linux.run`) and `aarch64` (`cuda_<version>_linux_sbsa.run`), checked by sha256.

:::note
An entry is dropped from this package once the builtin Spack recipe carries that release.
:::

## Installation

```bash
spack install slurm_factory.cuda@13.4.3
```

## Related Documentation

- [Slurm Package](./slurm.md): Uses CUDA when built with `+nvml`
