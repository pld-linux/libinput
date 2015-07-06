#
# Conditional build:
%bcond_with	gui		# event-gui (noinst as of 0.4.0)
%bcond_with	static_libs	# static library
#
Summary:	Input device library
Summary(pl.UTF-8):	Biblioteka urządzeń wejściowych
Name:		libinput
Version:	0.19.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://www.freedesktop.org/software/libinput/%{name}-%{version}.tar.xz
# Source0-md5:	ddb2c98687c2b9766a9757fd6ec90753
URL:		http://www.freedesktop.org/wiki/Software/libinput/
%{?with_gui:BuildRequires:	cairo-devel}
BuildRequires:	check-devel >= 0.9.10
BuildRequires:	doxygen >= 1.6.0
%{?with_gui:BuildRequires:	glib2-devel >= 2.0}
BuildRequires:	graphviz >= 2.26.0
%{?with_gui:BuildRequires:	gtk+3-devel >= 3.0}
BuildRequires:	libevdev-devel >= 0.4
BuildRequires:	mtdev-devel >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	udev-devel
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

%description apidocs
API documentation for libinput library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libinput.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
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
%doc COPYING README.txt
%attr(755,root,root) %{_bindir}/libinput-debug-events
%attr(755,root,root) %{_bindir}/libinput-list-devices
%attr(755,root,root) %{_libdir}/libinput.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libinput.so.10
%attr(755,root,root) /lib/udev/libinput-device-group
/lib/udev/rules.d/80-libinput-device-groups.rules
/lib/udev/hwdb.d/90-libinput-model-quirks.hwdb
/lib/udev/rules.d/90-libinput-model-quirks.rules
%{_mandir}/man1/libinput-debug-events.1*
%{_mandir}/man1/libinput-list-devices.1*

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
