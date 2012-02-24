%define debug_package %{nil}

Name:           hurricane
Version:        0.2.3
Release:        1%{?dist}
Summary:        A scalable, extensible, distributed messaging system. 

Group:          System Environment/Daemons
License:        BSD
URL:           http://gethurricane.org
# The tarball comes from here:
# http://github.com/%{name}/%{name}/tarball/v%{version}
# GitHub has layers of redirection and renames that make this a troublesome
# URL to include directly.
Source0:        %{name}-%{version}.tar.gz
Source1:        hurricane-init.d.sh
Source2:        hurricane-logrotate.conf
Source3:        sysconfig-hurricane.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  erlang
Requires:       erlang
Requires:       erlang-mochiweb

Requires(post): chkconfig initscripts
Requires(pre):  chkconfig initscripts
Requires(pre):  shadow-utils

%description
A scalable, extensible, distributed messaging system.

%package devel
BuildArch:  noarch
Summary:    Source files for development

%description devel
Source files for development


%prep
%setup -q

%build
make all

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}/erlang/lib/%{name}-%{version}
mkdir -p %{buildroot}/%{_libdir}/erlang/lib/%{name}-%{version}/ebin
%{__install} -p -m 644 ebin/* %{buildroot}/%{_libdir}/erlang/lib/%{name}-%{version}/ebin/

# Source for devel
mkdir -p %{buildroot}/%{_libdir}/erlang/lib/%{name}-%{version}/src
%{__install} -p -m 644 erl_modules/* %{buildroot}/%{_libdir}/erlang/lib/%{name}-%{version}/src/

mkdir -p %{buildroot}/%{_bindir}
%{__install} -p -m 755 run.escript %{buildroot}%{_bindir}/%{name}

# Sample configs
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__install} -D -m 644 examples/example.config %{buildroot}%{_sysconfdir}/%{name}/example.config

# init
%{__mkdir} -p %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}

# logs
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# sysconfig
%{__mkdir} -p %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%{__mkdir} -p %{buildroot}%{_localstatedir}/run/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_libdir}/erlang/lib/%{name}-%{version}
%dir %{_libdir}/erlang/lib/%{name}-%{version}/ebin
%{_libdir}/erlang/lib/%{name}-%{version}/ebin/*
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/rc.d/init.d/%{name}
%dir %{_localstatedir}/run/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%doc README.markdown

%files devel
%dir %{_libdir}/erlang/lib/%{name}-%{version}/src/
%{_libdir}/erlang/lib/%{name}-%{version}/src/*


%post
/sbin/chkconfig --add hurricane

%pre
# create hurricane group
if ! getent group hurricane >/dev/null; then
        groupadd -r hurricane
fi

# create hurricane user
if ! getent passwd hurricane >/dev/null; then
        useradd -r -g hurricane -d %{_javadir}/%{name} \
            -s /sbin/nologin -c "You know, for search" hurricane
fi


%preun
if [ $1 -eq 0 ]; then
  /sbin/service hurricane stop >/dev/null 2>&1
  /sbin/chkconfig --del hurricane
fi


%changelog
* Thu Feb 23 2012 tavisto@tavisto.net 0.2.3-1
- Added make file to ship only .beam files and added a devel subpackage for the source files.

* Tue Feb 21 2012 Tavis Aitken <tavisto@tavisto.net> - 0.2.2-1
- Initial package
