# TODO:
# - rpmbuild switches for using mysql/postgresql?
# - move muggle.state* files away from /etc

%define _default_patch_fuzz 2

%define pname     muggle
%define plugindir %(vdr-config --plugindir  2>/dev/null || echo ERROR)
%define audiodir  %(vdr-config --audiodir   2>/dev/null || echo ERROR)
%define configdir %(vdr-config --configdir  2>/dev/null || echo ERROR)
%define cachedir  %(vdr-config --cachedir   2>/dev/null || echo ERROR)
%define vardir    %(vdr-config --vardir     2>/dev/null || echo ERROR)
%define vdr_user  %(vdr-config --user       2>/dev/null || echo ERROR)
%define apiver    %(vdr-config --apiversion 2>/dev/null || echo ERROR)

Name:           vdr-muggle
Version:        0.1.12
Release:        4%{?dist}
Summary:        Media juggle plugin for VDR

Group:          Applications/Multimedia
License:        GPL+
URL:            http://www.selbstgetippt.de/selbstgetippt/Muggle.html
Source0:        http://downloads.sourceforge.net/vdr-muggle/%{name}-%{version}.tgz
Source1:        %{name}.conf
Patch0:         %{name}-0.1.12-gcc43.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  taglib-devel
BuildRequires:  libmad-devel
BuildRequires:  flac-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libsndfile-devel
BuildRequires:  sqlite-devel >= 3
BuildRequires:  vdr-devel >= 1.3.47
BuildRequires:  sed >= 3.95
Requires:       vdr(abi) = %{apiver}
# For muggle-image-convert:
Requires(hint): file
Requires(hint): mjpegtools
Requires(hint): netpbm-progs

%description
The media juggle plugin allows the management of arbitrary media files
via a database using VDR and its OSD.


%prep
%setup -q -n %{pname}-%{version}
%patch0
sed -i -e 's|"/tmp"|"%{cachedir}/muggle"|' mg_setup.c
f=HISTORY ; iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
sed -e 's|/var/lib/vdr/muggle|%{vardir}/muggle|' \
  -e 's|/srv/audio|%{audiodir}|' < %{SOURCE1} > muggle.conf


%build
make %{?_smp_mflags} LIBDIR=. VDRDIR=%{_libdir}/vdr MUSICDIR="%{audiodir}" \
  HAVE_SQLITE=1 HAVE_VORBISFILE=1 HAVE_FLAC=1 HAVE_SNDFILE=1


%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{plugindir}/bin
install -pm 755 libvdr-%{pname}.so.%{apiver} $RPM_BUILD_ROOT%{plugindir}
install -pm 755 scripts/muggle-image-convert $RPM_BUILD_ROOT%{plugindir}/bin

install -Dpm 644 muggle.conf \
  $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr-plugins.d/%{pname}.conf

install -Dpm 755 mugglei $RPM_BUILD_ROOT%{_bindir}/mugglei

install -dm 755 $RPM_BUILD_ROOT%{vardir}/muggle
touch $RPM_BUILD_ROOT%{vardir}/muggle/GiantDisc.sqlite

install -dm 755 $RPM_BUILD_ROOT%{configdir}/plugins/muggle
touch $RPM_BUILD_ROOT%{configdir}/plugins/muggle/muggle.state{,.old}

install -dm 755 $RPM_BUILD_ROOT%{cachedir}/muggle


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING HISTORY menu.txt README README.sqlite TODO
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/%{pname}.conf
%{_bindir}/mugglei
%{plugindir}/libvdr-%{pname}.so.%{apiver}
%{plugindir}/bin/muggle-image-convert
%defattr(-,%{vdr_user},root,-)
%{cachedir}/muggle/
%dir %{vardir}/muggle/
%ghost %{vardir}/muggle/GiantDisc.sqlite
%dir %{configdir}/plugins/muggle/
%ghost %{configdir}/plugins/muggle/muggle.state*


%changelog
* Tue Aug 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.1.12-4
- added _default_patch_fuzz define

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.1.12-3
- rebuild

* Tue Apr  8 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.1.12-2
- Patch to fix build with GCC 4.3's cleaned up C++ headers.
- Rebuild for VDR 1.6.0.

* Fri Jan  4 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.1.12-1
- 0.1.12.

* Sun Dec 30 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.1.11-2
- Patch for FLAC 1.1.3+ compatibility.
- License: GPL+
- Update URLs.

* Thu May 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.1.11-1
- 0.1.11.

* Sat Apr 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.1.10-1
- 0.1.10, most patches applied upstream.
- Adjust for VDR 1.3.47+, require versioned vdr(abi).

* Sat Mar 18 2006 Thorsten Leemhuis <fedora at leemhuis.info>- 0.1.9-1.lvn.7
- drop 1.lvn from release

* Wed Mar  1 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-1.lvn.7
- Rebuild for VDR 1.3.44.

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Sun Feb 19 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-1.lvn.6
- Rebuild for VDR 1.3.43.

* Sun Feb  5 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-1.lvn.5
- Rebuild for VDR 1.3.42.

* Sun Jan 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-1.lvn.4
- Fix button translations with VDR >= 1.3.38.
- Rebuild for VDR 1.3.40.

* Sun Jan 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-1.lvn.3
- Rebuild for VDR 1.3.39.

* Sun Jan  8 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-1.lvn.2
- Rebuild/patch for VDR 1.3.38.
- Fix build with gcc 4.1.

* Wed Nov 30 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-1.lvn.1
- First livna release.

* Mon Nov 28 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-0.4
- Rebuild for VDR 1.3.37.

* Sun Nov  6 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-0.3
- Rebuild for VDR 1.3.36.

* Tue Nov  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-0.2
- Rebuild for VDR 1.3.35.

* Wed Oct 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.9-0.1
- 0.1.9.

* Mon Oct  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.8-0.8
- Rebuild for VDR 1.3.34.

* Sun Sep 25 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.8-0.7
- Rebuild for VDR 1.3.33.

* Sun Sep 11 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.8-0.6
- Rebuild for VDR 1.3.32.

* Sun Aug 28 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.8-0.5
- Rebuild for VDR 1.3.31.

* Sat Aug 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.8-0.4
- Patch to add loading of DeleteStaleReferences from config.

* Sun Aug 21 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.8-0.3
- Switch to SQLite backend.

* Sun Aug  7 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.8-0.2
- Move plugins.d snippet according to VDR 1.3.28 packages.

* Sun Jul 31 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.8-0.1
- 0.1.8.

* Thu Jun  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.1.7-0.1
- First build.
