<p align="center">
  <a href="https://github.com/secureblue/Trivalent">
    <img src="https://github.com/secureblue/Trivalent/blob/live/trivalent.png" alt="Trivalent logo" href="https://github.com/secureblue/Trivalent" width=180 />
  </a>
</p>

<h1 align="center">Trivalent</h1>

[![build-x86_64](https://github.com/secureblue/Trivalent/actions/workflows/build_x86_64.yml/badge.svg)](https://github.com/secureblue/Trivalent/actions/workflows/build_x86_64.yml)
[![build-aarch64](https://github.com/secureblue/Trivalent/actions/workflows/build_aarch64.yml/badge.svg)](https://github.com/secureblue/Trivalent/actions/workflows/build_aarch64.yml)
[![Runners by - runs-on.com](https://img.shields.io/badge/Runners-runs--on.com-blue?style=flat)](https://runs-on.com/)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/secureblue/Trivalent/badge)](https://scorecard.dev/viewer/?uri=github.com/secureblue/Trivalent)
[![Discord](https://img.shields.io/discord/1202086019298500629?style=flat&logo=discord&logoColor=white&label=Discord&labelColor=%235F6AE9&color=%2333CB56)](https://discord.com/invite/qMTv5cKfbF)

A security-focused, Chromium-based browser for desktop Linux inspired by [Vanadium](https://github.com/GrapheneOS/Vanadium). Intended for use in [secureblue](https://github.com/secureblue/secureblue).

## Scope

### In scope

* Desktop-relevant patches from Vanadium (located in vanadium_patches)
* Changes that increase hardening against known and unknown vulnerabilities
* Changes that make secondary browser features opt-in instead of opt-out (for example, making the password manager and search suggestions opt-in)
* Changes that disable opt-in metrics and data collection, so long as they have no security implications

### Out of scope

* Any changes that sacrifice security for "privacy" (for example, enabling MV2) <sup>[why?](https://developer.chrome.com/docs/extensions/develop/migrate/improve-security)</sup>
* Any novel functionality that is unrelated to security

## Installation

Official support is only provided via [secureblue](https://github.com/secureblue/secureblue/). Unsupported installation is also possible [via our repo](https://repo.secureblue.dev/secureblue.repo). In addition to being unsupported, use of Trivalent outside of secureblue lacks [SELinux confinement](https://github.com/secureblue/secureblue/tree/live/files/scripts/selinux/trivalent).

## Post-install

Some additional preferences are added to `chrome://settings/security`, these provide additional security and privacy controls should they be needed. An example of one toggle is the `Network Service Sandbox`, which is known to occasionally clear cookies on exit, disabling the sandbox may help.
\
There is also a Website Dark Mode preference added to `chrome://settings/appearance`.
\
\
Additionally, the following flags are available that provide extra hardening but may cause breakage or usability issues:

* `chrome://flags/#show-punycode-domains`
* `chrome://flags/#clear-cross-origin-referrers`

Other flags are also provided for compatibility should you experience an issue related to some of the hardening enabled by default. For example, the default pop-up blocker is very strict, it may optionally be disabled `chrome://flags/#strict-popup-blocking` to improve usability.

## Content Blocking

Trivalent comes by default with content filtering enabled using chromium's internal subresource filter. The lists used for content filtering can be found [here](https://github.com/secureblue/trivalent-subresource-filter/blob/live/copr_script.sh#L19).
\
If you want to contribute to the subresource filter, example suggesting a new list, visit [here](https://github.com/secureblue/trivalent-subresource-filter).

## Contributing

Follow the [contributing documentation](CONTRIBUTING.md), and make sure to respect the [CoC](CODE_OF_CONDUCT.md).
