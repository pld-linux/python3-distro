#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	distro
Summary:	An OS platform information API
Name:		python-%{module}
Version:	1.4.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/nir0s/%{module}/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	ada22d75b32a4056ed13f32b9d986a2d
URL:		https://github.com/nir0s/distro
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.713
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-test
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-test
%endif
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
distro provides information about the OS distribution it runs on, such
as a reliable machine-readable ID, or version information.

%package -n python3-%{module}
Summary:	Parse human-readable date/time strings in Python
Group:		Libraries/Python

%description -n python3-%{module}
distro provides information about the OS distribution it runs on, such
as a reliable machine-readable ID, or version information.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE
%doc CONTRIBUTORS.md CHANGELOG.md README.md
%{py_sitescriptdir}/%{module}.*
%{py_sitescriptdir}/%{module}-%{version}-*.egg-info

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/distro
%doc LICENSE
%doc CONTRIBUTORS.md CHANGELOG.md README.md
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/%{module}*.py[co]
%{py3_sitescriptdir}/%{module}*.egg-info
%endif
