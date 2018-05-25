# Do we add appdata-files?
%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without appdata
%else
%bcond_with appdata
%endif

# Set to bcond_without or use --with bootstrap if bootstrapping a new release
# or architecture
%bcond_without bootstrap

# Build with Emacs support
%bcond_with emacs

# Run git tests
%bcond_without git_test

# Set to bcond_with or use --without gui to disable qt4 gui build
%bcond_with gui

# Use ncurses for colorful output
%bcond_without ncurses

# Setting the Python-version used by default
%if 0%{?rhel} && 0%{?rhel} < 8
%bcond_with python3
%else
%bcond_without python3
%endif

# Enable RPM dependency generators for cmake files written in Python
%bcond_without rpm

# Sphinx-build cannot import CMakeLexer on EPEL <= 6
%if 0%{?rhel} && 0%{?rhel} <= 6
%bcond_with sphin
%else
# broken in prefix
%bcond_with sphinx
%endif

# Run tests
%bcond_without test

# Enable X11 tests
%bcond_without X11_test

# Place rpm-macros into proper location
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# Setup _pkgdocdir if not defined already
%{!?_pkgdocdir:%global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global major_version 3
%global minor_version 11
# Set to RC version if building RC, else %%{nil}
#global rcsuf rc3
%{?rcsuf:%global relsuf .%{rcsuf}}
%{?rcsuf:%global versuf -%{rcsuf}}

# Uncomment if building for EPEL
%global name_suffix %%{major_version}%%{minor_version}
%global orig_name cmake

Name:           %{orig_name}%{?name_suffix}
Version:        %{major_version}.%{minor_version}.2
Release:        1%{?relsuf}%{?dist}
Summary:        Cross-platform make system

# most sources are BSD
# Source/CursesDialog/form/ a bunch is MIT
# Source/kwsys/MD5.c is zlib
# some GPL-licensed bison-generated files, which all include an
# exception granting redistribution under terms of your choice
License:        BSD and MIT and zlib
URL:            https://www.cmake.org
Source0:        https://www.cmake.org/files/v%{major_version}.%{minor_version}/%{orig_name}-%{version}%{?versuf}.tar.gz
Source1:        %{orig_name}-init.el
Source2:        macros.%{orig_name}
# See https://bugzilla.redhat.com/show_bug.cgi?id=1202899
Source3:        %{orig_name}.attr
Source4:        %{orig_name}.prov
Source5:        %{orig_name}.req

# Always start regular patches with numbers >= 100.
# We need lower numbers for patches in compat package.
# And this enables us to use %%autosetup
#
# Patch to fix RindRuby vendor settings
# http://public.kitware.com/Bug/view.php?id=12965
# https://bugzilla.redhat.com/show_bug.cgi?id=822796
Patch100:       %{orig_name}-findruby.patch
# replace release flag -O3 with -O2 for fedora
Patch101:       %{orig_name}-fedora-flag_release.patch
# Add dl to CMAKE_DL_LIBS on MINGW
# https://gitlab.kitware.com/cmake/cmake/issues/17600
Patch102:       %{orig_name}-mingw-dl.patch

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  sed
%if %{with git_test}
# Tests fail if only git-core is installed, bug #1488830
BuildRequires:  git
%else
BuildConflicts: git-core
%endif
%if %{with X11_test}
BuildRequires:  libX11-devel
%endif
%if %{with ncurses}
BuildRequires:  ncurses-devel
%endif
%if %{with sphinx}
BuildRequires:  %{_bindir}/sphinx-build
%endif
%if %{without bootstrap}
BuildRequires:  bzip2-devel
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  jsoncpp-devel
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  libarchive-devel
%else
BuildRequires:  libarchive3-devel
%endif
BuildRequires:  libuv-devel
BuildRequires:  rhash-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
%endif
%if %{with emacs}
BuildRequires:  emacs
%endif
%if %{with rpm}
%if %{with python3}
%{!?python3_pkgversion: %global python3_pkgversion 3}
BuildRequires:  python%{python3_pkgversion}-devel
%else
BuildRequires:  python2-devel
%endif
%endif
#BuildRequires: xmlrpc-c-devel
%if %{with gui}
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires: pkgconfig(Qt5Widgets)
%else
BuildRequires: pkgconfig(QtGui)
%endif
BuildRequires: desktop-file-utils
%endif

%if %{without bootstrap}
# Ensure we have our own rpm-macros in place during build.
BuildRequires:  %{name}-rpm-macros
%endif

Requires:       %{name}-data = %{version}-%{release}
Requires:       %{name}-rpm-macros = %{version}-%{release}
Requires:       %{name}-filesystem%{?_isa} = %{version}-%{release}

# Provide the major version name
Provides: %{orig_name}%{major_version} = %{version}-%{release}

# Source/kwsys/MD5.c
# see https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries
Provides: bundled(md5-deutsch)

# https://fedorahosted.org/fpc/ticket/555
Provides: bundled(kwsys)

%description
CMake is used to control the software compilation process using simple
platform and compiler independent configuration files. CMake generates
native makefiles and workspaces that can be used in the compiler
environment of your choice. CMake is quite sophisticated: it is possible
to support complex environments requiring system configuration, preprocessor
generation, code generation, and template instantiation.


%package        data
Summary:        Common data-files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       %{name}-rpm-macros = %{version}-%{release}
%if %{with emacs}
%if 0%{?fedora} || 0%{?rhel} >= 7
Requires:       emacs-filesystem%{?_emacs_version: >= %{_emacs_version}}
%endif
%endif

BuildArch:      noarch

%description    data
This package contains common data-files for %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
This package contains documentation for %{name}.


%package        filesystem
Summary:        Directories used by CMake modules

%description    filesystem
This package owns all directories used by CMake modules.


%if %{with gui}
%package        gui
Summary:        Qt GUI for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hicolor-icon-theme
Requires:       shared-mime-info%{?_isa}

%description    gui
The %{name}-gui package contains the Qt based GUI for %{name}.
%endif


%package        rpm-macros
Summary:        Common RPM macros for %{name}
Requires:       rpm
# when subpkg introduced
Conflicts:      cmake-data < 3.10.1-2

BuildArch:      noarch

%description    rpm-macros
This package contains common RPM macros for %{name}.


%prep
%autosetup -n %{orig_name}-%{version}%{?versuf} -p 1

%if %{with rpm}
%if %{with python3}
echo '#!%{__python3}' > %{orig_name}.prov
echo '#!%{__python3}' > %{orig_name}.req
%else
echo '#!%{__python2}' > %{orig_name}.prov
echo '#!%{__python2}' > %{orig_name}.req
%endif
tail -n +2 %{SOURCE4} >> %{orig_name}.prov
tail -n +2 %{SOURCE5} >> %{orig_name}.req
%endif

%global cmake_prefix /opt/%{name}
%global cmake_datadir %{cmake_prefix}/share

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{?__global_ldflags}"
mkdir build
pushd build
../bootstrap --prefix=%{cmake_prefix} --datadir=/share/%{orig_name} \
             --docdir=/share/doc/%{orig_name} --mandir=/share/man \
             --%{?with_bootstrap:no-}system-libs \
             --parallel=`/usr/bin/getconf _NPROCESSORS_ONLN` \
%if %{with sphinx}
             --sphinx-man --sphinx-html \
%else
             --sphinx-build=%{_bindir}/false \
%endif
             --%{!?with_gui:no-}qt-gui \
;
%make_build VERBOSE=1


%install
mkdir -p %{buildroot}%{_pkgdocdir}
%make_install -C build CMAKE_DOC_DIR=%{buildroot}%{_pkgdocdir}
find %{buildroot}%{cmake_datadir}/%{orig_name}/Modules -type f | xargs chmod -x
[ -n "$(find %{buildroot}%{cmake_datadir}/%{orig_name}/Modules -name \*.orig)" ] &&
  echo "Found .orig files in %{cmake_datadir}/%{orig_name}/Modules, rebase patches" &&
  exit 1
# Install major_version name links
%{!?name_suffix:for f in ccmake cmake cpack ctest; do ln -s $f %{buildroot}%{_bindir}/${f}%{major_version}; done}
# Install bash completion symlinks
mkdir -p %{buildroot}%{cmake_datadir}/bash-completion/completions
for f in %{buildroot}%{cmake_datadir}/%{orig_name}/completions/*
do
  ln -s ../../%{orig_name}/completions/$(basename $f) %{buildroot}%{cmake_datadir}/bash-completion/completions
done
%if %{with emacs}
# Install emacs cmake mode
mkdir -p %{buildroot}%{_emacs_sitelispdir}/%{orig_name}
install -p -m 0644 Auxiliary/cmake-mode.el %{buildroot}%{_emacs_sitelispdir}/%{orig_name}/%{orig_name}-mode.el
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/%{orig_name}/%{orig_name}-mode.el
mkdir -p %{buildroot}%{_emacs_sitestartdir}
install -p -m 0644 %SOURCE1 %{buildroot}%{_emacs_sitestartdir}
%endif
# RPM macros
install -p -m0644 -D %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{orig_name}
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}%{rpm_macros_dir}/macros.%{orig_name}
touch -r %{SOURCE2} %{buildroot}%{rpm_macros_dir}/macros.%{orig_name}
%if %{with rpm} && 0%{?_rpmconfigdir:1}
# RPM auto provides
install -p -m0644 -D %{SOURCE3} %{buildroot}%{_prefix}/lib/rpm/fileattrs/%{orig_name}.attr
install -p -m0755 -D %{orig_name}.prov %{buildroot}%{_prefix}/lib/rpm/%{orig_name}.prov
install -p -m0755 -D %{orig_name}.req %{buildroot}%{_prefix}/lib/rpm/%{orig_name}.req
%endif
mkdir -p %{buildroot}%{_libdir}/%{orig_name}
# Install copyright files for main package
find Source Utilities -type f -iname copy\* | while read f
do
  fname=$(basename $f)
  dir=$(dirname $f)
  dname=$(basename $dir)
  cp -p $f ./${fname}_${dname}
done
# Cleanup pre-installed documentation
%if %{with sphinx}
mv %{buildroot}%{_docdir}/%{orig_name}/html .
%endif
rm -rf %{buildroot}%{_docdir}/%{orig_name}
# Install documentation to _pkgdocdir
mkdir -p %{buildroot}%{_pkgdocdir}
cp -pr %{buildroot}%{cmake_datadir}/%{orig_name}/Help %{buildroot}%{_pkgdocdir}
mv %{buildroot}%{_pkgdocdir}/Help %{buildroot}%{_pkgdocdir}/rst
%if %{with sphinx}
mv html %{buildroot}%{_pkgdocdir}
%endif

%if %{with gui}
# Desktop file
desktop-file-install --delete-original \
  --dir=%{buildroot}%{cmake_datadir}/applications \
  %{buildroot}%{cmake_datadir}/applications/%{orig_name}-gui.desktop

%if %{with appdata}
# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p %{buildroot}%{cmake_datadir}/appdata
cat > %{buildroot}%{cmake_datadir}/appdata/cmake-gui.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Ryan Lerch <rlerch@redhat.com> -->
<!--
EmailAddress: kitware@kitware.com
SentUpstream: 2014-09-17
-->
<application>
  <id type="desktop">cmake-gui.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>CMake GUI</name>
  <summary>Create new CMake projects</summary>
  <description>
    <p>
      CMake is an open source, cross platform build system that can build, test,
      and package software. CMake GUI is a graphical user interface that can
      create and edit CMake projects.
    </p>
  </description>
  <url type="homepage">http://www.cmake.org</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/CMake/a.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF
%endif
%endif

# create manifests for splitting files and directories for filesystem-package
find %{buildroot}%{cmake_datadir}/%{orig_name} -type d | \
  sed -e 's!^%{buildroot}!%%dir "!g' -e 's!$!"!g' > data_dirs.mf
find %{buildroot}%{cmake_datadir}/%{orig_name} -type f | \
  sed -e 's!^%{buildroot}!"!g' -e 's!$!"!g' > data_files.mf
find %{buildroot}%{_libdir}/%{orig_name} -type d | \
  sed -e 's!^%{buildroot}!%%dir "!g' -e 's!$!"!g' > lib_dirs.mf
find %{buildroot}%{_libdir}/%{orig_name} -type f | \
  sed -e 's!^%{buildroot}!"!g' -e 's!$!"!g' > lib_files.mf
find %{buildroot}%{cmake_prefix}/bin -type f -or -type l -or -xtype l | \
  sed -e '/.*-gui$/d' -e '/^$/d' -e 's!^%{buildroot}!"!g' -e 's!$!"!g' >> lib_files.mf


%if %{with test}
%check
%if 0%{?rhel} && 0%{?rhel} <= 6
mv -f Modules/FindLibArchive.cmake Modules/FindLibArchive.disabled
%endif
pushd build
#CMake.FileDownload, CTestTestUpload, and curl require internet access
# RunCMake.CPack_RPM is broken if disttag contains "+", bug #1499151
NO_TEST="CMake.FileDownload|CTestTestUpload|curl|RunCMake.CPack_RPM"
# RunCMake.File_Generate fails on S390X
%ifarch s390x
NO_TEST="$NO_TEST|RunCMake.File_Generate"
%endif
export NO_TEST
bin/ctest%{?name_suffix} -V -E "$NO_TEST" %{?_smp_mflags}
popd
%if 0%{?rhel} && 0%{?rhel} <= 6
mv -f Modules/FindLibArchive.disabled Modules/FindLibArchive.cmake
%endif
%endif


%if %{with gui}
%post gui
update-desktop-database &> /dev/null || :
/bin/touch --no-create %{cmake_datadir}/mime || :
/bin/touch --no-create %{cmake_datadir}/icons/hicolor &>/dev/null || :

%postun gui
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{cmake_datadir}/mime || :
    update-mime-database %{?fedora:-n} %{cmake_datadir}/mime &> /dev/null || :
    /bin/touch --no-create %{cmake_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/gtk-update-icon-cache %{cmake_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gui
update-mime-database %{?fedora:-n} %{cmake_datadir}/mime &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{cmake_datadir}/icons/hicolor &>/dev/null || :
%endif


%files -f lib_files.mf
%doc %dir %{_pkgdocdir}
%license Copyright.txt*
%license COPYING*
%if %{with sphinx}
%{_mandir}/man1/c%{orig_name}.1.*
%{_mandir}/man1/%{orig_name}.1.*
%{_mandir}/man1/cpack%{?name_suffix}.1.*
%{_mandir}/man1/ctest%{?name_suffix}.1.*
%{_mandir}/man7/*.7.*
%endif


%files data -f data_files.mf
%{cmake_datadir}/aclocal/%{orig_name}.m4
%{cmake_datadir}/bash-completion
%if %{with emacs}
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_emacs_sitelispdir}/%{orig_name}
%{_emacs_sitestartdir}/%{orig_name}-init.el
%else
%{_emacs_sitelispdir}
%{_emacs_sitestartdir}
%endif
%endif


%files doc
# Pickup license-files from main-pkg's license-dir
# If there's no license-dir they are picked up by %%doc previously
%{?_licensedir:%license %{cmake_datadir}/licenses/%{orig_name}*}
%doc %{_pkgdocdir}


%files filesystem -f data_dirs.mf -f lib_dirs.mf


%if %{with gui}
%files gui
%{_bindir}/%{orig_name}-gui
%if %{with appdata}
%{cmake_datadir}/appdata/*.appdata.xml
%endif
%{cmake_datadir}/applications/%{orig_name}-gui.desktop
%{cmake_datadir}/mime/packages
%{cmake_datadir}/icons/hicolor/*/apps/CMake%{?name_suffix}Setup.png
%if %{with sphinx}
%{_mandir}/man1/%{orig_name}-gui.1.*
%endif
%endif


%files rpm-macros
%{rpm_macros_dir}/macros.%{orig_name}
%if %{with rpm} && 0%{?_rpmconfigdir:1}
%{_rpmconfigdir}/fileattrs/%{orig_name}.attr
%{_rpmconfigdir}/%{orig_name}.prov
%{_rpmconfigdir}/%{orig_name}.req
%endif


%changelog
* Fri May 25 2018 Jan Kundrát <jkt@kde.org> - 3.11.2-1
- Initial release, shamelessly stolen from the main Fedora
