%define		php_name	php%{?php_suffix}
%define		modname	cyrus
%define		status		stable
Summary:	%{modname} - eases manipulation of IMAP servers
Summary(pl.UTF-8):	%{modname} - ułatwienie manipulacji serwerami IMAP
Name:		%{php_name}-pecl-%{modname}
Version:	1.0
Release:	2
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	f0749ead144a8ddfd29d2961057d181b
URL:		http://pecl.php.net/package/cyrus/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	cyrus-imapd-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	php(core) >= 5.0.4
Obsoletes:	php-pear-%{modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extension which eases the manipulation of Cyrus IMAP servers.

In PECL status of this package is: %{status}.

%description -l pl.UTF-8
Rozszerzenie, które ułatwia manipulacje serwerami Cyrus IMAP.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
