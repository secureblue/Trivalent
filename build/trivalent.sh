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

# Sanitize & protect risky variables
declare -rx LD_PRELOAD=""
declare -rx LD_LIBRARY_PATH=""
declare -rx LD_AUDIT=""
declare -rx LD_PROFILE=""
declare -rx PATH="/usr/bin:/bin"
declare -rx HOME="$HOME"
declare -rx XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR"
declare -rx XAUTHORITY="$XAUTHORITY"
declare -rx DISPLAY="$DISPLAY"

# unify branding
declare -r CHROMIUM_NAME="@@CHROMIUM_NAME@@"

declare -rx CHROME_VERSION_EXTRA="Built from source for @@BUILD_TARGET@@"

# We don't want bug-buddy intercepting our crashes. http://crbug.com/24120
declare -rx GNOME_DISABLE_CRASH_DIALOG=SET_BY_GOOGLE_CHROME

# Let the wrapped binary know that it has been run through the wrapper.
CHROME_WRAPPER=$(readlink -f "$0")
declare -rx CHROME_WRAPPER
HERE=$(dirname "$CHROME_WRAPPER")
declare -r HERE

# obtain chromium flags from system file
# shellcheck source=build/trivalent.conf
[[ -f "/etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf" ]] && . "/etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf"
declare -r CHROMIUM_FLAGS="$CHROMIUM_FLAGS"

# desktop integration
declare -r xdg_app_dir="${XDG_DATA_HOME:-$HOME/.local/share/applications}"
mkdir -p "$xdg_app_dir"
[[ -f "$xdg_app_dir/mimeapps.list" ]] || touch "$xdg_app_dir/mimeapps.list"

# Check if Trivalent's subresource filter is installed,
# if so runs the installer
[[ -f "/usr/lib64/trivalent/install_filter.sh" ]] && /bin/bash /usr/lib64/trivalent/install_filter.sh

PROCESSES=$(ps aux)
echo "$PROCESSES" | grep "$CHROMIUM_NAME --type=zygote" | grep -v "grep" > /dev/null
IS_BROWSER_RUNNING=$?

# Fix Singleton process locking if the browser isn't running and the singleton files are present
if [[ $IS_BROWSER_RUNNING -eq 1 ]] && compgen -G "$HOME/.config/$CHROMIUM_NAME/Singleton*" > /dev/null; then
  echo "Ruh roh! This shouldn't be here..."
  rm "$HOME/.config/$CHROMIUM_NAME/Singleton"*
else
  echo "A process is already open in this directory or Singleton process files are not present."
fi

BWRAP_ARGS="--dev-bind / /"
[[ -f "/etc/ld.so.preload" ]] && BWRAP_ARGS+=" --ro-bind /dev/null /etc/ld.so.preload"

# Sanitize std{in,out,err} because they'll be shared with untrusted child
# processes (http://crbug.com/376567).
exec < /dev/null
exec > >(exec cat)
exec 2> >(exec cat >&2)

# shellcheck disable=SC2086
exec bwrap $BWRAP_ARGS "$HERE/$CHROMIUM_NAME" $CHROMIUM_FLAGS "$@"
