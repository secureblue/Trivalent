#!/bin/bash

# Sanitize & protect risky variables
readonly HOME="$HOME"
readonly XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR"
readonly PATH="/usr/bin:/bin"
readonly LD_PRELOAD=""
readonly LD_LIBRARY_PATH=""
readonly LD_AUDIT=""
readonly LD_PROFILE=""

# unify branding
readonly CHROMIUM_NAME="@@CHROMIUM_NAME@@"

# Sandbox parameter parsing logic
readonly SANDBOX_PARAMS="$SANDBOX_PARAMS"
function param_present() {
  echo "$SANDBOX_PARAMS" | tr "," '\n' | grep -F -x -q "$1"
}
function determine_sandbox_args() {
  # Initial args, these are transparent and do nothing on their own
  BWRAP_ARGS="--dev-bind / /" # Broad-full device access
  BWRAP_ARGS+=" --proc /proc" # procfs (for process management)
  [[ -f "/etc/ld.so.preload" ]] && BWRAP_ARGS+=" --ro-bind /dev/null /etc/ld.so.preload" # prevent system ld preload
  BWRAP_ARGS+=" --cap-drop ALL" # drop all capabilities, we always want to do this
  if ! param_present "nosandbox"; then
    # Filesystem Limits
    if ! param_present "nohidedevices"; then
      BWRAP_ARGS+=" --dev /dev" # create a fresh /dev directory
      ! param_present "hidegpudevice" && BWRAP_ARGS+=" --dev-bind /dev/dri /dev/dri" # GPU device access
      ! param_present "hideusbdevices" && BWRAP_ARGS+=" --dev-bind /dev/usb /dev/usb" # USB device access
    fi
    if param_present "ephemeralprofile"; then
      BWRAP_ARGS+=" --tmpfs $HOME" # mount user directories as tmpfs to prevent persistent data
      BWRAP_ARGS+=" --ro-bind $XDG_RUNTIME_DIR $XDG_RUNTIME_DIR" # mount xdg-run immutable to prevent potential persistence
      BWRAP_ARGS+=" --tmpfs /tmp" # create a new /tmp
    elif param_present "protecthome"; then
      BWRAP_ARGS+=" --ro-bind $HOME $HOME" # Prevent any writes to HOME, this includes downloads
      BWRAP_ARGS+=" --bind $HOME/.config/trivalent $HOME/.config/trivalent" # Allow access to Trivalent's data directory
      ! param_present "protectdownloads" && BWRAP_ARGS+=" --bind $HOME/Downloads $HOME/Downloads" # Prevent downloads access if the user wants it
    fi
    # Privilege Seperation
    param_present "dettachfromterminal" && BWRAP_ARGS+=" --new-session"
    param_present "unshareuser" && BWRAP_ARGS+=" --unshare-user"
    param_present "unsharepid" && BWRAP_ARGS+=" --unshare-pid"
    [[ "$USE_WAYLAND" == "true" ]] && BWRAP_ARGS+=" --unshare-ipc"
    if ! param_present "shareuts"; then
      BWRAP_ARGS+=" --unshare-uts"
      BWRAP_ARGS+=" --hostname $CHROMIUM_NAME"
    fi
    BWRAP_ARGS+=" --unshare-cgroup"
  fi
  BWRAP_ARGS+=" -- "
  echo "$BWRAP_ARGS" # return
}

# Let the wrapped binary know that it has been run through the wrapper.
readonly CHROME_WRAPPER="`readlink -f "$0"`"
readonly HERE="`dirname "$CHROME_WRAPPER"`"

# obtain chromium flags from system file
[[ -f /etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf ]] && . /etc/$CHROMIUM_NAME/$CHROMIUM_NAME.conf
readonly CHROMIUM_FLAGS="$CHROMIUM_FLAGS"

export CHROME_VERSION_EXTRA="Built from source for @@BUILD_TARGET@@"

# We don't want bug-buddy intercepting our crashes. http://crbug.com/24120
export GNOME_DISABLE_CRASH_DIALOG=SET_BY_GOOGLE_CHROME

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

readonly BWRAP_ARGS="$( determine_sandbox_args )"

# Sanitize std{in,out,err} because they'll be shared with untrusted child
# processes (http://crbug.com/376567).
exec < /dev/null
exec > >(exec cat)
exec 2> >(exec cat >&2)

exec /usr/bin/bwrap $BWRAP_ARGS "$HERE/$CHROMIUM_NAME" "$CHROMIUM_FLAGS" "$@"
