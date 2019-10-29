%ifarch %{arm} %{armx}
%define _disable_lto 1
%endif

%define         major 3
%define         libname %mklibname %{name}
%define         devel %mklibname %{name} -d

Name:     dav1d
Version:	0.5.1
Release:	2
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
# As of 0.5.0 release both arm failed to build on gcc due to a lot of issues like:
#error: undefined reference to 'checkasm_fail_func'
#/src/arm/64/ipred.S:876: error: undefined reference to 'dav1d_sm_weights'
# Using clang gives, error: unknown directive .endfunc
#<instantiation>:55:1: note: while in macro instantiation endfunc
# Solution is disable LTO and use Clanh for ARM.
#--
#ARM use GCC because Clang failed to build.
#ifarch %{arm} %{armx}
#global ldflags %{ldflags} -fuse-ld=gold
#export CC=gcc
#export CXX=g++
#endif

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
%{_libdir}/libdav1d.so.%{major}*
