%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define lib_name hurricane-driver

Name:           python-%{lib_name}
Version:        1.0.0
Release:        1%{?dist}
Summary:        This is the Python driver for Hurricane

Group:          Development/Languages
License:        BSD
URL:            http://gethurricane.org
# The tarball comes from here:
# http://github.com/%{name}/%{name}/tarball/v%{version}
# GitHub has layers of redirection and renames that make this a troublesome
# URL to include directly.
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Requires:       python

%description
The Hurricane Python driver includes libraries to communicate with
the Hurricane messaging system, encode/decode all Erlang terms,
and provides a WSGI server for use with Hurricane

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.markdown
%{python_sitelib}/%{lib_name}*
%{_bindir}/hurricane_wsgi_server


%changelog
* Fri Feb 24 2012  tavisto@tavisto.net 1.0.0-1
- Initial Package

