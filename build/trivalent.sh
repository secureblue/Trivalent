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

# Exit immediately if run as root
if [ "$(id -u)" -eq 0 ]; then
  echo "Trivalent must not be run as root."
  exit 1
fi

# Make filename expansion patterns (like *.conf) expand to nothing if no files match the pattern.
shopt -s nullglob

# Sanitize & protect risky variables
declare -rx LD_LIBRARY_PATH=""
declare -rx LD_AUDIT=""
declare -rx LD_PROFILE=""
declare -rx PATH="/usr/bin:/bin"
declare -rx HOME="$HOME"
declare -rx XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR"
declare -rx XAUTHORITY="$XAUTHORITY"
declare -rx DISPLAY="$DISPLAY"

ARCH="$(uname -m)"
declare -r ARCH

# enable hardware CFI feature
# https://www.gnu.org/software/libc/manual/html_node/Hardware-Capability-Tunables.html
if [[ "$ARCH" == "x86_64" ]]; then
  declare -rx GLIBC_TUNABLES="glibc.cpu.x86_ibt=on:glibc.cpu.x86_shstk=permissive"
fi

# unify branding
declare -r CHROMIUM_NAME="@@CHROMIUM_NAME@@"

declare -rx CHROME_VERSION_EXTRA="Built from source for @@BUILD_TARGET@@"

# We don't want bug-buddy intercepting our crashes. http://crbug.com/24120
declare -rx GNOME_DISABLE_CRASH_DIALOG=SET_BY_GOOGLE_CHROME

# Let the wrapped binary know that it has been run through the wrapper.
CHROME_WRAPPER=$(readlink -f "$0")
declare -rx CHROME_WRAPPER
HERE="${CHROME_WRAPPER%/*}"
declare -r HERE

# BROWSER_LOG_LEVEL=[0,1,2]
declare -ix BROWSER_LOG_LEVEL="${BROWSER_LOG_LEVEL:0}"

# USE_VULKAN=[true,false]
declare USE_VULKAN="${USE_VULKAN}:false}"

declare FEATURES
declare CHROMIUM_FLAGS

# obtain extra flags that are likely user-configured
if [[ -d "/etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf.d" ]]; then
  for conf_file in "/etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf.d"/*.conf; do
    # shellcheck source=/etc/trivalent/trivalent.conf.d/99-example.conf
    source "$conf_file"
  done
fi

# obtain chromium flags from system file
# shellcheck source=build/trivalent.conf
declare CHROMIUM_SYSTEM_FLAGS
if [[ -f "/etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf" ]]; then
  # shellcheck source=build/trivalent.conf
  source "/etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf"
fi

declare -r CHROMIUM_ALL_FLAGS="$CHROMIUM_FLAGS $CHROMIUM_SYSTEM_FLAGS"

# desktop integration
declare -r xdg_app_dir="${XDG_DATA_HOME:-$HOME/.local/share/applications}"
mkdir -p "$xdg_app_dir"
[[ -f "$xdg_app_dir/mimeapps.list" ]] || touch "$xdg_app_dir/mimeapps.list"

# Check if Trivalent's subresource filter is installed,
# if so runs the installer
if [[ -f "/usr/lib64/trivalent/install_filter.sh" ]] ; then
  /bin/bash /usr/lib64/trivalent/install_filter.sh
fi

pgrep -ax -U "$(id -ru)" "$CHROMIUM_NAME" | grep -Fq " --type=zygote"
IS_BROWSER_RUNNING=$?

# Fix Singleton process locking if the browser isn't running and the singleton files are present
if [[ $IS_BROWSER_RUNNING -eq 1 ]] && compgen -G "$HOME/.config/$CHROMIUM_NAME/Singleton*" > /dev/null; then
  [[ "$BROWSER_LOG_LEVEL" -gt 0 ]] && echo "Ruh roh! This shouldn't be here..."
  rm "$HOME/.config/$CHROMIUM_NAME/Singleton"*
else
  [[ "$BROWSER_LOG_LEVEL" -gt 0 ]] && echo "A process is already open in this directory or Singleton process files are not present."
fi

declare -r TMPFS_CACHE_DIR="/tmp/${CHROMIUM_NAME}_cache/"
mkdir -p "$TMPFS_CACHE_DIR"

declare BWRAP_ARGS="--dev-bind / /"
BWRAP_ARGS+=" --cap-drop ALL" # if the browser has capabilities, that is very concerning
BWRAP_ARGS+=" --ro-bind-try /dev/null /etc/ld.so.preload" # avoid ld preload usage
BWRAP_ARGS+=" --bind $TMPFS_CACHE_DIR $HOME/.cache" # avoid issues with other applications messing with cache
BWRAP_ARGS+=" --setenv GDK_DISABLE icon-nodes" # avoid issues with glycin

# Do this at the end so that everything else still gets hardened_malloc
declare -rx LD_PRELOAD=""

# Sanitize std{in,out,err} because they'll be shared with untrusted child
# processes (http://crbug.com/376567).
exec < /dev/null
exec > >(exec cat)
exec 2> >(exec cat >&2)

# shellcheck disable=SC2086
exec bwrap $BWRAP_ARGS -- "$HERE/$CHROMIUM_NAME" $CHROMIUM_ALL_FLAGS "$@"
