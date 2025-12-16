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

wget https://versionhistory.googleapis.com/v1/chrome/platforms/linux/channels/stable/versions/all/releases?filter=endtime=none -O chromium-version.json
grep \"version\" chromium-version.json | grep -oh "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" > chromium-version.txt

cd Trivalent

shopt -s nullglob

# copy Fedora patches to the build dir
pushd fedora_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp "${patches[i]}" "../build/fedora-$((i+1000)).patch"
done
popd

# copy Vanadium patches to the build dir
pushd vanadium_patches/
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp "${patches[i]}" "../build/vanadium-$((i+2000)).patch"
done
popd

# copy Trivalent patches to the build dir
pushd patches/
cp ../translation_patches/register-trivalent-strings.patch ./
cp ../translation_patches/translations/*.patch ./
patches=(*.patch)
for ((i=0; i<${#patches[@]}; i++)); do
	cp "${patches[i]}" "../build/trivalent-$((i+3000)).patch"
done
popd

# Move all the source files into the parent directory for the COPR build system to find them
cp /usr/src/chromium/chromium-*-clean.tar.xz ../
mv ./build/* ../
