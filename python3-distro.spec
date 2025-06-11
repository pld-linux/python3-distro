#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	distro
Summary:	An OS platform information API
Summary(pl.UTF-8):	API do intermacji o platformie systemu operacyjnego
Name:		python3-%{module}
Version:	1.9.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/python-distro/distro/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	cec5819e1367f0349b3ef2b3804f1e84
URL:		https://github.com/python-distro/distro
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	sphinx-pdg-3 >= 2
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
distro provides information about the OS distribution it runs on, such
as a reliable machine-readable ID, or version information.

%description -l pl.UTF-8
distro udostępnia informacje o dystrybucji systemu operacyjnego, na
jakim działa, takie jak wiarygodny, czytelny dla maszyny identyfikator
albo informację o wersji.

%package apidocs
Summary:	API documentation for Python distro module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona distro
Group:		Documentation

%description apidocs
API documentation for Python distro module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona distro.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/distro
%doc CHANGELOG.md CONTRIBUTORS.md LICENSE README.md
%{py3_sitescriptdir}/distro
%{py3_sitescriptdir}/distro-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
