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

"""CUDA, extended with releases newer than the builtin Spack recipe carries."""

import platform

from spack.package import *
from spack_repo.builtin.packages.cuda.package import Cuda as BuiltinCuda

# Releases NVIDIA has published that the builtin recipe does not have yet, in
# the builtin `_versions` format: (sha256, url) per platform.system()-machine().
# Drop an entry once spack-packages adds it.
_versions = {
    "13.4.3": {
        "Linux-aarch64": (
            "310bc2b79ef298f46e40e08cdd86d11565bd02a8c24aad417223bda6c67e7bcf",
            "https://developer.download.nvidia.com/compute/cuda/13.4.3/local_installers/cuda_13.4.3_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "4592f8040b845166ff209a49024dd79bdd3fa157ddb76ae8f59f4f2dd2a274f0",
            "https://developer.download.nvidia.com/compute/cuda/13.4.3/local_installers/cuda_13.4.3_linux.run",
        ),
    },
}


class Cuda(BuiltinCuda):
    """
    CUDA Toolkit: the builtin recipe plus newer NVIDIA releases.

    Slurm links CUDA for NVML GPU autodetection (``+nvml``). Every build step,
    variant and older version comes from the builtin ``cuda`` package; this
    class only registers releases the builtin recipe does not list yet.
    """

    for ver, packages in _versions.items():
        pkg = packages.get(f"{platform.system()}-{platform.machine()}")
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1], expand=False)
