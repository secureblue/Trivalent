%define _lto_cflags %{nil}
%global _default_patch_fuzz 2
%global numjobs %{_smp_build_ncpus}

# Fancy build status
%global build_target() \
	export NINJA_STATUS="[%2:%f/%t] " ; \
	ninja -j %{numjobs} -C '%1' '%2'

%global nodejs_version v20.6.1
%global esbuild_version 0.19.2
%global chromium_pybin %{__python3}
%global chromebuilddir out/Release
%global debug_package %{nil}
%global debug_level 0
%global chromium_name trivalent
%global chromium_path %{_libdir}/%{chromium_name}

# To generate this list, go into %%{buildroot}%%{chromium_path} and run
# for i in `find . -name "*.so" | sort`; do NAME=`basename -s .so $i`; printf "$NAME|"; done
%global __provides_exclude_from ^(%{chromium_path}/.*\\.so|%{chromium_path}/.*\\.so.*)$
%global __requires_exclude ^(%{chromium_path}/.*\\.so|%{chromium_path}/.*\\.so.*)$

Source69: chromium-version.txt

Name:	%{chromium_name}
%{lua:
       local f = io.open(macros['_sourcedir']..'/chromium-version.txt', 'r')
       local content = f:read "*all"
       print("Version: "..content.."\n")
}
Release: 1
Summary: A security-focused browser built upon Google's Chromium web browser
Url: http://www.chromium.org/Home
License: BSD-3-Clause AND LGPL-2.1-or-later AND Apache-2.0 AND IJG AND MIT AND GPL-2.0-or-later AND ISC AND OpenSSL AND (MPL-1.1 OR GPL-2.0-only OR LGPL-2.0-only)

Source0: chromium-%{version}-clean.tar.xz
Source2: %{chromium_name}.conf
Source3: %{chromium_name}.sh
Source4: %{chromium_name}.desktop
Source9: %{chromium_name}.xml
Source11: master_preferences
Source12: %{chromium_name}16.png
Source13: %{chromium_name}22.png
Source14: %{chromium_name}32.png
Source15: %{chromium_name}44.png
Source16: %{chromium_name}64.png

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
BuildRequires: clang
BuildRequires: clang-tools-extra
BuildRequires: llvm
BuildRequires: lld
BuildRequires: rustc
BuildRequires: bindgen-cli
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(openh264)
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
BuildRequires: compiler-rt
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
BuildRequires: nodejs
BuildRequires: gn
BuildRequires:	nss-devel >= 3.26
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	pipewire-devel
BuildRequires: libappstream-glib

# Fedora tries to use system libs whenever it can.
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
# For eu-strip
BuildRequires:	elfutils
BuildRequires:	elfutils-libelf-devel
# One of the python scripts invokes git to look for a hash. So helpful.
BuildRequires:	/usr/bin/git
BuildRequires:	hwdata
BuildRequires:	kernel-headers
BuildRequires:	libffi-devel
BuildRequires:	libudev-devel
BuildRequires:	libva-devel
BuildRequires:	libxshmfence-devel
BuildRequires:	mesa-libGL-devel
BuildRequires: %{chromium_pybin}
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires: python3-jinja2
BuildRequires: yasm
BuildRequires: zlib-devel
BuildRequires:	systemd
BuildRequires: ninja-build
BuildRequires: libevdev-devel

Requires: nss%{_isa} >= 3.26
Requires: nss-mdns%{_isa}
Requires: libcanberra-gtk3%{_isa}
Requires: u2f-hidraw-policy
Requires: %{chromium_name}-common%{_isa} = %{version}-%{release}

ExclusiveArch: x86_64

Provides: bundled(angle)
Provides: bundled(bintrees)
Provides: bundled(boringssl)
Provides: bundled(brotli)
Provides: bundled(bspatch)
Provides: bundled(cacheinvalidation)
Provides: bundled(colorama)
Provides: bundled(crashpad)
Provides: bundled(crc32c)
Provides: bundled(dav1d)
Provides: bundled(double-conversion)
Provides: bundled(dmg_fp)
Provides: bundled(expat)
Provides: bundled(fdmlibm)
Provides: bundled(flac)
Provides: bundled(fips181)
Provides: bundled(fontconfig)
Provides: bundled(freetype)
Provides: bundled(gperftools)
Provides: bundled(harfbuzz-ng)
Provides: bundled(highway)
Provides: bundled(hunspell)
Provides: bundled(iccjpeg)
Provides: bundled(icu)
Provides: bundled(kitchensink)
Provides: bundled(lcms2)
Provides: bundled(leveldb)
Provides: bundled(libaddressinput)
Provides: bundled(libaom)
Provides: bundled(libdrm)
Provides: bundled(libevent)
Provides: bundled(libjingle)
Provides: bundled(libjpeg)
Provides: bundled(libopenjpeg2)
Provides: bundled(libphonenumber)
Provides: bundled(libpng)
Provides: bundled(libsecret)
Provides: bundled(libsrtp)
Provides: bundled(libtiff)
Provides: bundled(libudis86)
Provides: bundled(libusbx)
Provides: bundled(libvpx)
Provides: bundled(libwebp)
Provides: bundled(libyuv)
Provides: bundled(libxml)
Provides: bundled(libxslt)
Provides: bundled(libXNVCtrl)
Provides: bundled(lzma)
Provides: bundled(mesa)
Provides: bundled(NSBezierPath)
Provides: bundled(mozc)
Provides: bundled(opus)
Provides: bundled(ots)
Provides: bundled(protobuf)
Provides: bundled(qcms)
Provides: bundled(re2)
Provides: bundled(sfntly)
Provides: bundled(skia)
Provides: bundled(SMHasher)
Provides: bundled(snappy)
Provides: bundled(speech-dispatcher)
Provides: bundled(sqlite)
Provides: bundled(superfasthash)
Provides: bundled(talloc)
Provides: bundled(usrsctp)
Provides: bundled(v8)
Provides: bundled(webrtc)
Provides: bundled(woff2)
Provides: bundled(xdg-mime)
Provides: bundled(xdg-user-dirs)
Provides: bundled(zstd)

# For selinux scriptlet
Requires(post): /usr/sbin/semanage
Requires(post): /usr/sbin/restorecon

%description
Trivalent is a security-focused browser built upon the Chromium web browser.

%package common
Summary: Files needed for Chromium
%description common
%{summary}.

%package qt5-ui
Summary: Qt5 UI built from Chromium
Requires: %{chromium_name}%{_isa} = %{version}-%{release}

%description qt5-ui
Qt5 UI for chromium.

%package qt6-ui
Summary: Qt6 UI built from Chromium
Requires: %{chromium_name}%{_isa} = %{version}-%{release}

%description qt6-ui
Qt6 UI for chromium.

%prep
%setup -q -n chromium-%{version}

### Patches ###
%autopatch -p1 -m 1000 -M %{_fedoraPatchCount}
%autopatch -p1 -m 2000 -M %{_vanadiumPatchCount}
%autopatch -p1 -m 3000 -M %{_hardeningPatchCount}

### Branding ###
cp -a %{SOURCE12} chrome/app/theme/default_100_percent/chromium/linux/product_logo_16.png
cp -a %{SOURCE14} chrome/app/theme/default_100_percent/chromium/linux/product_logo_32.png
cp -a %{SOURCE12} chrome/app/theme/default_100_percent/chromium/product_logo_16.png
cp -a %{SOURCE14} chrome/app/theme/default_100_percent/chromium/product_logo_32.png
cp -a %{SOURCE13} chrome/app/theme/default_100_percent/chromium/product_logo_name_22.png
cp -a %{SOURCE13} chrome/app/theme/default_100_percent/chromium/product_logo_name_22_white.png

cp -a %{SOURCE14} chrome/app/theme/default_200_percent/chromium/linux/product_logo_16.png
cp -a %{SOURCE16} chrome/app/theme/default_200_percent/chromium/linux/product_logo_32.png
cp -a %{SOURCE14} chrome/app/theme/default_200_percent/chromium/product_logo_16.png
cp -a %{SOURCE16} chrome/app/theme/default_200_percent/chromium/product_logo_32.png
cp -a %{SOURCE15} chrome/app/theme/default_200_percent/chromium/product_logo_name_22.png
cp -a %{SOURCE15} chrome/app/theme/default_200_percent/chromium/product_logo_name_22_white.png

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
find -type f \( -iname "*.py" \) -exec sed -i '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{chromium_pybin}=' {} +

# Add correct path for nodejs binary
mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node

# Get rid of the bundled esbuild
ln -sf %{_bindir}/esbuild third_party/devtools-frontend/src/third_party/esbuild/esbuild

# Get rid of the pre-built eu-strip binary, it is x86_64 and of mysterious origin
rm -rf buildtools/third_party/eu-strip/bin/eu-strip
  
# Replace it with a symlink to the Fedora copy
ln -s %{_bindir}/eu-strip buildtools/third_party/eu-strip/bin/eu-strip

# Hard code extra version
sed -i 's/getenv("CHROME_VERSION_EXTRA")/"%{chromium_name}"/' chrome/common/channel_info_posix.cc

# bz#2265957, add correct platform
sed -i "s/Linux x86_64/Linux %{_arch}/" content/common/user_agent.cc

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
rustc_version="$(rustc --version)"
rust_bindgen_root="%{_prefix}"

# set clang version
clang_version="$(clang --version | sed -n 's/clang version //p' | cut -d. -f1)"
clang_base_path="$(clang --version | grep InstalledDir | cut -d' ' -f2 | sed 's#/bin##')"

CHROMIUM_GN_DEFINES=""
CHROMIUM_GN_DEFINES+=' custom_toolchain="//build/toolchain/linux/unbundle:default"'
CHROMIUM_GN_DEFINES+=' host_toolchain="//build/toolchain/linux/unbundle:default"'
CHROMIUM_GN_DEFINES+=' is_debug=false dcheck_always_on=false dcheck_is_configurable=false'
CHROMIUM_GN_DEFINES+=' enable_nacl=false'
CHROMIUM_GN_DEFINES+=' system_libdir="%{_lib}"'
CHROMIUM_GN_DEFINES+=' is_official_build=true'
sed -i 's|OFFICIAL_BUILD|GOOGLE_CHROME_BUILD|g' tools/generate_shim_headers/generate_shim_headers.py
CHROMIUM_GN_DEFINES+=' chrome_pgo_phase=0'
CHROMIUM_GN_DEFINES+=' is_cfi=true use_thin_lto=true'
CHROMIUM_GN_DEFINES+=' enable_reporting=false'
CHROMIUM_GN_DEFINES+=' enable_remoting=false'
CHROMIUM_GN_DEFINES+=' is_clang=true'
CHROMIUM_GN_DEFINES+=" clang_base_path=\"$clang_base_path\""
CHROMIUM_GN_DEFINES+=" clang_version=\"$clang_version\""
CHROMIUM_GN_DEFINES+=' clang_use_chrome_plugins=false'
CHROMIUM_GN_DEFINES+=' use_lld=true'
CHROMIUM_GN_DEFINES+=' rust_sysroot_absolute="%{_prefix}"'
CHROMIUM_GN_DEFINES+=" rust_bindgen_root=\"$rust_bindgen_root\""
CHROMIUM_GN_DEFINES+=" rustc_version=\"$rustc_version\""
CHROMIUM_GN_DEFINES+=' use_sysroot=false'
CHROMIUM_GN_DEFINES+=' icu_use_data_file=true'
CHROMIUM_GN_DEFINES+=' target_os="linux"'
CHROMIUM_GN_DEFINES+=' current_os="linux"'
CHROMIUM_GN_DEFINES+=' treat_warnings_as_errors=false'
CHROMIUM_GN_DEFINES+=' enable_iterator_debugging=false'
CHROMIUM_GN_DEFINES+=' enable_vr=false'
CHROMIUM_GN_DEFINES+=' enable_arcore=false'
CHROMIUM_GN_DEFINES+=' enable_openxr=false'
CHROMIUM_GN_DEFINES+=' enable_cardboard=false'
CHROMIUM_GN_DEFINES+=' build_dawn_tests=false enable_perfetto_unittests=false'
CHROMIUM_GN_DEFINES+=' disable_fieldtrial_testing_config=true'
CHROMIUM_GN_DEFINES+=' symbol_level=%{debug_level} blink_symbol_level=%{debug_level}'
CHROMIUM_GN_DEFINES+=' angle_has_histograms=false'
CHROMIUM_GN_DEFINES+=' safe_browsing_use_unrar=false'
CHROMIUM_GN_DEFINES+=' ffmpeg_branding="Chrome" proprietary_codecs=true is_component_ffmpeg=true enable_ffmpeg_video_decoders=true media_use_ffmpeg=true'
CHROMIUM_GN_DEFINES+=' media_use_openh264=true'
CHROMIUM_GN_DEFINES+=' rtc_use_h264=true'
CHROMIUM_GN_DEFINES+=' use_kerberos=true'
CHROMIUM_GN_DEFINES+=' use_qt=true moc_qt5_path="%{_libdir}/qt5/bin/"'
CHROMIUM_GN_DEFINES+=' use_qt6=true moc_qt6_path="%{_libdir}/qt6/libexec/"'
CHROMIUM_GN_DEFINES+=' use_gio=true use_pulseaudio=true'
CHROMIUM_GN_DEFINES+=' enable_widevine=true'
CHROMIUM_GN_DEFINES+=' use_vaapi=true'
CHROMIUM_GN_DEFINES+=' rtc_use_pipewire=true rtc_link_pipewire=true'
CHROMIUM_GN_DEFINES+=' use_system_libffi=true' # ffi_pic is not found
export CHROMIUM_GN_DEFINES

system_libs=()
system_libs+=(ffmpeg)
system_libs+=(openh264)
build/linux/unbundle/replace_gn_files.py --system-libraries ${system_libs[@]}

# Check that there is no system 'google' module, shadowing bundled ones:
if python3 -c 'import google ; print google.__path__' 2> /dev/null ; then \
    echo "Python 3 'google' module is defined, this will shadow modules of this build"; \
    exit 1 ; \
fi

mkdir -p %{chromebuilddir} && cp -a %{_bindir}/gn %{chromebuilddir}/

%{chromebuilddir}/gn --script-executable=%{chromium_pybin} gen --args="$CHROMIUM_GN_DEFINES" %{chromebuilddir}

%build_target %{chromebuilddir} chrome
%build_target %{chromebuilddir} policy_templates

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
  cp -a libvk_swiftshader.so %{buildroot}%{chromium_path}
  cp -a libvulkan.so.1 %{buildroot}%{chromium_path}
  cp -a vk_swiftshader_icd.json %{buildroot}%{chromium_path}
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
  cp -a libqt5_shim.so %{buildroot}%{chromium_path}
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

cp -a out/Release/gen/chrome/app/policy/common/html/en-US/*.html .
cp -a out/Release/gen/chrome/app/policy/linux/examples/chrome.json .

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp -a chrome/app/theme/chromium/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{chromium_name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
cp -a chrome/app/theme/chromium/product_logo_128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{chromium_name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
cp -a chrome/app/theme/chromium/product_logo_64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{chromium_name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
cp -a chrome/app/theme/chromium/product_logo_48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{chromium_name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
cp -a chrome/app/theme/chromium/product_logo_24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{chromium_name}.png

# Install the master_preferences file
install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/%{chromium_name}/

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE4}

install -D -m0644 chrome/installer/linux/common/chromium-browser/chromium-browser.appdata.xml \
  ${RPM_BUILD_ROOT}%{_datadir}/metainfo/%{chromium_name}.appdata.xml
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

%files
%doc AUTHORS
%doc chrome_policy_list.html *.json
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{chromium_name}/%{chromium_name}.conf
%config %{_sysconfdir}/%{chromium_name}/master_preferences
%config %{_sysconfdir}/%{chromium_name}/policies/
%{_bindir}/%{chromium_name}
%{chromium_path}/*.bin
%{chromium_path}/chrome_*.pak
%{chromium_path}/chrome_crashpad_handler
%{chromium_path}/resources.pak
%{chromium_path}/%{chromium_name}
%{chromium_path}/%{chromium_name}.sh
%{_mandir}/man1/%{chromium_name}.*
%{_datadir}/icons/hicolor/*/apps/%{chromium_name}.png
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/*.appdata.xml
%{_datadir}/gnome-control-center/default-apps/%{chromium_name}.xml

%files qt5-ui
%{chromium_path}/libqt5_shim.so

%files qt6-ui
%{chromium_path}/libqt6_shim.so

%files common
%{chromium_path}/libvk_swiftshader.so*
%{chromium_path}/libvulkan.so*
%{chromium_path}/vk_swiftshader_icd.json
%{chromium_path}/libEGL.so*
%{chromium_path}/libGLESv2.so*
%{chromium_path}/icudtl.dat
%dir %{chromium_path}/
%dir %{chromium_path}/locales/
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
# Chromium _ALWAYS_ needs en-US.pak as a fallback
# This means we cannot apply the lang code here.
# Otherwise, it is filtered out on install.
%{chromium_path}/locales/en-US.pak
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
