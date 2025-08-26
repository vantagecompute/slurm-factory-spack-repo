# FreeIPMI Package

This package provides FreeIPMI support for hardware monitoring in Slurm clusters.

## Overview

FreeIPMI is a collection of Intelligent Platform Management Interface (IPMI) system software that provides in-band and out-of-band management of local and remote systems. When integrated with Slurm via the `+ipmi` variant, it enables hardware monitoring and power management features.

## Why Use FreeIPMI with Slurm?

Integrating FreeIPMI with Slurm enables:

- **Hardware Monitoring** - Temperature, voltage, fan speeds
- **Power Management** - Power capping and monitoring
- **Energy Accounting** - Track energy consumption per job
- **Health Checks** - Automated node health monitoring
- **Predictive Maintenance** - Identify failing hardware before it causes issues

## Installation

### With Slurm

Enable IPMI support when installing Slurm:

```bash
spack install slurm@25-11-0-1 +ipmi
```

This automatically installs FreeIPMI as a dependency.

### Standalone Installation

To install FreeIPMI independently:

```bash
spack install slurm_factory.freeipmi
```

## Usage with Slurm

Once Slurm is built with `+ipmi`, configure IPMI monitoring in `slurm.conf`:

```conf
# Enable IPMI-based power management
AcctGatherEnergyType=acct_gather_energy/ipmi

# Optional: Set IPMI polling frequency
AcctGatherNodeFreq=30
```

### Viewing Energy Data

After configuration, energy data appears in job accounting:

```bash
sacct -j <jobid> --format=JobID,ConsumedEnergy,ConsumedEnergyRaw
```

### Node Power Monitoring

Monitor real-time power consumption:

```bash
scontrol show node <nodename> | grep CurrentWatts
```

## Configuration

### IPMI Credentials

FreeIPMI may require IPMI credentials. Configure in `/etc/freeipmi/freeipmi.conf` or via Slurm's IPMI configuration.

### Permissions

IPMI device access requires appropriate permissions:

```bash
# Add slurm user to ipmi group (if applicable)
usermod -a -G ipmi slurm

# Or ensure /dev/ipmi0 is accessible
ls -l /dev/ipmi*
```

## Supported Features

FreeIPMI provides access to:

- **Sensor Data** - Temperature, voltage, current, fan speeds
- **Power Consumption** - Real-time and historical power usage
- **System Event Log (SEL)** - Hardware event logging
- **Chassis Control** - Power on/off, reset
- **Field Replaceable Units (FRU)** - Hardware inventory

## Hardware Requirements

IPMI support requires:

- **BMC (Baseboard Management Controller)** - IPMI-compliant hardware
- **IPMI Interface** - In-band (KCS) or out-of-band (LAN) access
- **Kernel Support** - IPMI device drivers loaded

Check IPMI availability:

```bash
# Check for IPMI device
ls /dev/ipmi*

# Test IPMI access
ipmi-sensors --quiet-cache --sdr-cache-recreate
```

## Troubleshooting

### No IPMI Device

If `/dev/ipmi*` doesn't exist:

```bash
# Load IPMI kernel modules
modprobe ipmi_devintf
modprobe ipmi_si

# Verify
lsmod | grep ipmi
```

### Permission Denied

If Slurm can't access IPMI:

```bash
# Check device permissions
ls -l /dev/ipmi0

# Fix permissions (temporary)
chmod 666 /dev/ipmi0

# Fix permanently via udev rules
echo 'KERNEL=="ipmi*", MODE="0666"' > /etc/udev/rules.d/90-ipmi.rules
```

### No Sensor Data

If sensors return no data:

```bash
# Clear and rebuild sensor cache
ipmi-sensors --quiet-cache --sdr-cache-recreate

# Test with verbose output
ipmi-sensors -vv
```

## Package Source

- **Homepage**: [https://www.gnu.org/software/freeipmi/](https://www.gnu.org/software/freeipmi/)
- **Package Definition**: [`packages/freeipmi/package.py`](https://github.com/vantagecompute/slurm-factory-spack-repo/blob/main/spack_repo/slurm_factory/packages/freeipmi/package.py)

## License

FreeIPMI is licensed under GPL-3.0-or-later.

## See Also

- [Slurm Package](./slurm) - Enable with `+ipmi` variant
- [Getting Started](../getting-started) - Installation guide
- [Slurm Power Management](https://slurm.schedmd.com/power_mgmt.html) - Official docs
