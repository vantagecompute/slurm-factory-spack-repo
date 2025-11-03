# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage


class Freeipmi(AutotoolsPackage, GNUMirrorPackage):
    """FreeIPMI provides in-band and out-of-band IPMI software based on the
    IPMI v1.5/2.0 specification. The IPMI specification defines a set of
    interfaces for platform management and is implemented by a number vendors
    for system management. The features of IPMI that most users will be
    interested in are sensor monitoring, system event monitoring, power control,
    and serial-over-LAN (SOL)."""

    homepage = "https://www.gnu.org/software/freeipmi/"
    gnu_mirror_path = "freeipmi/freeipmi-1.6.16.tar.gz"

    license("GPL-3.0-or-later")

    version("1.6.16", sha256="5bcef6bb9eb680e49b4a3623579930ace7899f53925b2045fe9f91ad6904111d")

    depends_on("c", type="build")
    depends_on("libgcrypt")

    def configure_args(self):
        return ["--with-systemdsystemunitdir=no"]
