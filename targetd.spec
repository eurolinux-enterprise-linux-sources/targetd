Name:           targetd
License:        GPLv3
Group:          System Environment/Libraries
Summary:        Service to make storage remotely configurable
Version:        0.8.6
Release:        1%{?dist}
URL:            https://github.com/open-iscsi/targetd
Source:         https://github.com/open-iscsi/targetd/releases/download/v%{version}/targetd-%{version}.tar.gz
Source1:        targetd.service
Source2:        targetd.yaml
BuildArch:      noarch
BuildRequires:  systemd, python-devel
Requires:       python-rtslib PyYAML python-setproctitle
Requires:       lvm2-python-libs >= 2.02.99, nfs-utils, btrfs-progs
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description
targetd turns the machine into a remotely-configurable storage appliance.
It supports an HTTP/jsonrpc-2.0 interface to let a remote
administrator allocate volumes from an LVM volume group, and export
those volumes over iSCSI.

%prep
%setup -q

%build
%{__python2} setup.py build
gzip --stdout targetd.8 > targetd.8.gz

%install
mkdir -p %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/target/
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/targetd.service
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/target/targetd.yaml
install -m 644 targetd.8.gz %{buildroot}%{_mandir}/man8/
%{__python2} setup.py install --skip-build --root %{buildroot}

%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable targetd.service > /dev/null 2>&1 || :
    /bin/systemctl stop targetd.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart targetd.service >/dev/null 2>&1 || :
fi

%files
%{_bindir}/targetd
%{_unitdir}/targetd.service
%{python2_sitelib}/*
%doc LICENSE README.md API.md client
%{_mandir}/man8/targetd.8.gz
%config(noreplace) %{_sysconfdir}/target/targetd.yaml

%changelog
* Thu Apr 27 2017 Tony Asleson <tasleson@redhat.com> - 0.8.6-1
- Update to latest version

* Fri Feb 17 2017 Tony Asleson <tasleson@redhat.com> - 0.8.5-1
- Update to latest version
- Be explicit in using python2

* Mon Feb 10 2014 Andy Grover <agrover@redhat.com> - 0.7.1-1
- Upddate to latest version
- Update service file for switching dependency to rtslib from targetcli

* Mon Jan 27 2014 Andy Grover <agrover@redhat.com> - 0.6.1-3
- Update Source/URL

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.6.1-2
- Mass rebuild 2013-12-27

* Thu Aug 8 2013 Andy Grover <agrover@redhat.com> 0.6.1-1
- Update to latest version, make needed changes
- Drop patches:
  * require-password.patch
  * use-std-ssl.patch
- Change requires from python-lvm to lvm2-python-libs

* Mon Aug  5 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.3.1-7
- Add systemd to BuildReq to fix FTBFS

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 16 2013 Andy Grover <agrover@redhat.com> - 0.3.1-5
- Update require-password.patch
- Change target.yaml to not include a commented-out default password

* Tue Apr 16 2013 Andy Grover <agrover@redhat.com> - 0.3.1-4
- Remove dependency on python-tlslite

* Mon Apr 15 2013 Andy Grover <agrover@redhat.com> - 0.3.1-3
- Add patch
  * use-std-ssl.patch
  * require-password.patch

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Andy Grover <agrover@redhat.com> - 0.3.1-1
- New upstream version

* Mon Sep 24 2012 Andy Grover <agrover@redhat.com> - 0.3-1
- New upstream version

* Fri Sep 7 2012 Andy Grover <agrover@redhat.com> - 0.2.4-1
- New upstream version

* Tue Aug 28 2012 Andy Grover <agrover@redhat.com> - 0.2.3-1
- New upstream version
- Add new dependency python-tlslite

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Andy Grover <agrover@redhat.com> - 0.2.2-2
- Add proper pkg requires

* Mon Jun 25 2012 Andy Grover <agrover@redhat.com> - 0.2.2-1
- Initial packaging
