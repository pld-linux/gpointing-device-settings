Summary:	GUI tool for setting pointing device
Name:		gpointing-device-settings
Version:	1.5.1
Release:	1
License:	LGPL v3+
Group:		X11/Applications
Source0:	http://jaist.dl.sourceforge.jp/gsynaptics/45812/%{name}-%{version}.tar.gz
# Source0-md5:	1d1491473df8eabca3c15c997a975d7f
Patch0:		%{name}-%{version}-plugin.patch
Patch1:		%{name}-%{version}-reboot.patch
Patch2:		%{name}-%{version}-gsd-crash.patch
Patch3:		%{name}-%{version}-gtk22.patch
Patch4:		%{name}-%{version}-crash.patch
URL:		http://live.gnome.org/GPointingDeviceSettings
BuildRequires:	gnome-settings-daemon-devel
BuildRequires:	gtk+2-devel >= 2.14.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	pkgconfig >= 0.9.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GPointingDeviceSettings is a GUI tool for setting pointing device such
as TrackPoint or Touchpad. Each UI can be written as dynamic loadable
module, so a third party can add its own UI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
#%%{__autoconf}
#%%{__autoheader}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/{gnome-settings-daemon*/*.la,gpointing-device-settings/module/*.la,*.la}

%find_lang %{name}

%post
/sbin/ldconfig
%gconf_schema_install %{name}_gnome_settings_daemon.schemas
%update_desktop_database_post

%preun
%gconf_schema_uninstall %{name}_gnome_settings_daemon.schemas

%postun
/sbin/ldconfig
%update_desktop_database_postun

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog MAINTAINERS NEWS TODO
%{_sysconfdir}/gconf/schemas/%{name}_gnome_settings_daemon.schemas
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/module
%attr(755,root,root) %{_libdir}/%{name}/module/*.so
%attr(755,root,root) %{_libdir}/gnome-settings-daemon*/*.so
%{_libdir}/gnome-settings-daemon*/pointing-device.gnome-settings-plugin
%attr(755,root,root) %{_libdir}/libgpds.so.0.1.0
%attr(755,root,root) %ghost %{_libdir}/libgpds.so.0
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_mandir}/man1/%{name}.1*
