Summary:	GNU uucp
Summary(de):	GNU-uupc 
Summary(fr):	uucp de GNU
Summary(pl):	GNU uucp
Summary(tr):	GNU uucp sistemi
Name:		uucp
Version:	1.06.1
Release:	3
Copyright:	GPL
Group:		Daemons
Group(pl):	Demony
Source0:	ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.gz
Source1:	%{name}.logrotate
Patch0:		%{name}-misc.patch
Buildroot:	/tmp/%{name}-%{version}-root

%description
UUCP is a Unix to Unix transfer mechanism.  It is used primarily
for remote sites to download and upload email and news files to local
machines. If you didn't already know that, you probably don't need this
package installed.  :-)

%description -l de
UUCP ist ein Unix-nach-Unix-Übertragungsprotokoll. Es wird vor allem
verwendet, um E-Mail- und News-Dateien von entfernten auf lokale Rechner
herunter- bzw. umgekehrt hochzuladen. Wie Sie wahrscheinlich wissen,
müssen Sie das Paket wahrscheinlich nicht installieren.  :-)

%description -l fr
UUCP est un mécanisme de transfert d'UNIX à UNIX. Il est principalement
utilisés par les sites de connexion pour télécharger ou envoyer des courriers
èlèctroniques et des nouvelles sur les machines locales. Si vous ne saviez
pas déja cela, vous n'avez probablement pas besoin d'insatller ce package.

%description -l pl
UUCP (Unix to Unix Copy Protocol) jest jednym z podstawowych protoko³ów systemu
Linux. U¿ywany jest przede wszystkim do wysy³ania i pobierania przesy³ek newsów
oraz poczty elektronicznej mêdzy maszynami po³±czonymi np. przez modem. 

%description -l tr
UUCP bir Unix'ten Unix'e iletim mekanizmasýdýr. Uzak sitelerden yerel
sisteme e-posta ve haber öbekleri aktarýmý için kullanýlýr. Bunun ne
olduðunu bilmiyorsanýz, büyük olasýlýkla iþinize de yaramayacaktýr. :-)

%prep
%setup -q
%patch0 -p1 

find . -name "*.perlpath" | xargs rm -f

%build
autoconf && %configure

make clean; make 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/{bin,sbin,share/{man/man{1,8},info}}

make \
    prefix=$RPM_BUILD_ROOT%{_prefix} \
    infodir=$RPM_BUILD_ROOT%{_infodir} \
    bindir=$RPM_BUILD_ROOT%{_bindir} \
    sbindir=$RPM_BUILD_ROOT%{_sbindir} \
    man1dir=$RPM_BUILD_ROOT%{_mandir}/man1 \
    man8dir=$RPM_BUILD_ROOT%{_mandir}/man8 \
    owner=`id -u` \
    install install-info 

gzip -9nf $RPM_BUILD_ROOT%{_infodir}/uucp*
gzip -9nf README ChangeLog MANIFEST NEWS sample/* 
gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,8}/*

install -d $RPM_BUILD_ROOT/var/spool/{uucp,uucppublic}
install -d $RPM_BUILD_ROOT/etc/uucp/oldconfig

install -d $RPM_BUILD_ROOT/usr/lib/uucp
ln -sf ../../sbin/uucico $RPM_BUILD_ROOT/usr/lib/uucp/uucico

install -d $RPM_BUILD_ROOT/etc/logrotate.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/uucp

install -d $RPM_BUILD_ROOT/var/log/uucp

# Create empty files
for n in Log Stats Debug; do
	touch $RPM_BUILD_ROOT/var/log/uucp/$n
done

for i in dial passwd port dialcode sys call ; do
cat > $RPM_BUILD_ROOT/etc/uucp/$i <<EOF 
# This is an example of a $i file. This file have the syntax compatible
# with Taylor UUCP (not HDB, not anything else). Please check uucp
# documentation if you are not sure how Taylor config files are supposed to 
# look like. Edit it as appropriate for your system.

# Everything after a '#' character is a comment.
EOF
done

# some more documentation
texi2html -monolithic uucp.texi

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/uucp.info.gz /etc/info-dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --del %{_infodir}/uucp.info.gz /etc/info-dir
fi

%files
%defattr(644,root,root,755)
%doc *.gz sample 

%attr(750,uucp,root) %dir /etc/uucp
%attr(755,uucp,root) %dir /etc/uucp/oldconfig

%attr(640,uucp,root) %config %verify(not size mtime md5) /etc/uucp/ca*
%attr(640,uucp,root) %config %verify(not size mtime md5) /etc/uucp/di*
%attr(640,uucp,root) %config %verify(not size mtime md5) /etc/uucp/p*
%attr(640,uucp,root) %config %verify(not size mtime md5) /etc/uucp/sys

%attr(640,root,root) %config /etc/logrotate.d/uucp

%attr(4711,uucp,uucp) %{_bindir}/cu
%attr(4711,uucp,uucp) %{_bindir}/uucp
%attr(0755,root,root) %{_bindir}/uulog
%attr(4711,uucp,uucp) %{_bindir}/uuname
%attr(0755,root,root) %{_bindir}/uupick
%attr(4711,uucp,uucp) %{_bindir}/uustat
%attr(0755,root,root) %{_bindir}/uuto
%attr(4711,uucp,uucp) %{_bindir}/uux

%{_infodir}/uucp.*

%attr(755,root,root) %dir %{_libdir}/uucp
%attr(755,root,root) %{_libdir}/uucp/uucico

%{_mandir}/man[18]/*

%attr(0755,uucp,uucp) %{_sbindir}/uuchk
%attr(4711,uucp,uucp) %{_sbindir}/uucico
%attr(0755,uucp,uucp) %{_sbindir}/uuconv
%attr(0755,root,root) %{_sbindir}/uusched
%attr(4711,uucp,uucp) %{_sbindir}/uuxqt

%attr(755,uucp,uucp) %dir /var/spool/uucppublic

%attr(750,uucp,root) %dir /var/log/uucp
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) /var/log/uucp/Debug
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) /var/log/uucp/Log
%attr(640,uucp,root) %config(noreplace) %verify(not size mtime md5) /var/log/uucp/Stats

%changelog
* Sun Dec 06 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [1.06.1-1d]
- build for Linux PLD from non root's account,
- rewrote spec file & major changes.
