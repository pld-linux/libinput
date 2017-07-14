#
# Conditional build:
%bcond_without	gui		# libinput-debug-gui
%bcond_without	libunwind	# libunwind debugging support
%bcond_with	static_libs	# static library
%bcond_without	doc		# documentation

%ifnarch %{ix86} %{x8664} %{arm} hppa ia64 mips ppc ppc64 sh
%undefine	with_libunwind
%endif
Summary:	Input device library
Summary(pl.UTF-8):	Biblioteka urządzeń wejściowych
Name:		libinput
Version:	1.8.0
Release:	2
License:	MIT
Group:		Libraries
Source0:	https://www.freedesktop.org/software/libinput/%{name}-%{version}.tar.xz
# Source0-md5:	f12066eeda3e1aeaa65eeca4b9ad833d
URL:		https://www.freedesktop.org/wiki/Software/libinput/
BuildRequires:	check-devel >= 0.9.10
%if %{with gui}
BuildRequires:	cairo-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gtk+3-devel >= 3.0
%endif
%if %{with apidocs}
BuildRequires:	doxygen >= 1.6.0
BuildRequires:	graphviz >= 2.26.0
%endif
BuildRequires:	libevdev-devel >= 1.3
%{?with_libunwind:BuildRequires:	libunwind-devel}
BuildRequires:	libwacom-devel >= 0.20
BuildRequires:	mtdev-devel >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	udev-devel
Requires:	libevdev >= 1.3
Requires:	libwacom >= 0.20
Requires:	mtdev >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libinput is a library that handles input devices for display servers
and other applications that need to directly deal with input devices.

It provides device detection, device handling, input device event
processing and abstraction so minimize the amount of custom input code
the user of libinput need to provide the common set of functionality
that users expect.

%description -l pl.UTF-8
libinput to biblioteka obsługująca urządzenia wejściowe dla serwerów
grafiki i innych aplikacji wymagających bezpośredniej obsługi urządzeń
wejściowych.

Biblioteka zapewnia wykrywanie urządzeń, obsługę urządzeń,
przetwarzanie zdarzeń urządzeń wejściowych oraz abstrakcję,
minimalizując ilość własnego kodu, który musi napisać użytkownik
biblioteki, aby zapewnić oczekiwaną funkcjonalność.

%package gui
Summary:	Debugging GUI for libinput
Summary(pl.UTF-8):	Graficzny interfejs diagnostyczny do libinput
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gui
Debugging GUI for libinput.

%description gui -l pl.UTF-8
Graficzny interfejs diagnostyczny do libinput.

%package devel
Summary:	Development files for libinput
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libinput
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	udev-devel

%description devel
This package contains the header files for developing applications
that use libinput.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe niezbędne do tworzenia aplikacji
wykorzystujących bibliotekę libinput.

%package static
Summary:	Static libinput library
Summary(pl.UTF-8):	Statyczna biblioteka libinput
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libinput library.

%description static -l pl.UTF-8
Statyczna biblioteka libinput.

%package apidocs
Summary:	API documentation for libinput library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libinput
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libinput library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libinput.

%prep
%setup -q

%build
%configure \
	%{!?with_gui:--disable-debug-gui} \
	--disable-silent-rules \
	--enable-documentation%{!?with_doc:=no} \
	%{?with_static_libs:--enable-static} \
	%{!?with_libunwind:--without-libunwind} \
	--with-udev-dir=/lib/udev

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_bindir}/libinput
%attr(755,root,root) %{_bindir}/libinput-debug-events
%attr(755,root,root) %{_bindir}/libinput-list-devices
%attr(755,root,root) %{_libdir}/libinput.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libinput.so.10
%dir %{_libexecdir}/libinput
%attr(755,root,root) %{_libexecdir}/libinput/libinput-debug-events
%attr(755,root,root) %{_libexecdir}/libinput/libinput-list-devices
%attr(755,root,root) %{_libexecdir}/libinput/libinput-measure
%attr(755,root,root) %{_libexecdir}/libinput/libinput-measure-touchpad-tap
%attr(755,root,root) /lib/udev/libinput-device-group
%attr(755,root,root) /lib/udev/libinput-model-quirks
/lib/udev/rules.d/80-libinput-device-groups.rules
/lib/udev/hwdb.d/90-libinput-model-quirks.hwdb
/lib/udev/rules.d/90-libinput-model-quirks.rules
%{_mandir}/man1/libinput.1*
%{_mandir}/man1/libinput-debug-events.1*
%{_mandir}/man1/libinput-list-devices.1*
%{_mandir}/man1/libinput-measure.1*
%{_mandir}/man1/libinput-measure-touchpad-tap.1*

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/libinput/libinput-debug-gui
%{_mandir}/man1/libinput-debug-gui.1*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libinput.so
%{_includedir}/libinput.h
%{_pkgconfigdir}/libinput.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libinput.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
