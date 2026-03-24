#! /bin/bash -x

# Copyright 2025 The Trivalent Authors
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

shopt -s nullglob

declare -r build_dir="$(pwd)"

cp /usr/src/chromium/chromium-*-clean.tar.xz "${build_dir}/"
cp /usr/src/chromium/chromium-version.txt "${build_dir}/"

pushd Trivalent/

pushd build/

# Move all the source files into the parent directory for the COPR build system to find them
cp ./branding/* "${build_dir}/"
cp ./install/* "${build_dir}/"
cp ./selinux/* "${build_dir}/"
cp ./trivalent.spec "${build_dir}/"

pushd patches/

pushd fedora_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	mv "${patches[i]}" "${build_dir}/fedora-$((i+1000)).patch"
done
popd #fedora_patches/

pushd vanadium_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	mv "${patches[i]}" "${build_dir}/vanadium-$((i+2000)).patch"
done
popd #vanadium_patches/

pushd trivalent_patches/
cp translation_patches/register-trivalent-strings.patch ./
cp translation_patches/translations/*.patch ./
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp "${patches[i]}" "${build_dir}/trivalent-$((i+3000)).patch"
done
popd #trivalent_patches/

popd #patches/

popd #build/

popd #Trivalent/
