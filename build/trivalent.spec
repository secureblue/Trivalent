%define _lto_cflags %{nil}
%global _default_patch_fuzz 2
%global numjobs %{_smp_build_ncpus}

%global chromebuilddir out/Release
%global debug_package %{nil}
%global debug_level 0
%global chromium_name trivalent
%global chromium_name_branding Trivalent
%global chromium_path %{_libdir}/%{chromium_name}

# To generate this list, go into %%{buildroot}%%{chromium_path} and run
# for i in `find . -name "*.so" | sort`; do NAME=`basename -s .so $i`; printf "$NAME|"; done
%global __provides_exclude_from ^(%{chromium_path}/.*\\.so|%{chromium_path}/.*\\.so.*)$
%global __requires_exclude ^(%{chromium_path}/.*\\.so|%{chromium_path}/.*\\.so.*)$

### Build configuration ###
# This allows for hardware accelerated video and WebDRM (for things like Netflix)
%global enable_proprietary_codecs 1

Source69: chromium-version.txt

Name:	%{chromium_name}
%{lua:
       local f = io.open(macros['_sourcedir']..'/chromium-version.txt', 'r')
       local content = f:read "*all"
       -- This will dynamically set the version based on chromium's latest stable release channel
       print("Version: "..content.."\n")

       -- This will automatically increment the release every ~1 hour
       print("Release: "..(os.time() // 4000).."\n")
}
Summary: A security-focused browser built upon Google's Chromium web browser
Url: https://github.com/secureblue/Trivalent
License: (GPL-2.0-only WITH (Apache-2.0-note AND FTL-note AND WebView-note)) AND BSD-3-Clause AND BSD-2-Clause AND dtoa AND SunPro AND Zlib AND Libpng AND libtiff AND FTL AND LGPL-2.1 AND LGPL-2.1-or-later AND LGPL-3.0-or-later AND Apache-2.0 AND IJG AND MIT AND GPL-2.0-or-later AND ISC AND OpenSSL AND (MPL-1.1 OR GPL-2.0-only OR LGPL-2.0-only)
# Replace the old package
Obsoletes: hardened-chromium

Source0: chromium-%{version}-clean.tar.xz
Source2: %{chromium_name}.conf
Source3: %{chromium_name}.sh
Source4: %{chromium_name}.desktop
Source9: %{chromium_name}.xml
Source10: %{chromium_name}.appdata.xml
Source11: master_preferences
Source12: %{chromium_name}16.png
Source13: %{chromium_name}22.png
Source14: %{chromium_name}32.png
Source15: %{chromium_name}44.png
Source16: %{chromium_name}64.png

Source17: %{chromium_name}24.png
Source18: %{chromium_name}48.png
Source19: %{chromium_name}128.png
Source20: %{chromium_name}256.png

### Patches ###
%{lua:
    rpm.execute("pwd")
    if posix.getenv("HOME") == "/builddir" then
        fpatches = rpm.glob('/builddir/build/SOURCES/fedora-*.patch')
        vpatches = rpm.glob('/builddir/build/SOURCES/vanadium-*.patch')
        hpatches = rpm.glob('/builddir/build/SOURCES/'..macros['chromium_name']..'-*.patch')
    else
        fpatches = rpm.glob(macros['_sourcedir']..'/fedora-*.patch')
        vpatches = rpm.glob(macros['_sourcedir']..'/vanadium-*.patch')
        hpatches = rpm.glob(macros['_sourcedir']..'/'..macros['chromium_name']..'-*.patch')
    end

    local count = 1000
    local printPatch = ""
    for p in ipairs(fpatches) do
        os.execute("echo 'Patching in "..fpatches[p].."'")
        printPatch = "Patch"..count..": fedora-"..count..".patch"
        rpm.execute("echo", printPatch)
        print(printPatch.."\n")
        count = count + 1
    end
    rpm.define("_fedoraPatchCount "..count-1)

    count = 2000
    printPatch = ""
    for p in ipairs(vpatches) do
        os.execute("echo 'Patching in "..vpatches[p].."'")
        printPatch = "Patch"..count..": vanadium-"..count..".patch"
        rpm.execute("echo", printPatch)
        print(printPatch.."\n")
        count = count + 1
    end
    rpm.define("_vanadiumPatchCount "..count-1)

    count = 3000
    printPatch = ""
    for p in ipairs(hpatches) do
        os.execute("echo 'Patching in "..hpatches[p].."'")
        printPatch = "Patch"..count..": "..macros['chromium_name'].."-"..count..".patch"
        rpm.execute("echo", printPatch)
        print(printPatch.."\n")
        count = count + 1
    end
    rpm.define("_hardeningPatchCount "..count-1)

    os.execute("echo 'Autopatch F: "..macros['_fedoraPatchCount'].."'")
    os.execute("echo 'Autopatch V: "..macros['_vanadiumPatchCount'].."'")
    os.execute("echo 'Autopatch H: "..macros['_hardeningPatchCount'].."'")
}

BuildRequires: golang-github-evanw-esbuild
BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	glib2-devel
BuildRequires:	glibc-devel
BuildRequires:	gperf
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt6Core)
BuildRequires: pkgconfig(Qt6Widgets)
BuildRequires: libatomic
BuildRequires:	libcap-devel
BuildRequires:	libcurl-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libudev-devel
BuildRequires:	libuuid-devel
BuildRequires:	libusb-compat-0.1-devel
BuildRequires:	libutempter-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXtst-devel
BuildRequires:	xcb-proto
BuildRequires:	mesa-libgbm-devel
BuildRequires:	nss-devel >= 3.26
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	pipewire-devel
BuildRequires: libappstream-glib

BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
# For eu-strip
BuildRequires:	elfutils
BuildRequires:	elfutils-libelf-devel
BuildRequires:	hwdata
BuildRequires:	kernel-headers
BuildRequires:	libffi-devel
BuildRequires:	libudev-devel
BuildRequires:	libva-devel
BuildRequires:	libxshmfence-devel
BuildRequires:	mesa-libGL-devel
BuildRequires: %{__python3}
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires: python3-jinja2
BuildRequires: yasm
BuildRequires: zlib-devel
BuildRequires:	systemd
BuildRequires: libevdev-devel
# One of the python scripts invokes git to look for a hash. So helpful.
BuildRequires:	git-core

Requires: nss%{_isa} >= 3.26
Requires: nss-mdns%{_isa}
Requires: libcanberra-gtk3%{_isa}
Requires: u2f-hidraw-policy
Requires: bubblewrap

ExclusiveArch: x86_64 aarch64

# License: BSD-3-Clause
Provides: bundled(angle)
# License: MIT
Provides: bundled(bintrees)
# License: Apache-2.0
Provides: bundled(boringssl)
# License: MIT
Provides: bundled(brotli)
# License: BSD-2-Clause
Provides: bundled(bspatch)
# License: Apache-2.0
Provides: bundled(cacheinvalidation)
# License: BSD-3-Clause
Provides: bundled(colorama)
# License: Apache-2.0
Provides: bundled(crashpad)
# License: BSD-3-Clause
Provides: bundled(crc32c)
# License: BSD-2-Clause
Provides: bundled(dav1d)
# License: BSD-3-Clause
Provides: bundled(double-conversion)
# License: dtoa
Provides: bundled(dmg_fp)
# License: MIT
Provides: bundled(expat)
# License: SunPro
Provides: bundled(fdmlibm)
# License: LGPL-2.1-or-later
Provides: bundled(ffmpeg)
# License: BSD-3-Clause
Provides: bundled(flac)
# License: BSD-3-Clause
Provides: bundled(fips181)
# License: MIT
Provides: bundled(fontconfig)
# License: FTL
Provides: bundled(freetype)
# License: BSD-3-Clause
Provides: bundled(gperftools)
# License: MIT
Provides: bundled(harfbuzz-ng)
# License: Apache-2.0
Provides: bundled(highway)
# License: MPL-1.1 OR GPL-2.0-only OR LGPL-2.0-only
Provides: bundled(hunspell)
# License: IJG
Provides: bundled(iccjpeg)
# License: Unicode-3.0
Provides: bundled(icu)
# License: MIT
Provides: bundled(lcms2)
# License: BSD-3-Clause
Provides: bundled(leveldb)
# License: Apache-2.0
Provides: bundled(libaddressinput)
# License: BSD-2-Clause
Provides: bundled(libaom)
# License: MIT
Provides: bundled(libdrm)
# License: BSD-3-Clause
Provides: bundled(libevent)
# License: BSD-3-Clause
Provides: bundled(libjingle)
# License: Zlib AND IJG and BSD-3-Clause
Provides: bundled(libjpeg)
# License: BSD-2-Clause
Provides: bundled(libopenjpeg2)
# License: Apache-2.0
Provides: bundled(libphonenumber)
# License: Libpng
Provides: bundled(libpng)
# License: LGPL-2.1
Provides: bundled(libsecret)
# License: BSD-3-Clause
Provides: bundled(libsrtp)
# License: libtiff
Provides: bundled(libtiff)
# License: BSD-2-Clause
Provides: bundled(libudis86)
# License: LGPL-2.1
Provides: bundled(libusbx)
# License: BSD-3-Clause
Provides: bundled(libvpx)
# License: BSD-3-Clause
Provides: bundled(libwebp)
# License: BSD-3-Clause
Provides: bundled(libyuv)
# License: MIT
Provides: bundled(libxml)
# License: MIT
Provides: bundled(libxslt)
# Public Domain
Provides: bundled(lzma)
# License: MIT
Provides: bundled(mesa)
# License: BSD-3-Clause
Provides: bundled(mozc)
# License: BSD-2-Clause
Provides: bundled(openh264)
# License: BSD-3-Clause
Provides: bundled(opus)
# License: BSD-3-Clause
Provides: bundled(ots)
# License: BSD-3-Clause
Provides: bundled(protobuf)
# License: MIT
Provides: bundled(qcms)
# License: BSD-3-Clause
Provides: bundled(re2)
# License: Apache-2.0
Provides: bundled(sfntly)
# License: BSD-3-Clause
Provides: bundled(skia)
# License: MIT
Provides: bundled(SMHasher)
# License: BSD-3-Clause
Provides: bundled(snappy)
# License: LGPL-2.1
Provides: bundled(speech-dispatcher)
# Public domain
Provides: bundled(sqlite)
# License: MIT
Provides: bundled(superfasthash)
# License: LGPL-3.0-or-later
Provides: bundled(talloc)
# License: BSD-3-Clause
Provides: bundled(usrsctp)
# License: BSD-3-Clause
Provides: bundled(v8)
# License: BSD-3-Clause
Provides: bundled(webrtc)
# License: MIT
Provides: bundled(woff2)
# License: MIT
Provides: bundled(xdg-mime)
# License: MIT
Provides: bundled(xdg-user-dirs)
# License: Zlib
Provides: bundled(zlib)
# License: BSD-3-Clause
Provides: bundled(zstd)

# For selinux scriptlet
Requires(post): /usr/sbin/semanage
Requires(post): /usr/sbin/restorecon

%description
%{chromium_name_branding} is a security-focused browser built upon the Chromium web browser.

%package qt6-ui
Summary: Qt6 UI built from %{chromium_name_branding}
Requires: %{chromium_name}%{_isa} = %{version}-%{release}

%description qt6-ui
Qt6 UI for %{chromium_name_branding}.

%prep
%setup -q -n chromium-%{version}

### Patches ###
%autopatch -p1 -m 1000 -M %{_fedoraPatchCount}
%autopatch -p1 -m 2000 -M %{_vanadiumPatchCount}
%autopatch -p1 -m 3000 -M %{_hardeningPatchCount}

### String Branding ###
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
        -e 's/\Chrome Web Store\b/REMOVE_PLACEHOLDER_CHROME_WEB_STORE/g' \
        -e 's/\bThe Chromium Authors\b/REMOVE_PLACEHOLDER_THE_CHROMIUM_AUTHORS/g' \
        -e 's/\bChrom\(e\|ium\)\b/%{chromium_name_branding}/g' \
        -e 's/REMOVE_PLACEHOLDER_GOOGLE_CHROME/Google Chrome/g' \
        -e 's/REMOVE_PLACEHOLDER_CHROME_WEB_STORE/Chrome Web Store/g' \
        -e 's/REMOVE_PLACEHOLDER_THE_CHROMIUM_AUTHORS/The Chromium Authors/g' \
        -e 's/REMOVE_PLACEHOLDER_CHROMIUM_PROJECT_TAG/ph>Chromium<ph/g' {} + 

### Branding ###
cp -a %{SOURCE12} chrome/app/theme/default_100_percent/chromium/linux/product_logo_16.png
cp -a %{SOURCE14} chrome/app/theme/default_100_percent/chromium/linux/product_logo_32.png
cp -a %{SOURCE12} chrome/app/theme/default_100_percent/chromium/product_logo_16.png
cp -a %{SOURCE14} chrome/app/theme/default_100_percent/chromium/product_logo_32.png
cp -a %{SOURCE13} chrome/app/theme/default_100_percent/chromium/product_logo_name_22.png
cp -a %{SOURCE13} chrome/app/theme/default_100_percent/chromium/product_logo_name_22_white.png

cp -a %{SOURCE14} chrome/app/theme/default_200_percent/chromium/product_logo_16.png
cp -a %{SOURCE16} chrome/app/theme/default_200_percent/chromium/product_logo_32.png
cp -a %{SOURCE15} chrome/app/theme/default_200_percent/chromium/product_logo_name_22.png
cp -a %{SOURCE15} chrome/app/theme/default_200_percent/chromium/product_logo_name_22_white.png

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
find -type f \( -iname "*.py" \) -exec sed -i '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +

# Get rid of the pre-built eu-strip binary, it is x86_64 and of mysterious origin
rm -rf buildtools/third_party/eu-strip/bin/eu-strip

# Replace it with a symlink to the Fedora copy
ln -s %{_bindir}/eu-strip buildtools/third_party/eu-strip/bin/eu-strip

# Hard code extra version
sed -i 's/getenv("CHROME_VERSION_EXTRA")/"%{chromium_name}"/' chrome/common/channel_info_posix.cc

%build
# reduce warnings
FLAGS=' -Wno-deprecated-declarations -Wno-unknown-warning-option -Wno-unused-command-line-argument'
FLAGS+=' -Wno-unused-but-set-variable -Wno-unused-result -Wno-unused-function -Wno-unused-variable'
FLAGS+=' -Wno-unused-const-variable -Wno-unneeded-internal-declaration -Wno-unknown-attributes -Wno-unknown-pragmas'

CFLAGS="$FLAGS"
CXXFLAGS="$FLAGS"

# reduce the size of relocations
LDFLAGS="$LDFLAGS -Wl,-z,pack-relative-relocs"
RUSTFLAGS=${RUSTFLAGS/--cap-lints/-Clink-arg=-Wl,-z,pack-relative-relocs --cap-lints}
RUSTFLAGS=${RUSTFLAGS/debuginfo=?/debuginfo=0}

export CC=clang
export CXX=clang++
export AR=llvm-ar
export NM=llvm-nm
export READELF=llvm-readelf
export CFLAGS
export CXXFLAGS
export LDFLAGS
export RUSTFLAGS

export RUSTC_BOOTSTRAP=1

declare -r SOURCE_DIR="$(pwd)/third_party"

# add internal clang to PATH for build
PATH="$PATH:$SOURCE_DIR/llvm-build/Release+Asserts/bin"

# add internal rust utils to PATH for build
PATH="$PATH:$SOURCE_DIR/rust-toolchain/bin"

# add internal nodejs to PATH for build
PATH="$PATH:$SOURCE_DIR/node/linux/node-linux-x64/bin"

export PATH

CHROMIUM_GN_DEFINES=''
%ifarch aarch64
CHROMIUM_GN_DEFINES+=' target_cpu="arm64"'
CHROMIUM_GN_DEFINES+=' use_v4l2_codec=true'
%endif
%if %{enable_proprietary_codecs}
CHROMIUM_GN_DEFINES+=' ffmpeg_branding="Chrome" proprietary_codecs=true enable_widevine=true'
%endif
CHROMIUM_GN_DEFINES+=' system_libdir="%{_lib}"'
CHROMIUM_GN_DEFINES+=' is_official_build=true'
CHROMIUM_GN_DEFINES+=' is_cfi=true use_cfi_cast=true'
CHROMIUM_GN_DEFINES+=' enable_reporting=false'
CHROMIUM_GN_DEFINES+=' enable_remoting=false'
CHROMIUM_GN_DEFINES+=' is_clang=true'
CHROMIUM_GN_DEFINES+=' use_sysroot=false'
CHROMIUM_GN_DEFINES+=' target_os="linux"'
CHROMIUM_GN_DEFINES+=' current_os="linux"'
CHROMIUM_GN_DEFINES+=' treat_warnings_as_errors=false'
CHROMIUM_GN_DEFINES+=' enable_vr=false'
CHROMIUM_GN_DEFINES+=' enable_openxr=false'
CHROMIUM_GN_DEFINES+=' enable_swiftshader=false' # build without swiftshader (it is actively being deprecated anyway)
CHROMIUM_GN_DEFINES+=' build_dawn_tests=false enable_perfetto_unittests=false'
CHROMIUM_GN_DEFINES+=' disable_fieldtrial_testing_config=true'
CHROMIUM_GN_DEFINES+=' symbol_level=%{debug_level} blink_symbol_level=%{debug_level}'
CHROMIUM_GN_DEFINES+=' angle_has_histograms=false'
CHROMIUM_GN_DEFINES+=' safe_browsing_use_unrar=false'
CHROMIUM_GN_DEFINES+=' use_kerberos=true'
CHROMIUM_GN_DEFINES+=' use_qt6=true moc_qt6_path="%{_libdir}/qt6/libexec/"'
CHROMIUM_GN_DEFINES+=' use_pulseaudio=true'
CHROMIUM_GN_DEFINES+=' rtc_use_pipewire=true rtc_link_pipewire=true'
CHROMIUM_GN_DEFINES+=' use_system_libffi=true' # ld.lld: error: unable to find library -lffi_pic
CHROMIUM_GN_DEFINES+=' v8_enable_drumbrake=false' # flip to true once it actually works
export CHROMIUM_GN_DEFINES

# Check that there is no system 'google' module, shadowing bundled ones:
if python3 -c 'import google ; print google.__path__' 2> /dev/null ; then \
    echo "Python 3 'google' module is defined, this will shadow modules of this build"; \
    exit 1 ; \
fi

mkdir -p %{chromebuilddir} && cp -a buildtools/linux64/gn %{chromebuilddir}/

%{chromebuilddir}/gn --script-executable=%{__python3} gen --args="$CHROMIUM_GN_DEFINES" %{chromebuilddir}

%{__python3} $SOURCE_DIR/depot_tools/autoninja.py %{chromebuilddir} chrome

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{chromium_path}/locales \
         %{buildroot}%{_sysconfdir}/%{chromium_name}

# install system wide chromium config
cp -a %{SOURCE2} %{buildroot}%{_sysconfdir}/%{chromium_name}/%{chromium_name}.conf
cp -a %{SOURCE3} %{buildroot}%{chromium_path}/%{chromium_name}.sh

export BUILD_TARGET=`cat /etc/redhat-release`
export CHROMIUM_PATH=%{chromium_path}
export CHROMIUM_NAME=%{chromium_name}

sed -i "s|@@BUILD_TARGET@@|$BUILD_TARGET|g" %{buildroot}%{chromium_path}/%{chromium_name}.sh
sed -i "s|@@CHROMIUM_PATH@@|$CHROMIUM_PATH|g" %{buildroot}%{chromium_path}/%{chromium_name}.sh
sed -i "s|@@CHROMIUM_NAME@@|$CHROMIUM_NAME|g" %{buildroot}%{chromium_path}/%{chromium_name}.sh

ln -s ../..%{chromium_path}/%{chromium_name}.sh %{buildroot}%{_bindir}/%{chromium_name}
mkdir -p %{buildroot}%{_mandir}/man1/

pushd %{chromebuilddir}
	cp -a icudtl.dat %{buildroot}%{chromium_path}
	cp -a chrom*.pak resources.pak %{buildroot}%{chromium_path}
	cp -a locales/*.pak %{buildroot}%{chromium_path}/locales/
  cp -a libvulkan.so.1 %{buildroot}%{chromium_path}
	cp -a chrome %{buildroot}%{chromium_path}/%{chromium_name}
	cp -a chrome_crashpad_handler %{buildroot}%{chromium_path}/chrome_crashpad_handler
	cp -a ../../chrome/app/resources/manpage.1.in %{buildroot}%{_mandir}/man1/%{chromium_name}.1
	sed -i "s|@@PACKAGE@@|%{chromium_name}|g" %{buildroot}%{_mandir}/man1/%{chromium_name}.1
	sed -i "s|@@MENUNAME@@|%{chromium_name}|g" %{buildroot}%{_mandir}/man1/%{chromium_name}.1

	# V8 initial snapshots
	# https://code.google.com/p/chromium/issues/detail?id=421063
	cp -a v8_context_snapshot.bin %{buildroot}%{chromium_path}

	# This is ANGLE, not to be confused with the similarly named files under swiftshader/
	cp -a libEGL.so libGLESv2.so %{buildroot}%{chromium_path}
  cp -a libqt6_shim.so %{buildroot}%{chromium_path}
popd

pushd %{buildroot}%{chromium_path}/
for f in *.so *.so.1 chrome_crashpad_handler %{chromium_name} headless_shell chromedriver ; do
   [ -f $f ] && strip $f
done
popd

# Add directories for policy management
mkdir -p %{buildroot}%{_sysconfdir}/%{chromium_name}/policies/managed
mkdir -p %{buildroot}%{_sysconfdir}/%{chromium_name}/policies/recommended

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp -a %{SOURCE20} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{chromium_name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
cp -a %{SOURCE19} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{chromium_name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
cp -a %{SOURCE16} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{chromium_name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
cp -a %{SOURCE18} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{chromium_name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
cp -a %{SOURCE17} %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{chromium_name}.png

# Install the master_preferences file
install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/%{chromium_name}/

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE4}

install -D -m0644 %{SOURCE10} ${RPM_BUILD_ROOT}%{_datadir}/metainfo/%{chromium_name}.appdata.xml
appstream-util validate-relax --nonet ${RPM_BUILD_ROOT}%{_datadir}/metainfo/%{chromium_name}.appdata.xml

mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps/
cp -a %{SOURCE9} %{buildroot}%{_datadir}/gnome-control-center/default-apps/

%post
# Set SELinux labels - semanage itself will adjust the lib directory naming
# But only do it when selinux is enabled, otherwise, it gets noisy.
if selinuxenabled; then
	semanage fcontext -a -t bin_t /usr/lib/%{chromium_name} &>/dev/null || :
	semanage fcontext -a -t bin_t /usr/lib/%{chromium_name}/%{chromium_name}.sh &>/dev/null || :
	restorecon -R -v %{chromium_path}/%{chromium_name} &>/dev/null || :
fi

%files qt6-ui
%{chromium_path}/libqt6_shim.so

%files
%doc AUTHORS
%license LICENSE
%{_mandir}/man1/%{chromium_name}.*
# Binary and Libs
%{_bindir}/%{chromium_name}
%dir %{chromium_path}/
%{chromium_path}/%{chromium_name}
%{chromium_path}/%{chromium_name}.sh
%{chromium_path}/chrome_crashpad_handler
%{chromium_path}/icudtl.dat
%{chromium_path}/v8_context_snapshot.bin
%{chromium_path}/libvulkan.so.1
%{chromium_path}/libEGL.so
%{chromium_path}/libGLESv2.so
# Config
%config(noreplace) %{_sysconfdir}/%{chromium_name}/%{chromium_name}.conf
%config %{_sysconfdir}/%{chromium_name}/master_preferences
%config %{_sysconfdir}/%{chromium_name}/policies/
# System entries
%{_datadir}/applications/%{chromium_name}.desktop
%{_datadir}/metainfo/%{chromium_name}.appdata.xml
%{_datadir}/gnome-control-center/default-apps/%{chromium_name}.xml
%{_datadir}/icons/hicolor/256x256/apps/%{chromium_name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{chromium_name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{chromium_name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{chromium_name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{chromium_name}.png
# Locale and Language
%{chromium_path}/resources.pak
%{chromium_path}/chrome_100_percent.pak
%{chromium_path}/chrome_200_percent.pak
%dir %{chromium_path}/locales/
# Chromium _ALWAYS_ needs en-US.pak as a fallback
%{chromium_path}/locales/en-US.pak
%lang(af) %{chromium_path}/locales/af.pak
%lang(am) %{chromium_path}/locales/am.pak
%lang(ar) %{chromium_path}/locales/ar.pak
%lang(bg) %{chromium_path}/locales/bg.pak
%lang(bn) %{chromium_path}/locales/bn.pak
%lang(ca) %{chromium_path}/locales/ca.pak
%lang(cs) %{chromium_path}/locales/cs.pak
%lang(da) %{chromium_path}/locales/da.pak
%lang(de) %{chromium_path}/locales/de.pak
%lang(el) %{chromium_path}/locales/el.pak
%lang(en_GB) %{chromium_path}/locales/en-GB.pak
%lang(es) %{chromium_path}/locales/es.pak
%lang(es) %{chromium_path}/locales/es-419.pak
%lang(et) %{chromium_path}/locales/et.pak
%lang(fa) %{chromium_path}/locales/fa.pak
%lang(fi) %{chromium_path}/locales/fi.pak
%lang(fil) %{chromium_path}/locales/fil.pak
%lang(fr) %{chromium_path}/locales/fr.pak
%lang(gu) %{chromium_path}/locales/gu.pak
%lang(he) %{chromium_path}/locales/he.pak
%lang(hi) %{chromium_path}/locales/hi.pak
%lang(hr) %{chromium_path}/locales/hr.pak
%lang(hu) %{chromium_path}/locales/hu.pak
%lang(id) %{chromium_path}/locales/id.pak
%lang(it) %{chromium_path}/locales/it.pak
%lang(ja) %{chromium_path}/locales/ja.pak
%lang(kn) %{chromium_path}/locales/kn.pak
%lang(ko) %{chromium_path}/locales/ko.pak
%lang(lt) %{chromium_path}/locales/lt.pak
%lang(lv) %{chromium_path}/locales/lv.pak
%lang(ml) %{chromium_path}/locales/ml.pak
%lang(mr) %{chromium_path}/locales/mr.pak
%lang(ms) %{chromium_path}/locales/ms.pak
%lang(nb) %{chromium_path}/locales/nb.pak
%lang(nl) %{chromium_path}/locales/nl.pak
%lang(pl) %{chromium_path}/locales/pl.pak
%lang(pt_BR) %{chromium_path}/locales/pt-BR.pak
%lang(pt_PT) %{chromium_path}/locales/pt-PT.pak
%lang(ro) %{chromium_path}/locales/ro.pak
%lang(ru) %{chromium_path}/locales/ru.pak
%lang(sk) %{chromium_path}/locales/sk.pak
%lang(sl) %{chromium_path}/locales/sl.pak
%lang(sr) %{chromium_path}/locales/sr.pak
%lang(sv) %{chromium_path}/locales/sv.pak
%lang(sw) %{chromium_path}/locales/sw.pak
%lang(ta) %{chromium_path}/locales/ta.pak
%lang(te) %{chromium_path}/locales/te.pak
%lang(th) %{chromium_path}/locales/th.pak
%lang(tr) %{chromium_path}/locales/tr.pak
%lang(uk) %{chromium_path}/locales/uk.pak
%lang(ur) %{chromium_path}/locales/ur.pak
%lang(vi) %{chromium_path}/locales/vi.pak
%lang(zh_CN) %{chromium_path}/locales/zh-CN.pak
%lang(zh_TW) %{chromium_path}/locales/zh-TW.pak
