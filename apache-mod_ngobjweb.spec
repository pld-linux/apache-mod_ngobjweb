# TODO:
# - mv SPECS/{apache-mod-ngobjweb.spec,apache-mod_ngobjweb.spec},v (if it's apache module)
# - why Name and install dir is sope-* ???
# - strange /var/*/*.so and /usr/local paths in generated OGo.conf

%define		mod_ngobjweb_makeflags		-v
%define		sope_version			4.3
%define		opengroupware.org_version	1.0a

Summary:	mod_ngobjweb apache module
Summary(pl):	Modu³ Apacha mod_ngobjweb
Name:		sope-mod_ngobjweb
Version:	3.15
Release:	1
Vendor:		OpenGroupware.org
License:	LGPL
Group:		Development/Libraries
Source0:	http://download.opengroupware.org/sources/trunk/sope-mod_ngobjweb-trunk-latest.tar.gz
URL:		http://www.softwarestudio.org/libical
Requires: 	apache >= 2.0.40
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	apache-devel
BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
Requires:	apache >= 2.0.40
Requires:	ogo-environment
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
apache2 mod_ngobjweb adaptor (for OpenGroupware.org). Enables Apache
to handle HTTP requests for the SOPE application server.

%description -l pl
Modu³ adaptera ngobjweb (dla OpenGroupware.org). Pozwala serwerowi
Apache obs³ugiwaæ ¿±dania HTTP dla serwera aplikacji SOPE.

%prep
%setup -n sope-mod_ngobjweb

%build
. /usr/lib/GNUstep/System/Library/Makefiles/GNUstep.sh
export PATH=$PATH:%{_sbindir}
%{__make} %{mod_ngobjweb_makeflags} \
	apxs=/usr/sbin/apxs \
	HTTPD=/usr/sbin/httpd \
	APXS_INCLUDE_DIRS="-I%{_includedir}/apr -I%{_includedir}/apr-util -I%{_includedir}/apache"

%install
rm -rf $RPM_BUILD_ROOT
export PATH=$PATH:%{_sbindir}
install -d $RPM_BUILD_ROOT%{_libdir}/sope-%{sope_version}

install mod_ngobjweb.so $RPM_BUILD_ROOT%{_libdir}/sope-%{sope_version}/mod_ngobjweb.so

install -d $RPM_BUILD_ROOT%{_var}/lib/opengroupware.org

echo "#this file contains the apache/httpd configuration for OpenGroupware.org
#it should be included from within your default httpd.conf ala:
#`include OGo.conf`
#(or copy it into the dir where additonal configs end up)
#
LoadModule ngobjweb_module %{_var}/lib/opengroupware.org/mod_ngobjweb.so
#
Alias /OpenGroupware10a.woa/WebServerResources/ %{_prefix}/local/share/opengroupware.org-%{opengroupware.org_version}/www/
Alias /ArticleImages %{_var}/lib/opengroupware.org/news
#
<LocationMatch "^/OpenGroupware*">
  SetAppPort 20000
  SetHandler ngobjweb-adaptor
</LocationMatch>
#
<LocationMatch "^/zidestore/*">
SetHandler ngobjweb-adaptor
SetAppPort 21000
</LocationMatch>
#
<LocationMatch "^/RPC2*">
SetHandler ngobjweb-adaptor
SetAppPort 22000
</LocationMatch>
" > $RPM_BUILD_ROOT%{_var}/lib/opengroupware.org/OGo.conf

%clean
rm -rf $RPM_BUILD_ROOT

# NOT THIS WAY
#%post
#cp %{_var}/lib/opengroupware.org/OGo.conf /etc/httpd/httpd.conf/88_OGo.conf

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/httpd.conf/88_OGo.conf
%attr(755,root,root) %{_libdir}/sope-%{sope_version}/mod_ngobjweb.so
%config(noreplace) %verify(not md5 mtime size) %{_var}/lib/opengroupware.org/OGo.conf
