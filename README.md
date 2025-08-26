# Slurm Factory Spack Repository

A custom Spack repository containing enhanced Slurm packages for cluster management and job scheduling.

## Overview

This repository provides a custom Slurm package for Spack with additional features and patches optimized for production environments.

## Installation

To use this repository with Spack, add it to `spack.yaml`.
```yaml
spack:
  repos:
    slurm_factory:
      git: https://github.com/vantagecompute/slurm-factory-spack-repo.git
  specs:
  - slurm@23-11-11-1 +influxdb +readline +hwloc +pmix +restd ~nvml ~rsmi +cgroup +pam sysconfdir=/etc/slurm %gcc@13.3.0
```

Or clone and add in one step:

```bash
git clone https://github.com/vantagecompute/slurm-factory-spack-repo.git
spack repo add slurm-factory-spack-repo
```

## Usage

Once added, you can install the custom Slurm package:

```bash
spack install slurm_factory::slurm
```

## Repository Structure

```
├── README.md
├── extras
│   └── package.py
├── spack-repo-index.yaml
└── spack_repo
    └── slurm_factory
        ├── packages
        │   └── slurm
        │       ├── package.py
        │       └── slurm_prefix.patch
        └── repo.yaml
```

## Available Packages

- **slurm**: Enhanced Slurm workload manager with custom patches and optimizations

## Contributing

Please follow Spack's package development guidelines when contributing to this repository.
