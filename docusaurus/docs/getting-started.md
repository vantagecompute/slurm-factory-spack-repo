# Getting Started

This guide will help you get started with installing Slurm from the Slurm Factory Spack buildcache.

## Prerequisites

You need:

- A Linux system (Ubuntu 22.04+, RHEL 8+, or similar)
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

Add the Slurm Factory buildcache mirrors:

```bash
# Add GCC compiler buildcache
spack mirror add slurm-factory-gcc \\
  https://slurm-factory-spack-binary-cache.vantagecompute.ai/compilers/15.2.0

# Add Slurm buildcache
spack mirror add slurm-factory-slurm \\
  https://slurm-factory-spack-binary-cache.vantagecompute.ai/slurm/25.11/15.2.0
```

Trust the buildcache GPG keys:

```bash
spack buildcache keys --install --trust
```

### Step 3: Install GCC Compiler (Optional)

If you want to use the same GCC version that was used to build Slurm:

```bash
# Install GCC 15.2.0 from buildcache
spack install --cache-only gcc@15.2.0

# Register it as a compiler
spack compiler find $(spack location -i gcc@15.2.0)

# Verify
spack compiler list | grep gcc@15.2.0
```

### Step 4: Install Slurm

Install Slurm from the buildcache:

```bash
# Install the latest Slurm 25.11
spack install --cache-only slurm@25-11-0-1
```

Or install by exact hash for reproducibility:

```bash
# This installs slurm@25-11-0-1%gcc@15.2.0
spack install --cache-only /ysm2idt
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

Here's a complete Dockerfile that demonstrates installing Slurm from the buildcache:

```dockerfile
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential ca-certificates curl git \\
    gcc g++ gfortran python3 unzip

# Install Spack
RUN git clone --depth 1 --branch v1.0.0 \\
    https://github.com/spack/spack.git /opt/spack

ENV SPACK_ROOT=/opt/spack
ENV PATH=$SPACK_ROOT/bin:$PATH

SHELL ["/bin/bash", "-l", "-c"]

# Add custom repository
RUN git clone --depth 1 \\
    https://github.com/vantagecompute/slurm-factory-spack-repo.git \\
    /opt/slurm-factory-spack-repo && \\
    spack repo add /opt/slurm-factory-spack-repo/spack_repo/slurm_factory

# Configure buildcache mirrors
RUN spack mirror add slurm-factory-gcc \\
    https://slurm-factory-spack-binary-cache.vantagecompute.ai/compilers/15.2.0 && \\
    spack mirror add slurm-factory-slurm \\
    https://slurm-factory-spack-binary-cache.vantagecompute.ai/slurm/25.11/15.2.0

# Trust buildcache keys
RUN spack buildcache keys --install --trust

# Install GCC compiler
RUN spack install --cache-only gcc@15.2.0 && \\
    spack compiler find $(spack location -i gcc@15.2.0)

# Install Slurm
RUN spack install --cache-only /ysm2idt

# Verify installation
RUN spack find slurm && \\
    $(spack location -i slurm)/bin/srun --version

CMD ["/bin/bash"]
```

See the complete example in [`examples/Dockerfile.install-from-buildcache-with-repo`](https://github.com/vantagecompute/slurm-factory-spack-repo/blob/main/examples/Dockerfile.install-from-buildcache-with-repo).

## Building from Source

If you prefer to build from source or need a custom configuration:

```bash
# Install with specific variants
spack install slurm@25-11-0-1 +pmix +hwloc +restd +ipmi
```

Available variants are documented in the [Slurm package documentation](./packages/slurm).

## Using in spack.yaml

For environment-based workflows, add to your `spack.yaml`:

```yaml
spack:
  repos:
    - slurm_factory:
        git: https://github.com/vantagecompute/slurm-factory-spack-repo.git
  
  mirrors:
    slurm-factory-gcc: 
      url: https://slurm-factory-spack-binary-cache.vantagecompute.ai/compilers/15.2.0
    slurm-factory-slurm:
      url: https://slurm-factory-spack-binary-cache.vantagecompute.ai/slurm/25.11/15.2.0
  
  specs:
    - slurm@25-11-0-1
  
  concretizer:
    unify: true
```

Then:

```bash
spack env create myenv spack.yaml
spack env activate myenv
spack install --cache-only
```

## Next Steps

- [Slurm Package Documentation](./packages/slurm) - Explore available variants and versions
- [OpenSSL Package](./packages/openssl) - Custom OpenSSL builds
- [FreeIPMI Package](./packages/freeipmi) - IPMI support for hardware monitoring
- [Contributing](./contributing) - Help improve this repository

## Troubleshooting

### Buildcache Not Found

If you get errors about packages not being in the buildcache:

```bash
# List available packages
spack buildcache list --allarch

# Check mirror configuration
spack mirror list
```

### Compilation Fallback

If you don't use `--cache-only`, Spack will build from source if binaries aren't available. This can take several hours for Slurm and dependencies.

### GPG Key Issues

If you have GPG key errors:

```bash
# Force trust all keys
spack buildcache keys --install --trust --force
```

## Getting Help

- [GitHub Issues](https://github.com/vantagecompute/slurm-factory-spack-repo/issues) - Report bugs or request features
- [Contact](./contact) - Get in touch with the maintainers
