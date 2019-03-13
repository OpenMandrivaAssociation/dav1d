%define         libname %mklibname %{name}
%define         devel %mklibname %{name} -d

Name:     dav1d
Version:  0.2.1
Release:  1
License:  BSD
Group:    System/Libraries
Summary:  AV1 cross-platform Decoder
URL:      https://code.videolan.org/videolan/dav1d
Source0:  https://code.videolan.org/videolan/dav1d/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  doxygen
BuildRequires:  nasm
BuildRequires:  ninja
BuildRequires:  meson

%description
dav1d is a new AV1 cross-platform Decoder, open-source, and focused on speed and correctness.

%package -n %{libname}
Summary:        Library files for dav1d
Group:          System/Libraries

%description -n %{libname}
Library files for dav1d, the AV1 cross-platform Decoder

%package -n %{devel}
Summary:        Development files for dav1d
Group:          System/Libraries
Requires:       %{libname} = %{version}-%{release}

%description -n %{devel}
Development files for dav1d, the AV1 cross-platform Decoder.

%prep
%setup -q

%build
#ARM use GCC because Clang failed to build.
%ifarch %{arm} %{armx}
export CC=gcc
export CXX=g++
%endif

%meson
%ninja -C build

%install
%ninja_install -C build

%files
%license COPYING
%doc CONTRIBUTING.md README.md THANKS.md NEWS
%{_bindir}/%{name}

%files -n %{devel}
%{_includedir}/%{name}/
%{_libdir}/libdav1d.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n %{libname}
%{_libdir}/libdav1d.so*
