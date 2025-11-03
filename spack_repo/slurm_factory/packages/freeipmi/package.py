# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freeipmi(Package):
    """FreeIPMI provides in-band and out-of-band IPMI software based on the
    IPMI v1.5/2.0 specification. The IPMI specification defines a set of
    interfaces for platform management and is implemented by a number vendors
    for system management. The features of IPMI that most users will be
    interested in are sensor monitoring, system event monitoring, power control,
    and serial-over-LAN (SOL)."""

    homepage = "https://www.gnu.org/software/freeipmi/"
    url = "https://ftpmirror.gnu.org/freeipmi/freeipmi-1.6.16.tar.gz"

    maintainers("slurm-factory")

    license("GPL-3.0-or-later")

    version("1.6.16", sha256="5bcef6bb9eb680e49b4a3623579930ace7899f53925b2045fe9f91ad6904111d")

    depends_on("libgcrypt")

    def install(self, spec, prefix):
        """Manual configure, make, install to avoid AutotoolsPackage dependencies"""
        configure = Executable("./configure")
        configure(
            f"--prefix={prefix}",
            "--with-systemdsystemunitdir=no",
        )
        make()
        make("install")
