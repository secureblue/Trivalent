<!-- omit in toc -->

# Contributing to Trivalent

<!-- omit in toc -->

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Building locally](#building-locally)
  - [Pull Requests](#pull-requests)

## Code of Conduct

This project and everyone participating in it is governed by the
[Code of Conduct](./CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to <secureblueadmin@proton.me>.

## I Have a Question

Before you ask a question, it is best to search for existing [Issues](https://github.com/secureblue/Trivalent/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/secureblue/Trivalent/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (Node.js, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## I Want To Contribute

<!-- markdownlint-disable MD022 -->

> ### Legal Notice <!-- omit in toc -->
>
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.

### Building locally

> [!NOTE]
> These steps can also be done in a distrobox (or any other container software) if preferred. See below for instructions on how to use [systemd-nspawn](#setting-up-a-systemd-nspawn-container) if you're not running Fedora.

#### Setup

Enable the COPR repository (as root):

`dnf copr enable secureblue/trivalent`

Install the `trivalent-chromium-clean-source` package (as root):

`dnf install trivalent-chromium-clean-source`

> This command can take a while especially on a slow network, the package is over 3 gigabytes

Clone the repository:

`git clone https://github.com/secureblue/trivalent.git`

Then run the COPR script:

`/bin/bash ./trivalent/copr_script.sh`

#### Build RPM

Build the patched chromium source from the spec file:

`rpmbuild -bs -v --define "_sourcedir $PWD" --define "_rpmdir $PWD" --define "_builddir $PWD" --define "_specdir $PWD" --define "_srcrpmdir $PWD" trivalent.spec`

Rebuild the source for your system:

`mock --resultdir=dist -r %{distro}-%{version}-%{arch} --rebuild trivalent-%{version}.%{distro}.src.rpm`

Install the built rpm...

#### Setting up a systemd-nspawn container

Start by installing `dnf` on your distro. Make sure to pick `dnf5` if your distro ships it as a separate package than dnf 4.x (e.g. Arch Linux). Configure the Fedora repositories in `/etc/dnf/dnf.conf`.

```
[fedora]
name=Fedora $releasever - $basearch
metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-$releasever&arch=$basearch
gpgkey=https://fedoraproject.org/fedora.gpg
gpgcheck=1

[updates]
name=Fedora $releasever - $basearch - Updates
metalink=https://mirrors.fedoraproject.org/metalink?repo=updates-released-f$releasever&arch=$basearch
gpgkey=https://fedoraproject.org/fedora.gpg
gpgcheck=1
```

Then create a directory (or btrfs subvolume if applicable) in `/var/lib/machines` and bootstrap a Fedora environment inside. You will need to set a password for the root user.

```
# mkdir /var/lib/machines/<container-name>  # If you're on btrfs, you likely will want to use a subvolume instead.
# dnf5 --releasever=45 --setopt=install_weak_deps=False --best --use-host-config --installroot=/var/lib/machines/<container-name> install dbus dhcp-client dnf dnf5-plugins fedora-release glibc glibc-langpack-en iputils less ncurses passwd systemd systemd-networkd systemd-resolved util-linux vim-default-editor rpm rpm-build mock git
# systemd-nspawn -D /var/lib/machines/<container-name> systemctl enable systemd-networkd systemd-resolved
# systemd-nspawn -D /var/lib/machines/<container-name> passwd
```

If you're on a distro that does not use `systemd-networkd`, you'll need to start it on the host to get connectivity inside the container, or manually configure network connectivity. `systemd-networkd` does not touch interfaces unless it is configured to do so; starting it alongside e.g. NetworkManager should not cause any issues on the host and only the virtual ethernet adapter will be managed by `systemd-networkd`.

Once this is done, you can start the container and login via `machinectl`.

```
machinectl start <container-name>
machinectl login <container-name>
```

> [!TIP]
> If you're encountering permission issues when running `mock`, a workaround is to use `mock --isolation=simple` which uses a chroot instead of trying to create a nested `nspawn` setup.

See also:

- [Arch Wiki - systemd-nspawn](https://wiki.archlinux.org/title/Systemd-nspawn)
- [Fedora Server User Documentation - Setting up a systemd-nspawn Fedora container](https://docs.fedoraproject.org/en-US/fedora-server/containerization/systemd-nspawn-setup)
- [systemd-nspawn(1)](https://man.archlinux.org/man/systemd-nspawn.1)

### Pull Requests

#### Before Submitting a Pull Request

A good pull request should be ready for review before it is even created. For all pull requests, ensure:

- Your changes passes all checks
- Your commits are signed
- You have no unnecessary changes, including whitespace changes
- For substantive changes, you include evidence of proper functionality in the pull request in addition to the build results.
