Summary:	Input device library
Name:		libinput
Version:	0.1.0
Release:	1
License:	MIT
URL:		http://www.freedesktop.org/wiki/Software/libinput/
Source0:	http://www.freedesktop.org/software/libinput/%{name}-%{version}.tar.xz
# Source0-md5:	f5d794beb5228353f480d15a058e1885
Group:		Libraries
BuildRequires:	libevdev-devel
BuildRequires:	mtdev-devel
BuildRequires:	udev-devel

%description
libinput is a library that handles input devices for display servers
and other applications that need to directly deal with input devices.

It provides device detection, device handling, input device event
processing and abstraction so minimize the amount of custom input code
the user of libinput need to provide the common set of functionality
that users expect.

%package        devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure \
	--disable-static \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %ghost %{_libdir}/libinput.so.0
%attr(755,root,root) %{_libdir}/libinput.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/libinput.h
%attr(755,root,root) %{_libdir}/libinput.so
%{_pkgconfigdir}/libinput.pc
