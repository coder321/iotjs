Name: iotjs
Version: 1.0.0
Release: 0
Summary: Platform for Internet of Things with JavaScript
Group: Network & Connectivity
License: Apache-2.0
URL: https://www.iotjs.net/
Source:     %{name}-%{version}.tar.gz
Source1:    %{name}.pc.in
Source1001: %{name}.manifest
ExclusiveArch: %arm

BuildRequires: python
BuildRequires: cmake
BuildRequires: glibc-static
#BuildRequires: aul
BuildRequires: pkgconfig(appcore-agent)
BuildRequires: pkgconfig(capi-appfw-service-application)
BuildRequires: pkgconfig(capi-appfw-app-common)
#BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(capi-appfw-application)
BuildRequires: pkgconfig(capi-system-peripheral-io)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(capi-appfw-app-control)
BuildRequires: pkgconfig(bundle)
#BuildRequires: pkgconfig(st_things_sdkapi)

#for https
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel

Requires(postun): /sbin/ldconfig
Requires(post): /sbin/ldconfig

%description
Platform for Internet of Things with JavaScript

# Initialize the variables
%{!?build_mode: %define build_mode release}
%{!?external_build_options: %define external_build_options %{nil}}

%package service
Summary: Development files for %{name}
Group: Network & Connectivity/Service
Requires: %{name} = %{version}-%{release}

%description service
The %{name}-service package contains service iotjs files for
developing applications that use %{name}.

%package devel
Summary: Header files for %{name}
Group: Network & Connectivity/Service
Requires: %{name} = %{version}-%{release}

%description devel
Development libraries for %{name}

%prep
%setup -q -c
chmod g-w %_sourcedir/*
cat LICENSE
cp %{SOURCE1001} .

%build
V=1 VERBOSE=1 ./tools/build.py \
  --clean \
  --buildtype=%{build_mode} \
  --profile=test/profiles/tizen.profile \
  --target-arch=noarch \
  --target-os=tizen \
  --target-board=rpi3 \
  --external-lib=capi-system-peripheral-io \
  --external-lib=capi-appfw-app-common \
  --external-lib=dlog \
  --external-lib=bundle \
  --external-lib=capi-appfw-app-control \
  --external-lib=appcore-agent \
  --external-lib=pthread \
  --external-lib=curl \
  --external-include-dir=/usr/include/dlog/ \
  --external-include-dir=/usr/include/appcore-agent/ \
  --external-include-dir=/usr/include/appfw/ \
  --external-include-dir=/usr/include/glib-2.0/ \
  --external-include-dir=/usr/lib/glib-2.0/include/ \
  --compile-flag=-D__TIZEN__ \
  --compile-flag=-DENABLE_DEBUG_LOG \
  --create-shared-lib \
  --no-init-submodule \
  --no-parallel-build \
  %{external_build_options}
# --external-lib=sdkapi \

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}/iotjs
mkdir -p %{buildroot}%{_libdir}/iotjs
mkdir -p %{buildroot}%{_libdir}/pkgconfig


cp ./build/noarch-tizen/%{build_mode}/bin/iotjs %{buildroot}%{_bindir}/
cp ./build/noarch-tizen/%{build_mode}/lib/*.so %{buildroot}%{_libdir}/

cp ./src/platform/tizen/iotjs_tizen_service_app.h %{buildroot}%{_includedir}/iotjs
cp ./config/tizen/packaging/%{name}.pc.in %{buildroot}/%{_libdir}/pkgconfig/%{name}.pc

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%manifest config/tizen/packaging/%{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/*

%files devel
%manifest config/tizen/packaging/%{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libiotjs.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*
