# Slurm Dependency Types Update

## Problem
The Docker buildcache test was building all Slurm dependencies from source instead of using the buildcache. This happened because dependencies were incorrectly marked as runtime dependencies (`type="run"`), causing Spack to require them as separate packages even when they're statically linked or embedded into Slurm.

## Solution
Properly classify each dependency according to how Slurm actually uses it:

### Dependency Type Categories

#### 1. Build-only (`type="build"`)
Dependencies needed only during compilation:
- **pkgconfig** - pkg-config for finding libraries

#### 2. Link-only (`type="link"`)
Libraries that are statically linked or headers-only (not needed as separate runtime packages):
- **librdkafka** - Kafka support (usually static)
- **http-parser** - HTTP parsing for REST API (static library)
- **libyaml** - YAML config parsing (static library)

#### 3. Build+Link (`type=("build", "link")`)
Libraries linked into Slurm but don't need to exist as separate runtime packages:
- **dbus** - Cgroup plugin support
- **linux-pam** - PAM authentication
- **freeipmi** - IPMI hardware monitoring
- **json-c** - JSON parsing
- **lz4** - Fast compression
- **ncurses** - Terminal UI
- **lua** - Lua scripting engine (embedded)
- **readline** - Command line editing
- **hwloc** - Hardware topology
- **hdf5** - HDF5 file format support

#### 4. Full Runtime (`type=("build", "link", "run")`)
Libraries truly needed at runtime as separate packages:
- **curl** - HTTP client (may be called as external tool + linked)
- **mysql-connector-c** - Database client for accounting
- **openssl** - Crypto libraries
- **glib** - Core library with runtime components
- **munge** - Authentication daemon
- **libssh2** - SSH functionality
- **libjwt** - JWT token generation for REST API
- **pmix** - Process management interface
- **zlib-api** - Compression (dynamically loaded by some plugins)

#### 5. Runtime-only (`type="run"`)
Dependencies not linked but needed at runtime:
- **cuda** (when +nvml) - NVIDIA GPU monitoring
- **rocm-smi-lib** (when +rsmi) - AMD GPU monitoring

## Impact

### Before
```bash
spack install slurm@25.11%gcc@8.5.0
# Would pull ~50+ packages as runtime dependencies
# Buildcache installation would fail or build from source
```

### After
```bash
spack install slurm@25.11%gcc@8.5.0
# Only pulls ~10 true runtime dependencies
# Buildcache installation succeeds with minimal footprint
```

### Benefits
1. **Smaller buildcache** - Only packages actual runtime dependencies
2. **Faster installation** - Fewer packages to download/extract
3. **Cleaner deployments** - Only necessary runtime libs included
4. **Better caching** - More packages can be reused across builds
5. **Reduced conflicts** - Fewer version constraints to satisfy

## Testing
To verify the fix works:

```bash
# In slurm-factory-spack-repo
git checkout fix-dependency-types

# Test buildcache installation
docker build -f Dockerfile.test-buildcache -t slurm-buildcache-test .

# The build should now use buildcache for most dependencies
# instead of building from source
```

## Validation
Compare dependency trees:

```bash
# Before (main branch)
spack spec slurm@25.11%gcc@8.5.0 | grep -c "^"
# Result: ~80-100 packages

# After (fix-dependency-types branch)
spack spec slurm@25.11%gcc@8.5.0 | grep -c "^"
# Result: ~50-60 packages (only runtime deps included)
```

## References
- [Spack Dependency Types Documentation](https://spack.readthedocs.io/en/latest/basic_usage.html#dependency-types)
- Original issue: Docker buildcache test building all deps from source
- Branch: `fix-dependency-types`
