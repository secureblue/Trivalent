#! /bin/bash -x

# Copyright 2025-2026 The Trivalent Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


set -oue pipefail

BUILD_DIR="$(pwd)"
declare -r BUILD_DIR

cd Trivalent

shopt -s nullglob

pushd build
	cp install/* "${BUILD_DIR}"
	cp resources/* "${BUILD_DIR}"
	cp selinux/* "${BUILD_DIR}"
	pushd patches
		declare -i reversecount=0
		function mv_patch() {
			local -r patch="${1}"
			local -r source="${2}"
			local -i count="${3}"
			
			if [[ "${patch:0:8}" == "REVERSE-" ]]; then
				cp "${patch}" "${BUILD_DIR}/reverse-$((reversecount+4000)).patch"
				((++reversecount))
			else
				cp "${patch}" "${BUILD_DIR}/${source}-${count}.patch"
				((++count))
			fi
			return "${count}"
		}

		pushd trivalent/
			for dir in *; do
				if [[ -d "${dir}" ]]; then
					mv "${dir}/"*.patch .
				fi
			done
			patches=(*.patch)
			count=0
			for ((i=0; i<${#patches[@]}; i++)); do
				count="$(mv_patch "${patches[i]}" "trivalent" "$((count+3000))")"
			done
		popd

		pushd third_party/
			pushd fedora/
				patches=(*.patch)
				count=0
				for ((i=0; i<${#patches[@]}; i++)); do
					count="$(mv_patch "${patches[i]}" "fedora" "$((count+1000))")"
				done
			popd

			pushd vanadium/
				patches=(*.patch)
				count=0
				for ((i=0; i<${#patches[@]}; i++)); do
					count="$(mv_patch "${patches[i]}" "vanadium" "$((count+2000))")"
				done
			popd
		popd
	popd
popd


# Move all the source files into the parent directory for the COPR build system to find them
cp /usr/src/chromium/chromium-*-clean.tar.xz "${BUILD_DIR}"
cp /usr/src/chromium/chromium-version.txt "${BUILD_DIR}"
