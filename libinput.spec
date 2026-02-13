# TODO:
# - package user docs from build/Documentation
#
# Conditional build:
%bcond_without	gui		# libinput-debug-gui
%bcond_with	gtk4		# build libinput-debug-gui with gtk4
%bcond_without	libunwind	# libunwind debugging support
%bcond_without	doc		# documentation
%bcond_without	tests		# tests

%ifnarch %{ix86} %{x8664} %{arm} hppa ia64 mips ppc ppc64 sh
%undefine	with_libunwind
%endif
Summary:	Input device library
Summary(pl.UTF-8):	Biblioteka urządzeń wejściowych
Name:		libinput
Version:	1.31.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://gitlab.freedesktop.org/libinput/libinput/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	97ec7b0621eac9a7d07c5ff64593a2da
URL:		https://www.freedesktop.org/wiki/Software/libinput/
BuildRequires:	check-devel >= 0.9.10
BuildRequires:	libevdev-devel >= 1.10.0
%{?with_libunwind:BuildRequires:	libunwind-devel}
BuildRequires:	libwacom-devel >= 2.18.0
BuildRequires:	lua54-devel
BuildRequires:	meson >= 0.64.0
BuildRequires:	mtdev-devel >= 1.1.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
%{?with_tests:BuildRequires:	python3-pytest}
%{?with_tests:BuildRequires:	python3-pytest-xdist}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
%{?with_tests:BuildRequires:	valgrind}
BuildRequires:	xz
%if %{with gui}
BuildRequires:	cairo-devel
BuildRequires:	glib2-devel >= 2.0
%if %{with gtk4}
BuildRequires:	gtk4-devel >= 4.0
%else
BuildRequires:	gtk+3-devel >= 3.20
%endif
BuildRequires:	wayland-devel
BuildRequires:	wayland-protocols
BuildRequires:	xorg-lib-libX11-devel
%endif
%if %{with doc}
BuildRequires:	doxygen >= 1.8.3
BuildRequires:	graphviz >= 2.26.0
BuildRequires:	python3-recommonmark
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	libevdev >= 1.10.0
Requires:	libwacom >= 2.18.0
Requires:	mtdev >= 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# libinput-util.h:31
# #warning "libinput relies on assert(). #defining NDEBUG is not recommended"
%define		filterout_cpp	-DNDEBUG

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
%if %{with gtk4}
Requires:	gtk4 >= 4.0
%else
Requires:	gtk+3 >= 3.20
%endif

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

%package apidocs
Summary:	API documentation for libinput library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libinput
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libinput library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libinput.

%package -n zsh-completion-%{name}
Summary:	Zsh completion for libinput command
Summary(pl.UTF-8):	Dopełnianie parametrów w zsh dla polecenia libinput
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-%{name}
Zsh completion for libinput command.

%description -n zsh-completion-%{name} -l pl.UTF-8
Dopełnianie parametrów w zsh dla polecenia libinput.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	tools/libinput-analyze-{buttons,per-slot-delta,recording,touch-down-state}.py \
	tools/libinput-list-kernel-devices.py \
	tools/libinput-measure-{fuzz,touchpad-pressure,touch-size,touchpad-tap}.py \
	tools/libinput-{replay,measure-touchpad-size}.py

%if %{without gtk4}
%{__sed} -i -e "/dependency('gtk4'/ s/'gtk4'/'gtk4-disabled'/" meson.build
%endif

%build
%meson \
	-Ddebug-gui=%{__true_false gui} \
	-Ddocumentation=%{__true_false doc} \
	-Dtests=%{__true_false tests} \
	-Dudev-dir=/lib/udev \
	-Dzshcompletiondir=%{zsh_compdir}

%meson_build

%if %{with tests}
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export PYTEST_PLUGINS=xdist
export FDO_CI_CONCURRENT="%{__jobs}"
%meson_test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%{?with_tests:%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/libinput-test-suite.1}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_bindir}/libinput
%attr(755,root,root) %{_libdir}/libinput.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libinput.so.10
%dir %{_libexecdir}/libinput
%attr(755,root,root) %{_libexecdir}/libinput/libinput-analyze
%attr(755,root,root) %{_libexecdir}/libinput/libinput-analyze-buttons
%attr(755,root,root) %{_libexecdir}/libinput/libinput-analyze-per-slot-delta
%attr(755,root,root) %{_libexecdir}/libinput/libinput-analyze-recording
%attr(755,root,root) %{_libexecdir}/libinput/libinput-analyze-touch-down-state
%attr(755,root,root) %{_libexecdir}/libinput/libinput-debug-events
%attr(755,root,root) %{_libexecdir}/libinput/libinput-debug-tablet
%attr(755,root,root) %{_libexecdir}/libinput/libinput-debug-tablet-pad
%attr(755,root,root) %{_libexecdir}/libinput/libinput-list-devices
%attr(755,root,root) %{_libexecdir}/libinput/libinput-list-kernel-devices
%attr(755,root,root) %{_libexecdir}/libinput/libinput-measure
%attr(755,root,root) %{_libexecdir}/libinput/libinput-measure-fuzz
%attr(755,root,root) %{_libexecdir}/libinput/libinput-measure-touchpad-pressure
%attr(755,root,root) %{_libexecdir}/libinput/libinput-measure-touchpad-size
%attr(755,root,root) %{_libexecdir}/libinput/libinput-measure-touchpad-tap
%attr(755,root,root) %{_libexecdir}/libinput/libinput-measure-touch-size
%attr(755,root,root) %{_libexecdir}/libinput/libinput-quirks
%attr(755,root,root) %{_libexecdir}/libinput/libinput-record
%attr(755,root,root) %{_libexecdir}/libinput/libinput-replay
%attr(755,root,root) %{_libexecdir}/libinput/libinput-test
%attr(755,root,root) /lib/udev/libinput-device-group
%attr(755,root,root) /lib/udev/libinput-fuzz-extract
%attr(755,root,root) /lib/udev/libinput-fuzz-to-zero
/lib/udev/rules.d/80-libinput-device-groups.rules
/lib/udev/rules.d/90-libinput-fuzz-override.rules
%dir %{_datadir}/libinput
%{_datadir}/libinput/*.quirks
%{_mandir}/man1/libinput.1*
%{_mandir}/man1/libinput-analyze.1*
%{_mandir}/man1/libinput-analyze-buttons.1*
%{_mandir}/man1/libinput-analyze-per-slot-delta.1*
%{_mandir}/man1/libinput-analyze-recording.1*
%{_mandir}/man1/libinput-analyze-touch-down-state.1*
%{_mandir}/man1/libinput-debug-events.1*
%{_mandir}/man1/libinput-debug-tablet.1*
%{_mandir}/man1/libinput-debug-tablet-pad.1*
%{_mandir}/man1/libinput-list-devices.1*
%{_mandir}/man1/libinput-list-kernel-devices.1*
%{_mandir}/man1/libinput-measure.1*
%{_mandir}/man1/libinput-measure-fuzz.1*
%{_mandir}/man1/libinput-measure-touchpad-pressure.1*
%{_mandir}/man1/libinput-measure-touchpad-size.1*
%{_mandir}/man1/libinput-measure-touchpad-tap.1*
%{_mandir}/man1/libinput-measure-touch-size.1*
%{_mandir}/man1/libinput-quirks.1*
%{_mandir}/man1/libinput-quirks-list.1*
%{_mandir}/man1/libinput-quirks-validate.1*
%{_mandir}/man1/libinput-record.1*
%{_mandir}/man1/libinput-replay.1*
%{_mandir}/man1/libinput-test.1*

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

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif

%files -n zsh-completion-%{name}
%defattr(644,root,root,755)
%{zsh_compdir}/_libinput
