Name:           hurricane
Version:        0.2.1
Release:        1%{?dist}
Summary:        A scalable, extensible, distributed messaging system. 

Group:      
License:        BSD      
URL:           http://gethurricane.org 
Source0:       https://github.com/icheishvili/hurricane/tarball/v%{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       erlang
Requires:       erlang-mochiweb 

%description
A scalable, extensible, distributed messaging system.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc

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
* Tue Feb 21 2012 Tavis Aitken <tavisto@tavisto.net> - 0.2.1-1
- Initial package
