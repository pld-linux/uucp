Summary:	GNU uucp
Summary(de):	GNU-uucp
Summary(es):	Uucp de la GNU
Summary(fr):	uucp de GNU
Summary(pl):	GNU uucp
Summary(pt_BR):	Uucp da GNU
Summary(ru):	GNU uucp
Summary(tr):	GNU uucp sistemi
Summary(uk):	GNU uucp
Name:		uucp
Version:	1.07
Release:	3
License:	GPL
Group:		Networking
Source0:	ftp://ftp.gnu.org/pub/gnu/uucp/%{name}-%{version}.tar.gz
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
URL:		http://lists.cirr.com/cgi-bin/wilma/taylor-uucp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
UUCP is a Unix to Unix transfer mechanism. It is used primarily for
remote sites to download and upload email and news files to local
machines. If you didn't already know that, you probably don't need
this package installed. :-)

%description -l de
UUCP ist ein Unix-nach-Unix-Übertragungsprotokoll. Es wird vor allem
verwendet, um E-Mail- und News-Dateien von entfernten auf lokale
Rechner herunter- bzw. umgekehrt hochzuladen. Wie Sie wahrscheinlich
wissen, müssen Sie das Paket wahrscheinlich nicht installieren. :-)

%description -l es
UUCP es un mecanismo de transferencia de Unix para Unix. Se usa
primeramente en sitios remotos para hacer download y upload de
archivos de mail y news para máquinas locales. Si no lo sabias,
probablemente no necesitas de este paquete instalado. :-)

%description -l fr
UUCP est un mécanisme de transfert d'UNIX à UNIX. Il est
principalement utilisés par les sites de connexion pour télécharger ou
envoyer des courriers èlèctroniques et des nouvelles sur les machines
locales. Si vous ne saviez pas déja cela, vous n'avez probablement pas
besoin d'insatller ce package.

%description -l pl
UUCP (Unix to Unix Copy Protocol) jest jednym z podstawowych
protoko³ów systemu Linux. U¿ywany jest przede wszystkim do wysy³ania i
pobierania przesy³ek newsów oraz poczty elektronicznej miêdzy maszynami
po³±czonymi np. przez modem.

%description -l pt_BR
UUCP é um mecanismo de transferência de Unix para Unix. Ele é usado
primeiramente em sites remotos para fazer download e upload de
arquivos de mail e news para máquinas locais. Se você não sabia disso,
você provavelmente não precisa deste pacote instalado. :-)

%description -l ru
UUCP - ÜÔÏ ÍÅÈÁÎÉÚÍ ÐÅÒÅÄÁÞÉ ÆÁÊÌÏ× ÍÅÖÄÕ UNIX-ÓÉÓÔÅÍÁÍÉ. ÷ ÏÓÎÏ×ÎÏÍ
ÉÓÐÏÌØÚÕÅÔÓÑ ÄÌÑ ÏÂÍÅÎÁ ÐÏÞÔÏÊ É ÔÅÌÅËÏÎÆÅÒÅÎÃÉÑÍÉ ÍÅÖÄÕ ÍÁÛÉÎÁÍÉ.
åÓÌÉ ×Ù ÜÔÏÇÏ ÎÅ ÚÎÁÌÉ, ×ÁÍ ÜÔÏÔ ÐÁËÅÔ ÎÅ ÎÕÖÅÎ :-))

%description -l tr
UUCP bir Unix'ten Unix'e iletim mekanizmasýdýr. Uzak sitelerden yerel
sisteme e-posta ve haber öbekleri aktarýmý için kullanýlýr. Bunun ne
olduðunu bilmiyorsanýz, büyük olasýlýkla iþinize de yaramayacaktýr.
:-)

%description -l uk
UUCP - ÃÅ ÍÅÈÁÎ¦ÚÍ ÐÅÒÅÄÁÞ¦ ÆÁÊÌ¦× Í¦Ö UNIX-ÓÉÓÔÅÍÁÍÉ. úÄÅÂ¦ÌØÛÏÇÏ
×ÉËÏÒÉÓÔÏ×Õ¤ÔØÓÑ ÄÌÑ ÏÂÍ¦ÎÕ ÐÏÛÔÏÀ ÔÁ ÔÅÌÅËÏÎÆÅÒÅÎÃ¦ÑÍÉ Í¦Ö ÍÁÛÉÎÁÍÉ.
ñËÝÏ ×É ÃØÏÇÏ ÎÅ ÚÎÁÌÉ, ×ÁÍ ÃÅÊ ÐÁËÅÔ ÎÅ ÐÏÔÒ¦ÂÅÎ :-))

%package server
Summary:	GNU uucp server
Summary(de):	GNU-uucp
Summary(fr):	uucp de GNU
Summary(pl):	Serwer GNU uucp
Group:		Networking
Requires:	%{name} = %{version}

%description server
GNU uucp server.

%description server -l pl
Serwer GNU uucp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

find . -name "*.perlpath" | xargs rm -f

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-newconfigdir=/etc/uucp \
	--with-oldconfigdir=/etc/uucp/oldconfig

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/{lock/uucp,spool/{uucp,uucppublic}}
install -d $RPM_BUILD_ROOT/var/log/{uucp,archiv/uucp}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{uucp/oldconfig,sysconfig/rc-inetd,cron.d,logrotate.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	OWNER=$(id -u)

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/uucp
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/uucp
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.d/uucp
bzip2 -dc %{SOURCE4} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

# Create empty files
for n in Log Stats Debug; do
	touch $RPM_BUILD_ROOT/var/log/uucp/$n
done

for i in dial passwd port dialcode sys call ; do
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

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post server
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun server
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO sample contrib

%attr(750,uucp,root) %dir %{_sysconfdir}/uucp
%attr(755,uucp,root) %dir %{_sysconfdir}/uucp/oldconfig

%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/uucp/ca*
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/uucp/di*
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/uucp/p*
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/uucp/sys

%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/uucp
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/cron.d/%{name}

%attr(4554,uucp,uucp) %{_bindir}/cu
%attr(4554,uucp,uucp) %{_bindir}/uucp
%attr(0755,root,root) %{_bindir}/uulog
%attr(4554,uucp,uucp) %{_bindir}/uuname
%attr(0755,root,root) %{_bindir}/uupick
%attr(4554,uucp,uucp) %{_bindir}/uustat
%attr(0755,root,root) %{_bindir}/uuto
%attr(4554,uucp,uucp) %{_bindir}/uux

%{_infodir}/uucp.*

%{_mandir}/man[18]/*
%lang(fi) %{_mandir}/fi/man[18]/*
%lang(ja) %{_mandir}/ja/man[18]/*
%lang(pl) %{_mandir}/pl/man[18]/*

%attr(0755,uucp,uucp) %{_sbindir}/uuchk
%attr(4554,uucp,uucp) %{_sbindir}/uucico
%attr(0755,uucp,uucp) %{_sbindir}/uuconv
%attr(0755,root,root) %{_sbindir}/uusched
%attr(4554,uucp,uucp) %{_sbindir}/uuxqt

%attr(755,uucp,uucp) %dir /var/spool/uucppublic
%attr(755,uucp,uucp) %dir /var/spool/uucp

%attr(750,uucp,root) %dir /var/log/uucp
%attr(750,uucp,root) %dir /var/log/archiv/uucp
%attr(750,uucp,root) %dir /var/lock/uucp
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) /var/log/uucp/Debug
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) /var/log/uucp/Log
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) /var/log/uucp/Stats

%files server
%defattr(644,root,root,755)
%attr(640,root,root) %config /etc/sysconfig/rc-inetd/uucp
