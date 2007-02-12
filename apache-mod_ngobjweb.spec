%define		mod_ngobjweb_makeflags		-v
%define		sope_version			4.5
%define		opengroupware.org_version	1.1
%define		datenightly			200601231102
%define		sopename			sope-mod_ngobjweb
%define 	apxs		/usr/sbin/apxs
%define		mod_name	ngobjweb
Summary:	mod_ngobjweb Apache module
Summary(pl.UTF-8):   Moduł Apacha mod_ngobjweb
Name:		apache-mod_%{mod_name}
Version:	r1203  
Release:	0.1
Vendor:		OpenGroupware.org
License:	LGPL
Group:		Development/Libraries
Source0:	http://download.opengroupware.org/nightly/sources/trunk/%{sopename}-trunk-%{version}-%{datenightly}.tar.gz
# Source0-md5:	7fba15c6f4a8ae86de057eb25e08a331
Source1:	%{name}.conf
Patch0:		%{name}-makefile.patch
URL:		http://www.softwarestudio.org/libical
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
BuildRequires:	autoconf
BuildRequires:	automake
Requires:	apache(modules-api) = %apache_modules_api
Requires:	ogo-environment
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
apache2 mod_ngobjweb adaptor (for OpenGroupware.org). Enables Apache
to handle HTTP requests for the SOPE application server.

%description -l pl.UTF-8
Moduł adaptera ngobjweb (dla OpenGroupware.org). Pozwala serwerowi
Apache obsługiwać żądania HTTP dla serwera aplikacji SOPE.

%prep
%setup -q -n sope-mod_ngobjweb
%patch0 -p1

%build
. %{_libdir}/GNUstep/System/Library/Makefiles/GNUstep.sh
%{__make} \
	CC="%{__cc}" \
	LD="%{__cc}" \
	apxs=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}
install mod_ngobjweb.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/88_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
