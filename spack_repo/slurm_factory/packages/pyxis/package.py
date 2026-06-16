# Copyright (c) 2025 Vantage Compute Corporation. and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from spack.package import *
from spack_repo.builtin.build_systems.makefile import MakefilePackage


class Pyxis(MakefilePackage):
    """
    NVIDIA Pyxis is a SPANK plugin for the Slurm workload manager.

    Pyxis allows unprivileged cluster users to run containerized tasks
    through the srun command. It is designed to work with Enroot as the
    container runtime, enabling seamless integration of containers into
    Slurm job submissions.
    """

    homepage = "https://github.com/NVIDIA/pyxis"
    url = "https://github.com/NVIDIA/pyxis/archive/refs/tags/v0.21.0.tar.gz"

    license("Apache-2.0")

    version("0.24.0", sha256="9c4cdb79a67301d8ea05951aa4d2c205f40cf6145e338214b0191add8b36d6c4")

    depends_on("c", type="build")

    # Pyxis builds against slurm headers (spank.h)
    depends_on("slurm_factory.slurm", type=("build", "link"))

    @property
    def build_targets(self):
        spec = self.spec
        slurm_prefix = spec["slurm_factory.slurm"].prefix
        return [
            f"CPPFLAGS=-I{slurm_prefix}/include",
            "CC={0}".format(spack_cc),
        ]

    @property
    def install_targets(self):
        return [
            "install",
            f"prefix={self.prefix}",
            f"libdir={self.prefix}/lib",
        ]

    @run_after("install")
    def fixup_plugin_rpath(self):
        """Fix RPATH on spank_pyxis.so so it can find slurm libs at runtime."""
        import spack.util.executable as exe

        plugin = os.path.join(self.prefix.lib, "slurm", "spank_pyxis.so")
        if not os.path.exists(plugin):
            return

        patchelf = exe.which("patchelf")
        if not patchelf:
            return

        try:
            current_rpath = patchelf("--print-rpath", plugin, output=str).strip()
            parts = [p for p in current_rpath.split(":") if p]
            if "$ORIGIN/.." not in parts:
                parts.insert(0, "$ORIGIN/..")
            patchelf("--set-rpath", ":".join(parts), plugin)
        except Exception:
            pass
