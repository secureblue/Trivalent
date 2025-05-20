#!/bin/bash

# Sanitize & protect risky variables
readonly HOME="$HOME"
readonly PATH="/usr/bin:/bin"
readonly LD_PRELOAD=""
readonly LD_LIBRARY_PATH=""
readonly LD_AUDIT=""
readonly LD_PROFILE=""

# unify branding
readonly CHROMIUM_NAME="@@CHROMIUM_NAME@@"

# obtain chromium flags from system file
[[ -f /etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf ]] && . /etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf
readonly CHROMIUM_FLAGS="$CHROMIUM_FLAGS"

# desktop integration
xdg_app_dir="${XDG_DATA_HOME:-$HOME/.local/share/applications}"
mkdir -p "$xdg_app_dir"
[ -f "$xdg_app_dir/mimeapps.list" ] || touch "$xdg_app_dir/mimeapps.list"

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

export CHROME_VERSION_EXTRA="Built from source for @@BUILD_TARGET@@"

# We don't want bug-buddy intercepting our crashes. http://crbug.com/24120
export GNOME_DISABLE_CRASH_DIALOG=SET_BY_GOOGLE_CHROME

# Let the wrapped binary know that it has been run through the wrapper.
export CHROME_WRAPPER="`readlink -f "$0"`"
readonly HERE="`dirname "$CHROME_WRAPPER"`"

BWRAP_ARGS="--dev-bind / /"
if [ -f "/etc/ld.so.preload" ]; then
  BWRAP_ARGS+=" --ro-bind /dev/null /etc/ld.so.preload"
fi
if [ "$USE_WAYLAND" == "true" ]; then
  BWRAP_ARGS+=" --unshare-ipc" # prevent IPC where it isn't needed (x11 performance depends on IPC)
fi

# Sanitize std{in,out,err} because they'll be shared with untrusted child
# processes (http://crbug.com/376567).
exec < /dev/null
exec > >(exec cat)
exec 2> >(exec cat >&2)

exec /usr/bin/bwrap $BWRAP_ARGS "$HERE/$CHROMIUM_NAME" $CHROMIUM_FLAGS "$@"
