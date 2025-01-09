#!/bin/bash

find . -type f \( -iname "*.grd" -o -iname "*.grdp" -o -iname "*.xtb" \) \
    ! -path "*ash_strings*" \
    ! -path "*android*" \
    ! -path "*chromeos_strings*" \
    ! -path "*ios/chrome*" \
    ! -path "*tools/grit/*" \
    ! -path "*device/fido/*" \
    ! -path "*chromeos/*" \
    ! -path "*remoting_strings*" \
    -exec sed -i \
        -e 's/\bph>Chromium<ph\b/REMOVE_PLACEHOLDER_CHROMIUM_PROJECT_TAG/g' \
        -e 's/\bGoogle Chrome\b/REMOVE_PLACEHOLDER_GOOGLE_CHROME/g' \
        -e 's/\bThe Chromium Authors\b/REMOVE_PLACEHOLDER_THE_CHROMIUM_AUTHORS/g' \
        -e 's/\bChrom\(e\|ium\)\b/Trivalent/g' \
        -e 's/REMOVE_PLACEHOLDER_GOOGLE_CHROME/Google Chrome/g' \
        -e 's/REMOVE_PLACEHOLDER_THE_CHROMIUM_AUTHORS/The Chromium Authors/g' \
        -e 's/REMOVE_PLACEHOLDER_CHROMIUM_PROJECT_TAG/ph>Chromium<ph/g' {} + 