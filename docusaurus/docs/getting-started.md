# Getting Started

This guide will help you get started with installing Slurm from the Slurm Factory Spack buildcache.

## Prerequisites

You need:

- A Linux system on `x86_64` or `aarch64` that matches one of the [buildcache toolchains](./index.md#supported-toolchains) (Ubuntu 22.04, 24.04 or 26.04, or Rocky Linux 8, 9 or 10)
- [Spack](https://spack.io) installed (v1.0.0 or later)
- Basic familiarity with Spack package management

### Install Spack

If you don't have Spack installed:

```bash
git clone --depth 1 --branch v1.0.0 https://github.com/spack/spack.git ~/spack
source ~/spack/share/spack/setup-env.sh
```

Add Spack to your shell startup:

```bash
echo 'source ~/spack/share/spack/setup-env.sh' >> ~/.bashrc
```

## Installing Slurm from Buildcache

The fastest way to get Slurm is to install it from our public buildcache. This eliminates the need to compile from source.

### Step 1: Add the Spack Repository

First, clone and add this custom Spack repository:

```bash
git clone https://github.com/vantagecompute/slurm-factory-spack-repo.git
spack repo add slurm-factory-spack-repo/spack_repo/slurm_factory
```

Verify the repository was added:

```bash
spack repo list
```

You should see `slurm_factory` in the list.

### Step 2: Configure the Buildcache

The buildcache has one mirror per OS toolchain, at `<toolchain>/spack`. Add the one matching your host; this example uses Ubuntu 24.04 (`noble`):

```bash
spack mirror add slurm-factory \
  https://slurm-factory-spack-binary-cache.vantagecompute.ai/noble/spack
```

The other toolchains are `resolute` (Ubuntu 26.04), `jammy` (Ubuntu 22.04), `rockylinux10`, `rockylinux9` and `rockylinux8`. Each mirror holds every supported Slurm series for both `x86_64` and `aarch64`.

Trust the buildcache GPG key:

```bash
spack buildcache keys --install --trust
```

### Step 3: Install GCC Compiler (Optional)

Each toolchain's packages are built with that OS's GCC (13.3.0 on `noble`), and the mirror carries that GCC too. If you want to build further packages with the same compiler:

```bash
# Install GCC 13.3.0 from buildcache
spack install --cache-only gcc@13.3.0

# Register it as a compiler
spack compiler find $(spack location -i gcc@13.3.0)

# Verify
spack compiler list
```

### Step 4: Install Slurm

List the Slurm builds in the mirror:

```bash
spack buildcache list --long --variants slurm
```

Install one by its hash, so you get exactly the spec from the buildcache:

```bash
spack install --cache-only /<hash>
```

You can also install by spec. The published builds are `+nvml +rsmi sysconfdir=/etc/slurm` built with the toolchain's GCC, so the spec has to match for Spack to reuse them:

```bash
spack install --cache-only \
  slurm_factory.slurm@26-05-5-1 +nvml +rsmi sysconfdir=/etc/slurm %gcc@13.3.0
```

### Step 5: Verify Installation

Check that Slurm was installed:

```bash
spack find slurm
spack location -i slurm
```

Test the binaries:

```bash
$(spack location -i slurm)/bin/srun --version
```

## Docker Example

Here's a complete Dockerfile that installs Slurm from the `noble` buildcache:

```dockerfile
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential ca-certificates curl git \
    gcc g++ gfortran python3 unzip

# Install Spack
RUN git clone --depth 1 --branch v1.0.0 \
    https://github.com/spack/spack.git /opt/spack

ENV SPACK_ROOT=/opt/spack
ENV PATH=$SPACK_ROOT/bin:$PATH

SHELL ["/bin/bash", "-l", "-c"]

# Add custom repository
RUN git clone --depth 1 \
    https://github.com/vantagecompute/slurm-factory-spack-repo.git \
    /opt/slurm-factory-spack-repo && \
    spack repo add /opt/slurm-factory-spack-repo/spack_repo/slurm_factory

# Configure the buildcache mirror for this toolchain
RUN spack mirror add slurm-factory \
    https://slurm-factory-spack-binary-cache.vantagecompute.ai/noble/spack

# Trust buildcache keys
RUN spack buildcache keys --install --trust

# Install Slurm
RUN spack install --cache-only \
    slurm_factory.slurm@26-05-5-1 +nvml +rsmi sysconfdir=/etc/slurm %gcc@13.3.0

# Verify installation
RUN spack find slurm && \
    $(spack location -i slurm)/bin/srun --version

CMD ["/bin/bash"]
```

## Building from Source

If you prefer to build from source or need a custom configuration:

```bash
# Install with specific variants
spack install slurm_factory.slurm@26-05-5-1 +nvml sysconfdir=/etc/slurm
```

PMIx, hwloc, slurmrestd, FreeIPMI and the other integrations are always built in; only `sysconfdir`, `gtk`, `nvml` and `rsmi` are variants. They are documented in the [Slurm package documentation](./packages/slurm.md).

## Using in spack.yaml

For environment-based workflows, add to your `spack.yaml`. This is the same repository configuration Slurm Factory uses:

```yaml
spack:
  repos:
    slurm_factory:
      git: https://github.com/vantagecompute/slurm-factory-spack-repo.git
      branch: main

  mirrors:
    slurm-factory:
      url: https://slurm-factory-spack-binary-cache.vantagecompute.ai/noble/spack
      signed: true

  specs:
    - slurm_factory.slurm@26-05-5-1 +nvml +rsmi sysconfdir=/etc/slurm %gcc@13.3.0

  concretizer:
    unify: true
```

Then:

```bash
spack env create myenv spack.yaml
spack env activate myenv
spack buildcache keys --install --trust
spack install --cache-only
```

## Next Steps

- [Slurm Package Documentation](./packages/slurm.md): Explore available variants and versions
- [OpenSSL Package](./packages/openssl.md): Custom OpenSSL builds
- [FreeIPMI Package](./packages/freeipmi.md): IPMI support for hardware monitoring
- [Contributing](./contributing.md): Help improve this repository

## Troubleshooting

### Buildcache Not Found

If you get errors about packages not being in the buildcache:

```bash
# List available packages for every architecture
spack buildcache list --allarch

# Check mirror configuration
spack mirror list
```

Make sure the mirror's toolchain matches your OS: a `noble` build will not be reused on Rocky Linux.

### Compilation Fallback

If you don't use `--cache-only`, Spack will build from source if binaries aren't available. This can take several hours for Slurm and its dependencies.

### GPG Key Issues

If `spack buildcache keys` does not import the key, fetch it from a keyserver and trust it directly, as Slurm Factory does:

```bash
gpg --keyserver hkps://keyserver.ubuntu.com \
  --recv-keys FDEA90667641505264EFD114DFB92630BCA5AB71
gpg --armor --export FDEA90667641505264EFD114DFB92630BCA5AB71 > vantage-spack.pub
spack gpg trust vantage-spack.pub
```

## Getting Help

- [GitHub Issues](https://github.com/vantagecompute/slurm-factory-spack-repo/issues): Report bugs or request features
- [Contact](./contact.md): Get in touch with the maintainers
