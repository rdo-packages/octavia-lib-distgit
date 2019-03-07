# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global library octavia-lib
%global module octavia_lib

%global common_desc A library to support Octavia provider drivers.

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    OpenStack Octavia library
License:    ASL 2.0
URL:        https://docs.openstack.org/octavia-lib/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n  python%{pyver}-%{library}
Summary:    OpenStack Octavia library
%{?python_provide:%python_provide python%{pyver}-%{library}}
# Required for tests
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-stestr
BuildRequires: python%{pyver}-testtools
BuildRequires: python%{pyver}-oslo-i18n
BuildRequires: python%{pyver}-oslo-log
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-six

Requires:   python%{pyver}-pbr
Requires:   python%{pyver}-oslo-i18n >= 3.15.3
Requires:   python%{pyver}-oslo-log >= 3.36.0
Requires:   python%{pyver}-oslo-serialization >= 2.28.1
Requires:   python%{pyver}-oslo-utils >= 3.33.0
Requires:   python%{pyver}-six >= 1.10.0

%description -n python%{pyver}-%{library}
%{common_desc}


%package -n python%{pyver}-%{library}-tests
Summary:    OpenStack Octavia library tests
%{?python_provide:%python_provide python%{pyver}-%{library}-tests}
Requires:   python%{pyver}-%{library} = %{version}-%{release}

%description -n python%{pyver}-%{library}-tests
%{common_desc}

This package contains the Octavia library test files.

%if 0%{?with_doc}
%package doc
Summary:    OpenStack Octavia library documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description doc
%{common_desc}

This package contains the documentation.
%endif

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Remove setuptools installed data_files
rm -rf %{buildroot}%{_datadir}/%{library}/LICENSE
rm -rf %{buildroot}%{_datadir}/%{library}/README.rst

%check
export OS_TEST_PATH='./octavia_lib/tests/unit'
export PATH=$PATH:%{buildroot}/usr/bin
export PYTHONPATH=$PWD
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{library}
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python%{pyver}-%{library}-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%changelog
