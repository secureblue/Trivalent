#!/bin/bash

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

repo_directory=$(pwd)

readonly vanadium_patches_path="./vanadium_patches/"
readonly vanadium_git_url="https://github.com/GrapheneOS/Vanadium.git"
current_vanadium_patches=()
truncated_vanadium_patches=()
remote_vanadium_patches=()
truncated_remote_vanadium_patches=()

readonly fedora_patches_path="./fedora_patches/"
readonly fedora_git_url="https://src.fedoraproject.org/rpms/chromium.git"
current_fedora_patches=()
remote_fedora_patches=()

get_remote_vanadium_patches() {
	cd vanadium-patches-tmp/
	retry=0
	while true; do
		git clone "$vanadium_git_url"
		if [ ! -d Vanadium/patches/ ]; then
			rm -rf Vanadium/
			echo "ERROR! git operation failed!"
			if [[ $retry -gt 0 ]]; then
				echo "Failed to clone $((retry+1)) times..."
			fi
			if [[ $retry == 2 ]]; then
				echo "Aborting!"
				cd "$repo_directory"
				rm -rf vanadium-patches-tmp/
				exit 1
			fi
			echo "Retrying..."
			retry=$((retry+1))
		else
			break
		fi
	done
	cd Vanadium/patches/
	remote_vanadium_patches=(*.patch)
	for ((i=0; i<${#remote_vanadium_patches[@]}; i++)); do
		if [[ ${remote_vanadium_patches[$i]} =~ ^[0-9]{4}[\-] ]]; then
			truncated_remote_vanadium_patches[i]="${remote_vanadium_patches[$i]:4}"
		else
			echo "ERROR! Remote patch ${remote_vanadium_patches[$i]} does match expected naming scheme!"
			echo "Aborting!"
			cd "$repo_directory"
			rm -rf vanadium-patches-tmp/
			exit 1
		fi
	done
	cd "$repo_directory"
}

update_vanadium_patches() {
	get_remote_vanadium_patches
	cd "$vanadium_patches_path"
	current_vanadium_patches=(*.patch)
	for ((i=0; i<${#current_vanadium_patches[@]}; i++)); do
		truncated_vanadium_patches[i]="${current_vanadium_patches[$i]:4}"
	done
	updated_counter=0
	removed_counter=0
	patch_not_found_counter=0
	for ((i=0; i<${#truncated_vanadium_patches[@]}; i++)); do
		for ((j=0; j<${#truncated_remote_vanadium_patches[@]}; j++)); do
			if [[ "${truncated_remote_vanadium_patches[$j]}" == "${truncated_vanadium_patches[$i]}" ]]; then
				if [[ "${remote_vanadium_patches[$j]}" == "${current_vanadium_patches[$i]}" ]]; then
					echo "Updating patch ${current_vanadium_patches[$i]}"
					echo "	No name change"
				else
					echo "Updating patch ${current_vanadium_patches[$i]}"
					echo "	Patch renamed to: ${remote_vanadium_patches[$j]}"
				fi
				rm "${current_vanadium_patches[$i]}"
				cp "$repo_directory/vanadium-patches-tmp/Vanadium/patches/${remote_vanadium_patches[$j]}" ./
				updated_counter=$((updated_counter+1))
			else
				patch_not_found_counter=$((patch_not_found_counter+1))
			fi
		done
		# Assume, since the patch has not been found, the patch has been removed
		if [[ $patch_not_found_counter == "${#truncated_remote_vanadium_patches[@]}" ]]; then
			echo "Removing ${current_vanadium_patches[i]}"
			echo "	Patch has been removed in Vanadium"
			rm "${current_vanadium_patches[$i]}"
			removed_counter=$((removed_counter+1))
		fi
		patch_not_found_counter=0
	done
	echo ""
	echo "Updated $updated_counter patches."
	echo "Removed $removed_counter patches."
	cd "$repo_directory"
}

update_fedora_patches() {
	cd fedora-patches-tmp
	git clone "$fedora_git_url"
	cd chromium
	remote_fedora_patches=(*.patch)
	cd "$repo_directory/$fedora_patches_path"
	current_fedora_patches=(*.patch)
	updated_counter=0
	removed_counter=0
	patch_not_found_counter=0
	for ((i=0; i<${#current_fedora_patches[@]}; i++)); do
		for ((j=0; j<${#remote_fedora_patches[@]}; j++)); do
			if [[ "${remote_fedora_patches[$j]}" == "${current_fedora_patches[$i]}" ]]; then
				echo "Updating patch ${current_fedora_patches[$i]} from Fedora"
				rm "${current_fedora_patches[$i]}"
				cp "$repo_directory/fedora-patches-tmp/chromium/${remote_fedora_patches[$j]}" ./
				updated_counter=$((updated_counter+1))
			else
				patch_not_found_counter=$((patch_not_found_counter+1))
			fi
		done
		if [[ $patch_not_found_counter == "${#remote_fedora_patches[@]}" ]]; then
			echo "Deleting removed patch ${current_fedora_patches[i]}"
			rm "${current_fedora_patches[$i]}"
			removed_counter=$((removed_counter+1))
		fi
		patch_not_found_counter=0
	done
	echo ""
	echo "Updated $updated_counter patches."
	echo "Removed $removed_counter patches."
	cd "$repo_directory"
}

mkdir vanadium-patches-tmp/ # create a temporary directory for cloning the Vanadium patches
update_vanadium_patches
rm -rf vanadium-patches-tmp/ # cleanup

mkdir fedora-patches-tmp/ # create a temporary directory for cloning the Fedora patches
update_fedora_patches
rm -rf fedora-patches-tmp/ # cleanup
exit 0
