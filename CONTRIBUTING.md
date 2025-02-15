<!-- omit in toc -->
# Contributing to Trivalent

First off, thanks for taking the time to contribute! ❤️

> If you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Building locally](#your-first-code-contribution)
  - [Pull Requests](#💫-pull-requests)


## Code of Conduct

This project and everyone participating in it is governed by the
[Code of Conduct](https://github.com/secureblue/trivalent/blob/master/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to <secureblueadmin@proton.me>.


## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation]().

Before you ask a question, it is best to search for existing [Issues](https://github.com/secureblue/trivalent/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/secureblue/trivalent/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (nodejs, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.

### Building locally

> [!NOTE]
> These steps can also be done in a distrobox (or any other container software) if preferred

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
### Pull Requests

#### Before Submitting a Pull Request

A good pull request should be ready for review before it is even created. For all pull requests, ensure:

- Your changes passes all checks
- Your commits are signed
- You have no unnecessary changes, including whitespace changes
- For substantive changes, you include evidence of proper functionality in the pull request in addition to the build results.
