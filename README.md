<p align="center">
  <a href="https://github.com/secureblue/Trivalent">
    <img src="https://github.com/secureblue/Trivalent/blob/live/trivalent.png" href="https://github.com/secureblue/Trivalent" width=180 />
  </a>
</p>

<h1 align="center">Trivalent</h1>

[![Trivalent](https://img.shields.io/badge/dynamic/json?color=blue&label=hardened-chromium&query=builds.latest.source_package.version&url=https%3A%2F%2Fcopr.fedorainfracloud.org%2Fapi_3%2Fpackage%3Fownername%3Dsecureblue%26projectname%3Dhardened-chromium%26packagename%3Dhardened-chromium%26with_latest_build%3DTrue)](https://copr.fedorainfracloud.org/coprs/secureblue/hardened-chromium/)

A hardened chromium for desktop Linux inspired by [Vanadium](https://github.com/GrapheneOS/Vanadium), using [Fedora's Chromium](https://src.fedoraproject.org/rpms/chromium) as a base. Intended for use with [hardened_malloc](https://github.com/GrapheneOS/hardened_malloc) as packaged and provided by [secureblue](https://github.com/secureblue/secureblue).

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

Official support is only provided via [secureblue](https://github.com/secureblue/secureblue/). Unsupported installation is also possible [via COPR](https://copr.fedorainfracloud.org/coprs/secureblue/hardened-chromium/).

## Post-install

Some additional preferences are added to `chrome://settings/security`, these provide additional security and privacy controls should they be needed. There is also a Website Dark Mode preference added to `chrome://settings/appearance`.
\
\
Additionally, the following flags are available that provide extra hardening but may cause breakage or usability issues:

- `chrome://flags/#show-punycode-domains`
- `chrome://flags/#clear-cross-origin-referrers`

Other flags are also provided for compatibility should you experience an issue related to some of the hardening enabled by default. For example, if you experience cookies being cleared on each run of chromium, disable `chrome://flags/#network-service-sandbox`.

## Contributing

Follow the [contributing documentation](CONTRIBUTING.md), and make sure to respect the [CoC](CODE_OF_CONDUCT.md).
