%{!?ruby_sitelib: %global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%define lib_name hurricane-driver

Name:           rubygem-%{lib_name}
Version:        1.0.0
Release:        1%{?dist}
Summary:        This is the Ruby driver for Hurricane

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
BuildRequires:  ruby ruby-devel
Requires:       ruby(abi) = 1.8

%description
The Hurricane Ruby driver includes libraries to communicate with
the Hurricane messaging system, encode/decode all Erlang terms,
and provides a WSGI server for use with Hurricane

%prep
%setup -q


%build
export CFLAGS="%{optflags}"


%install
rm -rf %{buildroot}

 
%check


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README.markdown
%{ruby_sitelib}/%{lib_name}*


%changelog
* Fri Feb 24 2012 tavisto@tavisto.net 1.0.0-1
- Initial Package

