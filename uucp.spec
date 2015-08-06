Summary:	GNU uucp
Summary(de.UTF-8):	GNU-uucp
Summary(es.UTF-8):	Uucp de la GNU
Summary(fr.UTF-8):	uucp de GNU
Summary(pl.UTF-8):	GNU uucp
Summary(pt_BR.UTF-8):	Uucp da GNU
Summary(ru.UTF-8):	GNU uucp
Summary(tr.UTF-8):	GNU uucp sistemi
Summary(uk.UTF-8):	GNU uucp
Name:		uucp
Version:	1.07
Release:	7
License:	GPL
Group:		Networking
Source0:	http://ftp.gnu.org/gnu/uucp/%{name}-%{version}.tar.gz
# Source0-md5:	64c54d43787339a7cced48390eb3e1d0
Source1:	%{name}.logrotate
Source2:	%{name}.inetd
Source3:	%{name}.crontab
Source4:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/%{name}-non-english-man-pages.tar.bz2
# Source4-md5:	47994a0f9fc7acaadc5cfff6b01f6728
Patch0:		%{name}-misc.patch
Patch1:		%{name}-debian.patch
Patch2:		%{name}-ac.patch
Patch3:		%{name}-pipe.patch
Patch4:		%{name}-no_libnsl.patch
Patch5:		format-security.patch
URL:		http://lists.cirr.com/cgi-bin/wilma/taylor-uucp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	texinfo
Requires:	crondaemon
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
UUCP is a Unix to Unix transfer mechanism. It is used primarily for
remote sites to download and upload email and news files to local
machines. If you didn't already know that, you probably don't need
this package installed. :-)

%description -l de.UTF-8
UUCP ist ein Unix-nach-Unix-Übertragungsprotokoll. Es wird vor allem
verwendet, um E-Mail- und News-Dateien von entfernten auf lokale
Rechner herunter- bzw. umgekehrt hochzuladen. Wie Sie wahrscheinlich
wissen, müssen Sie das Paket wahrscheinlich nicht installieren. :-)

%description -l es.UTF-8
UUCP es un mecanismo de transferencia de Unix para Unix. Se usa
primeramente en sitios remotos para hacer download y upload de
archivos de mail y news para máquinas locales. Si no lo sabias,
probablemente no necesitas de este paquete instalado. :-)

%description -l fr.UTF-8
UUCP est un mécanisme de transfert d'UNIX à UNIX. Il est
principalement utilisés par les sites de connexion pour télécharger ou
envoyer des courriers èlèctroniques et des nouvelles sur les machines
locales. Si vous ne saviez pas déja cela, vous n'avez probablement pas
besoin d'insatller ce package.

%description -l pl.UTF-8
UUCP (Unix to Unix Copy Protocol) jest jednym z podstawowych
protokołów systemu Linux. Używany jest przede wszystkim do wysyłania i
pobierania przesyłek newsów oraz poczty elektronicznej między
maszynami połączonymi np. przez modem.

%description -l pt_BR.UTF-8
UUCP é um mecanismo de transferência de Unix para Unix. Ele é usado
primeiramente em sites remotos para fazer download e upload de
arquivos de mail e news para máquinas locais. Se você não sabia disso,
você provavelmente não precisa deste pacote instalado. :-)

%description -l ru.UTF-8
UUCP - это механизм передачи файлов между UNIX-системами. В основном
используется для обмена почтой и телеконференциями между машинами.
Если вы этого не знали, вам этот пакет не нужен :-))

%description -l tr.UTF-8
UUCP bir Unix'ten Unix'e iletim mekanizmasıdır. Uzak sitelerden yerel
sisteme e-posta ve haber öbekleri aktarımı için kullanılır. Bunun ne
olduğunu bilmiyorsanız, büyük olasılıkla işinize de yaramayacaktır.
:-)

%description -l uk.UTF-8
UUCP - це механізм передачі файлів між UNIX-системами. Здебільшого
використовується для обміну поштою та телеконференціями між машинами.
Якщо ви цього не знали, вам цей пакет не потрібен :-))

%package server
Summary:	GNU uucp server
Summary(de.UTF-8):	GNU-uucp
Summary(fr.UTF-8):	uucp de GNU
Summary(pl.UTF-8):	Serwer GNU uucp
Group:		Networking
Requires:	%{name} = %{version}-%{release}

%description server
GNU uucp server.

%description server -l pl.UTF-8
Serwer GNU uucp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

find . -name "*.perlpath" | xargs rm -f

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-newconfigdir=%{_sysconfdir}/uucp \
	--with-oldconfigdir=%{_sysconfdir}/uucp/oldconfig

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/{lock/uucp,spool/{uucp,uucppublic}}
install -d $RPM_BUILD_ROOT/var/log/{uucp,archive/uucp}
install -d $RPM_BUILD_ROOT/etc/{sysconfig/rc-inetd,cron.d,logrotate.d}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/uucp/oldconfig

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	OWNER=$(id -u)

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/uucp
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/uucp
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.d/uucp
bzip2 -dc %{SOURCE4} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

# Create empty files
for n in Log Stats Debug; do
	touch $RPM_BUILD_ROOT/var/log/uucp/$n
done

for i in dial passwd port dialcode sys call; do
cat > $RPM_BUILD_ROOT%{_sysconfdir}/uucp/$i <<EOF
# This is an example of a $i file. This file have the syntax compatible
# with Taylor UUCP (not HDB, not anything else). Please check uucp
# documentation if you are not sure how Taylor config files are supposed to
# look like. Edit it as appropriate for your system.

# Everything after a '#' character is a comment.
EOF
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post server
%service -q rc-inetd reload

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun server
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO sample contrib

%attr(750,uucp,root) %dir %{_sysconfdir}/uucp
%attr(755,uucp,root) %dir %{_sysconfdir}/uucp/oldconfig

%attr(640,uucp,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/uucp/ca*
%attr(640,uucp,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/uucp/di*
%attr(640,uucp,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/uucp/p*
%attr(640,uucp,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/uucp/sys

%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/uucp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}

%attr(4554,uucp,uucp) %{_bindir}/cu
%attr(4554,uucp,uucp) %{_bindir}/uucp
%attr(755,root,root) %{_bindir}/uulog
%attr(4554,uucp,uucp) %{_bindir}/uuname
%attr(755,root,root) %{_bindir}/uupick
%attr(4554,uucp,uucp) %{_bindir}/uustat
%attr(755,root,root) %{_bindir}/uuto
%attr(4554,uucp,uucp) %{_bindir}/uux

%{_infodir}/uucp.*

%{_mandir}/man[18]/*
%lang(fi) %{_mandir}/fi/man[18]/*
%lang(ja) %{_mandir}/ja/man[18]/*
%lang(pl) %{_mandir}/pl/man[18]/*

%attr(755,uucp,uucp) %{_sbindir}/uuchk
%attr(4554,uucp,uucp) %{_sbindir}/uucico
%attr(755,uucp,uucp) %{_sbindir}/uuconv
%attr(755,root,root) %{_sbindir}/uusched
%attr(4554,uucp,uucp) %{_sbindir}/uuxqt

%attr(755,uucp,uucp) %dir /var/spool/uucppublic
%attr(755,uucp,uucp) %dir /var/spool/uucp

%attr(750,uucp,root) %dir /var/log/uucp
%attr(750,uucp,root) %dir /var/log/archive/uucp
%attr(750,uucp,root) %dir /var/lock/uucp
%attr(640,uucp,root) %config(noreplace) %verify(not md5 mtime size) /var/log/uucp/Debug
%attr(640,uucp,root) %config(noreplace) %verify(not md5 mtime size) /var/log/uucp/Log
%attr(640,uucp,root) %config(noreplace) %verify(not md5 mtime size) /var/log/uucp/Stats

%files server
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/uucp
