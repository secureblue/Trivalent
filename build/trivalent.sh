#!/bin/bash
#
# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# unify branding
export CHROMIUM_NAME="@@CHROMIUM_NAME@@"

# Let the wrapped binary know that it has been run through the wrapper.
export CHROME_WRAPPER="`readlink -f "$0"`"

HERE="`dirname "$CHROME_WRAPPER"`"

# We include some xdg utilities next to the binary, and we want to prefer them
# over the system versions when we know the system versions are very old. We
# detect whether the system xdg utilities are sufficiently new to be likely to
# work for us by looking for xdg-settings. If we find it, we leave $PATH alone,
# so that the system xdg utilities (including any distro patches) will be used.
if ! which xdg-settings &> /dev/null; then
  # Old xdg utilities. Prepend $HERE to $PATH to use ours instead.
  export PATH="$HERE:$PATH"
else
  # Use system xdg utilities. But first create mimeapps.list if it doesn't
  # exist; some systems have bugs in xdg-mime that make it fail without it.
  xdg_app_dir="${XDG_DATA_HOME:-$HOME/.local/share/applications}"
  mkdir -p "$xdg_app_dir"
  [ -f "$xdg_app_dir/mimeapps.list" ] || touch "$xdg_app_dir/mimeapps.list"
fi

export CHROME_VERSION_EXTRA="Built from source for @@BUILD_TARGET@@"

# We don't want bug-buddy intercepting our crashes. http://crbug.com/24120
export GNOME_DISABLE_CRASH_DIALOG=SET_BY_GOOGLE_CHROME

# Allow users to override command-line options and prefer user defined
# CHROMIUM_USER_FLAGS from env over system wide CHROMIUM_FLAGS
[[ -f /etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf ]] && . /etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf
CHROMIUM_FLAGS=${CHROMIUM_USER_FLAGS:-$CHROMIUM_FLAGS}

# handle migration from the old directory
# the migration file just tells this wrapper not to copy over data
NEW_DIR="$HOME/.config/$CHROMIUM_NAME"
OLD_DIR="$HOME/.config/chromium"
MIGRATION_FILE="$HOME/.config/.$CHROMIUM_NAME-migration"
if [[ ! -d "$NEW_DIR" && -d "$OLD_DIR" && ! -f "$MIGRATION_FILE" ]]; then
  echo "Migrating user data directory..."
  mv "$OLD_DIR" "$NEW_DIR"
else
  echo "Data directory already present, no old data to migrate, or data already migrated."
fi
if [[ ! -f "$MIGRATION_FILE" ]]; then
  echo "Remembering migration status..."
  touch "$MIGRATION_FILE"
fi

restorecon -vR $HOME/.config/$CHROMIUM_NAME
restorecon -vR $HOME/.cache/$CHROMIUM_NAME

# Check if Trivalent's subresource filter is installed,
# if so runs the installer
if [ -f "/usr/lib64/trivalent/install_filter.sh" ]; then
   /bin/bash /usr/lib64/trivalent/install_filter.sh
fi

PROCESSES=$(ps aux)
echo $PROCESSES | grep "$CHROMIUM_NAME --type=zygote" | grep -v "grep" > /dev/null
IS_TRIVALENT_RUNNING=$?

# Fix Singleton process locking if the browser isn't running and the singleton files are present
if [[ $IS_TRIVALENT_RUNNING -ne 0 ]] && [[ -f "$HOME/.config/$CHROMIUM_NAME/SingletonLock" ||
      -f "$HOME/.config/$CHROMIUM_NAME/SingletonCookie" || -f "$HOME/.config/$CHROMIUM_NAME/SingletonSocket" ]]; then
  echo "Ruh roh! This shouldn't be here..."
  rm "$HOME/.config/$CHROMIUM_NAME/Singleton"*
else
  echo "A process is already open in this directory or Singleton process files are not present."
fi

# Sanitize std{in,out,err} because they'll be shared with untrusted child
# processes (http://crbug.com/376567).
exec < /dev/null
exec > >(exec cat)
exec 2> >(exec cat >&2)

exec -a "$0" "$HERE/$CHROMIUM_NAME" $CHROMIUM_FLAGS "$@"
