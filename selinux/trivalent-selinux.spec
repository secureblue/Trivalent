%global chromium_name trivalent
%global chromium_name_branding Trivalent
%global chromium_path %{_libdir}/%{chromium_name}

%global source_repo_name Trivalent
%global source_repo https://github.com/secureblue/%{source_repo_name}
%global source_repo_branch live

%global with_selinux 1
%global modulename %{chromium_name}
%global selinuxtype targeted

Name:           %{chromium_name}-selinux
Epoch:          1
Version:        1.0.0
Release:        1
Summary:        SELinux policies for %{chromium_name_branding}
License:        Apache-2.0 OR MIT
URL:            %{source_repo}
Source:         %{source_repo}/archive/refs/heads/%{source_repo_branch}.tar.gz

BuildRequires:  container-selinux
BuildRequires:  make
BuildRequires:  selinux-policy-devel

Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
Recommends:     %{chromium_name}
Recommends:     container-selinux
BuildArch:      noarch
%{?selinux_requires_min}

%description
SELinux policy module for %{chromium_name_branding}.

%prep
%setup -q -n %{source_repo_name}-%{source_repo_branch}

%build
make -f %{_datadir}/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 %{modulename}.pp

%install
install -Dp -m 0644 -t %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype} %{modulename}.pp.bz2
install -Dp -m 0644 -t %{buildroot}%{_datadir}/selinux/devel/include/distributed selinux/%{modulename}.if

%pre
%selinux_relabel_pre -s %{selinuxtype}

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%postun
if [ "$1" -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
    %selinux_relabel_post -s %{selinuxtype}
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}
%{_sbindir}/restorecon -Ri %{chromium_path}

%files
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%{_datadir}/selinux/devel/include/distributed/%{modulename}.if
%ghost %verify(not md5 size mode mtime) %{_selinux_store_path}/%{selinuxtype}/active/modules/200/%{modulename}

%changelog
* Mon Aug 31 2026 secureblue <noreply@secureblue.dev> - 1:1.0.0-1
- Split off trivalent-selinux into separate RPM spec
- Set epoch to 1 and reset version scheme
