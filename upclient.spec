%define	name	upclient
%define	version	5.0
%define	release	%mkrel 1.b5.2

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Sends the uptime of the machine it's running on to a server
License:	GPL
Group:		System/Servers
Source0:	http://uptime.hexon.cx/download/%{name}-%{version}b5.tar.bz2
Source1:	%{name}.init.bz2
Source2:	%{name}.conf.bz2
URL:		http://uptime.hexon.cx/
Requires(post,preun):	rpm-helper

%description
Upclient is a small program that sends the uptime of the machine it's
running on to a server (ufo.its.kun.nl). This server collects all uptimes
and puts them in a table. To view the table, visit 
http://ufo.its.kun.nl/uptime/
Upclient causes almost no traffic (72bytes/minute), and won't give away
any other information than the uptime, load and the operating system
it's running on. But to make sure the program can't do any harm, don't run
it as root. All it needs, is access to /proc/uptime (and /proc/loadavg).
Upclient is totally freeware, so spread it around and make the list grow :)

%prep
%setup -q -n %{name}-%{version}b5

%build
(cd src; CFLAGS="$RPM_OPT_FLAGS" %make linux prefix=%{_prefix} sysconfdir=%{_sysconfdir})

%install
rm -rf $RPM_BUILD_ROOT
(cd src; %makeinstall)
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}
install -d $RPM_BUILD_ROOT{%{_initrddir},%{_localstatedir}/%{name},%{_var}/run/%{name}}
bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_initrddir}/%{name}
bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
chmod 755 $RPM_BUILD_ROOT{%{_initrddir},%{_sbindir}}/%{name}
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

%pre
%_pre_useradd %{name} %{_localstatedir}/%{name} /bin/bash

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc doc/* AUTHORS COPYING FAQ HISTORY HISTORY-BETA INSTALL README TODO TODO-flawfinder 
%{_sbindir}/%{name}
%config(noreplace) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_mandir}/man8/*
%dir %attr(-,upclient,upclient) %{_localstatedir}/%{name}
%dir %attr(-,upclient,upclient) %{_var}/run/%{name}

