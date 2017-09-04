Name:           stlink
Version:        1.4.0
Release:        1%{?dist}
Summary:        STM32 discovery line Linux programmer
License:        BSD

Url:            https://github.com/texane/stlink
Source0:        https://github.com/texane/stlink/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(libusb-1.0)
Requires:       pkgconfig(udev)

%description
STLINK v1/v2 JTAG/SWD debugging/flashing tool for STM32 microcontrollers.

%package        gui
Summary:        GUI for STM32 discovery line linux programmer
Requires:       %{name} = %{version}

%description    gui
STLINK v1/v2 JTAG/SWD debugging/flashing tool for STM32 microcontrollers.

%package        devel
Summary:        Include files and mandatory libraries for development
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Include files and mandatory libraries for development.

%prep
%setup -q
#https://github.com/texane/stlink/issues/633
sed -i "s|STLINK_LIBRARY_PATH \"lib/\${CMAKE_LIBRARY_PATH}\"|STLINK_LIBRARY_PATH \"%{_libdir}/\${CMAKE_LIBRARY_PATH}\"|" CMakeLists.txt

%build
mkdir build
pushd build
    %cmake .. -DSTLINK_UDEV_RULES_DIR="%{_udevrulesdir}"
    %make_build
popd

%install
pushd build
    %make_install
popd

%post
/sbin/ldconfig
%{udev_rules_update}

%postun
/sbin/ldconfig
%{udev_rules_update}

%files
%doc README.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/modprobe.d/%{name}*
%{_bindir}/st-*
%{_libdir}/lib%{name}-shared.so.*
%{_mandir}/man1/st-*.1*
%{_udevrulesdir}/49-%{name}*

%files gui
%{_bindir}/%{name}-gui
%{_datadir}/%{name}

%files    devel
%{_includedir}/%{name}*
%{_libdir}/lib%{name}-shared.so
%{_libdir}/lib%{name}.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Sep 01 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Mon Jun 20 2016 Vasiliy N. Glazov <vascom2@gmail.com> 1.2.0-1
- Update to 1.2.0

* Tue Aug 18 2015 Vasiliy N. Glazov <vascom2@gmail.com> 1.1.0-1
- Correct spec for Fedora

* Fri Apr  3 2015 dmitry_r@opensuse.org
- Update to version 1.1.0
  * New devices support, see included README file
  * Bugfixes
* Wed Jun 11 2014 dmitry_r@opensuse.org
- Add COPYING and README to package documentation
* Fri Jun  6 2014 dmitry_r@opensuse.org
- Initial package, version 1.0.0
