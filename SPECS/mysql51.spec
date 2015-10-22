
# Uncomment if working with an Release Candidate version, and comment if your not.
#%%define rc_tag -rc

# ius stuff
%global basever 5.1
%global real_name mysql
%global name mysql51

Name: %{name}
Version: 5.1.72
Release: 1.ius%{?dist}
Summary: MySQL client programs and shared libraries.
License: GPL
Group: Applications/Databases
URL: http://www.mysql.com
BuildRoot: %{_tmppath}/%{name}-%{version}-root

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest:%global runselftest 1}

# Upstream has a mirror redirector for downloads, so the URL is hard to
# represent statically.  You can get the tarball by following a link from
# http://dev.mysql.com/downloads/mysql/
Source0: mysql-%{version}-nodocs.tar.gz
# The upstream tarball includes non-free documentation that we cannot ship.
# To remove the non-free documentation, run this script after downloading
# the tarball into the current directory:
# ./generate-tarball.sh $VERSION
Source1: generate-tarball.sh

Source2: mysql.init
Source3: mysql.logrotate
Source4: scriptstub.c
Source5: my_config.h
Source9: mysql-embedded-check.c
Source10: README.mysql-docs
Source11: mysqld.sysconfig

Source100: my-51-terse.cnf
Source101: my-51-verbose.cnf

# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh 

Patch1: mysql-ssl-multilib.patch
Patch2: mysql-errno.patch
# Patch3: mysql-stack.patch
Patch4: mysql-testing.patch
#Patch5: mysql-install-test.patch
Patch6: mysql-stack-guard.patch
#Patch7: mysql-plugin-bug.patch
Patch8: mysql-setschedparam.patch
#Patch10: mysql-strmov.patch
Patch11: mysql-signal-align.patch
Patch12: mysql-cve-2008-7247.patch
#Patch13: mysql-expired-certs.patch
#Patch14: mysql-charset-bug.patch
Patch15: mysql-no-docs.patch
#Patch16: mysql-lowercase-bug.patch

Patch201: mysql-5.1.24-libdir.patch 
#Patch207: mysql-5.0.41-compress-test.patch 
Patch209: mysql-5.0.67-bindir.patch
Patch311: mysql-5.1.28-rc-mysqld_safe.patch 
Patch315: mysql-5.1.37-sysconfig.patch 
# Test structure has changed in 5.1.58
#Patch316: mysql-5.1.54-disabled_tests.patch
Patch317: mysql-5.1.61-disabled_tests.patch

#Disable SSL_OP_NO_COMPRESSION as it is not available in openssl for RHEL 5
Patch318: mysql-5.1.69-disable_SSL_OP_NO_COMPRESSION.patch

Requires: %{name}-libs = %{version}-%{release}
Requires: bash, grep, fileutils
BuildRequires: gperf, perl, readline-devel, openssl-devel
BuildRequires: gcc, gcc-c++, ncurses-devel, zlib-devel
BuildRequires: libtool automake autoconf
BuildRequires: gettext-devel
# make test requires time and ps
BuildRequires: time procps
# Socket is needed to run regression tests
BuildRequires: perl(Socket)

Provides:  %{real_name} = %{version}-%{release}
Provides: mysqlclient16 = %{version}
Conflicts: %{real_name} < %{basever}
Conflicts: MySQL

# Not compatible with Plesk < 9.5 (Rackspace-isms)
Conflicts: psa < 9.5

# added as a convenience, mysql51 doesn't require mysqlclient15
# but all the packages built against mysql 5.0 do
Requires: mysqlclient15 


# Working around perl dependency checking bug in rpm FTTB. Remove later.
%global __perl_requires %{SOURCE999}

%description
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the MySQL client programs, the client shared libraries, and
generic MySQL files.


%package libs
Summary: The shared libraries required for MySQL clients
Group: Applications/Databases
Requires: /sbin/ldconfig

%description libs
The mysql-libs package provides the essential shared libraries for any
MySQL client program or interface. You will need to install this package
to use any other MySQL package or any clients that need to connect to a
MySQL server.

%package server
Summary: The MySQL server and related files.
License: GPL
Group: Applications/Databases
Requires(pre): /sbin/chkconfig, /usr/sbin/useradd
Requires: %{name} = %{version}-%{release}, sh-utils
# mysqlhotcopy needs DBI/DBD support
Requires: perl-DBI, perl-DBD-MySQL
Conflicts: MySQL-server
Provides:   %{real_name}-server = %{version}-%{release}
Conflicts:  %{real_name}-server < %{base_ver}
Conflicts:  mysql50-server

# Plugins - obsolete old subpackages
Obsoletes: %{name}-plugins-blackhole < 5.1.46-1
Obsoletes: %{name}-plugins-archive < 5.1.46-1
Obsoletes: %{name}-plugins-example < 5.1.46-1
Obsoletes: %{name}-plugins-innodb < 5.1.46-1
Obsoletes: %{name}-plugins-federated < 5.1.46-1

%description server
MySQL is a multi-user, multi-threaded SQL database server. MySQL is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MySQL server and some accompanying files and directories.

%package devel
Summary: Files for development of MySQL applications.
License: GPL
Group: Applications/Databases
Requires:   %{name} = %{version}-%{release}
Requires:   openssl-devel
Conflicts:  MySQL-devel
Provides:   mysqlclient16-devel = %{version}
Provides:   %{real_name}-devel = %{version}-%{release}
Conflicts:  %{real_name}-devel < %{base_ver}
Conflicts:  mysql50-devel

%description devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the libraries and header files that are needed for
developing MySQL client applications.


%package embedded
Summary: MySQL as an embeddable library
Group: Applications/Databases

%description embedded
MySQL is a multi-user, multi-threaded SQL database server. This
package contains a version of the MySQL server that can be embedded
into a client application instead of running as a separate process.

%package embedded-devel
Summary: Development files for MySQL as an embeddable library
Group: Applications/Databases
Requires: %{name}-embedded = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description embedded-devel
MySQL is a multi-user, multi-threaded SQL database server. This
package contains files needed for developing and testing with
the embedded version of the MySQL server.

%package bench
Summary:    MySQL benchmark scripts and data.
License:    GPL
Group:      Applications/Databases
Requires:   %{name} = %{version}-%{release}
Conflicts:  MySQL-bench
Provides:   %{real_name}-bench = %{version}-%{release}
Conflicts:  %{real_name}-bench < %{base_ver}
Conflicts:  mysql50-bench

%description bench
MySQL is a multi-user, multi-threaded SQL database server. This
package contains benchmark scripts and data for use when benchmarking
MySQL.

%package test
Summary: The test suite distributed with MySQL
Group: Applications/Databases
Requires: %{name} = %{version}-%{release}
Requires: %{name}-server = %{version}-%{release}
Conflicts: MySQL-test

%description test
MySQL is a multi-user, multi-threaded SQL database server. This
package contains the regression test suite distributed with
the MySQL sources.


%prep
%setup -q -n %{real_name}-%{version}%{?rc_tag} 
cp %SOURCE10 .
cp %SOURCE100 .
cp %SOURCE101 .

sed -i "s|@@@mysql_server_docdir@@@|%{_docdir}|" my-51-terse.cnf
sed -i "s|@@@mysql_server_docdir@@@|%{_docdir}|" my-51-verbose.cnf

%patch1 -p1
%patch2 -p1
# %%patch3 -p1
%patch4 -p1
#%%patch5 -p1
%patch6 -p1
#%%patch7 -p1
%patch8 -p1
#%patch10 -p1
%patch11 -p1
%patch12 -p1
#%%patch13 -p1
#%%patch14 -p1
%patch15 -p1
#%patch16 -p1
%patch201 -p1
#%%patch207 -p1  
%patch209 -p1 -b .bindir
%patch311 -p1 -b .mysqld_safe
%patch315 -p1 -b .sysconfig
#%patch316 -p1 -b .disabled_tests
%patch317 -p1 -b .disabled_tests
%patch318 -p1

libtoolize --force
aclocal
automake --add-missing -Wno-portability
autoconf
autoheader

%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
    if [ x"`id -u`" = x0 ]; then
    echo "mysql's regression tests fail if run as root."
    echo "If you really need to build the RPM as root, use"
    echo "--define='runselftest 0' to skip the regression tests."
    exit 1
    fi
%endif

CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv -fPIC"
CXXFLAGS="$CFLAGS -felide-constructors -fno-rtti -fno-exceptions"
export CFLAGS CXXFLAGS

%configure \
    --with-comment='Distributed by The IUS Community Project' \
    --with-server-suffix='-ius' \
    --with-readline \
    --with-ssl=/usr \
    --without-debug \
    --enable-shared \
    --with-embedded-server \
    --localstatedir=/var/lib/mysql \
    --with-unix-socket-path=/var/lib/mysql/mysql.sock \
    --with-mysqld-user="mysql" \
    --with-extra-charsets=all \
    --with-big-tables \
    --with-pic \
    --enable-local-infile \
    --enable-largefile \
    --with-innodb \
    --with-plugin-partition \
    --with-federated-storage-engine \
    --enable-thread-safe-client \
    --disable-dependency-tracking \
    --enable-community-features \
    --enable-profiling

gcc $CFLAGS $LDFLAGS -o scriptstub "-DLIBDIR=\"%{_libdir}/mysql\"" %{SOURCE4}

make %{?_smp_mflags}

# regular build will make libmysqld.a but not libmysqld.so :-(
mkdir libmysqld/work
cd libmysqld/work
ar -x ../libmysqld.a

# Resolves MySQL Bug #48960
rm ha_federated.o libfederated*string.o

gcc $CFLAGS $LDFLAGS -shared -Wl,-soname,libmysqld.so.0 -o libmysqld.so.0.0.1 \
    *.o \
    -lpthread -lcrypt -lnsl -lssl -lcrypto -lz -lrt -lstdc++ -lm -lc
# this is to check that we built a complete library
cp %{SOURCE9} .
ln -s libmysqld.so.0.0.1 libmysqld.so.0
gcc -I../../include $CFLAGS mysql-embedded-check.c libmysqld.so.0
LD_LIBRARY_PATH=. ldd ./a.out
cd ../..


%check

make check

%if %runselftest
  make test
%endif

%install
rm -rf %{buildroot}

%makeinstall
install -m 644 include/my_config.h %{buildroot}/usr/include/mysql/my_config_`uname -i`.h
install -m 644 %{SOURCE5} %{buildroot}/usr/include/mysql/
mkdir -p %{buildroot}/var/log \
         %{buildroot}/var/lib/mysqllogs \
         %{buildroot}/var/lib/mysqltmp
touch %{buildroot}/var/log/mysqld.log

# List the installed tree for RPM package maintenance purposes.
find %{buildroot} -print | sed "s|^%{buildroot}||" | sort > ROOTFILES
rm -f %{buildroot}%{_datadir}/mysql/mysql-*.spec
rm -f %{buildroot}%{_datadir}/mysql/mysql-log-rotate

mkdir -p %{buildroot}/etc/{rc.d/init.d,logrotate.d}
mkdir -p %{buildroot}/var/run/mysqld
install -m 0755 -d %{buildroot}/var/lib/mysql
install -m 0755 %{SOURCE2} %{buildroot}/etc/rc.d/init.d/mysqld
install -m 0644 %{SOURCE3} %{buildroot}/etc/logrotate.d/mysqld
install -m 0644 my-51-terse.cnf %{buildroot}/etc/my.cnf
mv %{buildroot}/usr/mysql-test $RPM_BUILD_ROOT%{_datadir}/mysql-test
# 5.1.32 forgets to install the mysql-test README file
install -m 0644 mysql-test/README $RPM_BUILD_ROOT%{_datadir}/mysql-test/README

# Environment file
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mysqld


# install the archive_reader tool
install -m 0755 storage/archive/archive_reader %{buildroot}%{_bindir}

rm -f %{buildroot}/%{_infodir}/dir*
mv %{buildroot}/usr/sql-bench %{buildroot}%{_datadir}/sql-bench

mv %{buildroot}%{_bindir}/mysqlbug %{buildroot}%{_libdir}/mysql/mysqlbug
install -m 0755 scriptstub %{buildroot}%{_bindir}/mysqlbug
mv %{buildroot}%{_bindir}/mysql_config %{buildroot}%{_libdir}/mysql/mysql_config
install -m 0755 scriptstub %{buildroot}%{_bindir}/mysql_config
cp -a support-files/mysql.server support-files/mysql.init-lsb_compliant

rm -f %{buildroot}%{_libdir}/mysql/libmysqld.a
install -m 0755 libmysqld/work/libmysqld.so.0.0.1 %{buildroot}%{_libdir}/mysql/libmysqld.so.0.0.1
ln -s libmysqld.so.0.0.1 %{buildroot}%{_libdir}/mysql/libmysqld.so.0
ln -s libmysqld.so.0 %{buildroot}%{_libdir}/mysql/libmysqld.so

rm -f %{buildroot}%{_bindir}/comp_err
rm -f %{buildroot}%{_mandir}/man1/comp_err.1*
rm -f %{buildroot}%{_bindir}/make_win_binary_distribution
rm -f %{buildroot}%{_bindir}/make_win_src_distribution
rm -f %{buildroot}%{_mandir}/man1/make_win_bin_dist.1*
rm -f %{buildroot}%{_mandir}/man1/make_win_src_distribution.1*
rm -f %{buildroot}%{_libdir}/mysql/libmysqlclient*.la
rm -f %{buildroot}%{_libdir}/mysql/libndbclient.la
rm -f %{buildroot}%{_libdir}/mysql/plugin/*.la
rm -f %{buildroot}%{_libdir}/mysql/plugin/*.a
rm -f %{buildroot}%{_datadir}/mysql/binary-configure
rm -f %{buildroot}%{_datadir}/mysql/make_binary_distribution
rm -f %{buildroot}%{_datadir}/mysql/make_sharedlib_distribution
rm -f %{buildroot}%{_datadir}/mysql/mi_test_all*
rm -f %{buildroot}%{_datadir}/mysql/mysql.server
rm -f %{buildroot}%{_datadir}/mysql/mysqld_multi.server
rm -f %{buildroot}%{_datadir}/mysql/MySQL-shared-compat.spec
rm -f %{buildroot}%{_datadir}/mysql/*.plist
rm -f %{buildroot}%{_datadir}/mysql/preinstall
rm -f %{buildroot}%{_datadir}/mysql/postinstall
rm -f %{buildroot}%{_datadir}/mysql/mysql-*.spec
rm -f %{buildroot}%{_datadir}/mysql/mysql-log-rotate
rm -f %{buildroot}%{_datadir}/mysql/ChangeLog
rm -f %{buildroot}%{_mandir}/man1/mysql-stress-test.pl.1*
rm -f %{buildroot}%{_mandir}/man1/mysql-test-run.pl.1*
rm -f %{buildroot}/usr/libexec/ndb_cpcd
rm -f %{buildroot}%{_mandir}/man1/ndb_cpcd.1*
rm -f %{buildroot}/%{_datadir}/mysql/ndb-config-2-node.ini

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{_libdir}/mysql" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

%clean
rm -rf %{buildroot}

%pre 
# This is to remind everyone to run fix_privilege_tables
curMySQLVersion=$(mysql_config --version 2> /dev/null | awk -F . {' print $1"."$2 '})
newMySQLVersion=$(echo %{version} | awk -F . {' print $1"."$2 '})

curIsLessThanNew=$(echo "$curMySQLVersion $newMySQLVersion" | awk '{if ($1 < $2) print "true"}')
if [ $curIsLessThanNew ]; then 
cat <<EOF
========================================================================

    Please note that if you are upgrading major versions of MySQL
    you must run the following script after installation:

    %{_bindir}/mysql_upgrade -t /tmp

========================================================================
EOF
fi


%pre server
/usr/sbin/groupadd -g 27 mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -M -o -r -d /var/lib/mysql -s /bin/bash \
    -c "MySQL Server" -u 27 mysql -g mysql > /dev/null 2>&1 || :

%post 
/sbin/ldconfig

%post server
if [ $1 = 1 ]; then
    /sbin/chkconfig --add mysqld
fi
if [ $1 -ge 1 ]; then
    /sbin/service mysqld condrestart || :
fi
/bin/chmod 0755 /var/lib/mysql
/bin/touch /var/log/mysqld.log

%preun server
if [ $1 = 0 ]; then
    /sbin/service mysqld stop || :
    /sbin/chkconfig --del mysqld
fi

%postun
if [ $1 = 0 ] ; then
    /sbin/ldconfig
fi


%files
%defattr(-,root,root)
%doc README COPYING
%doc README.mysql-docs

%{_bindir}/msql2mysql
%{_bindir}/mysql
%{_bindir}/mysql_config
%{_bindir}/mysql_find_rows
%{_bindir}/mysql_waitpid
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/my_print_defaults

%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysql_config.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysql_waitpid.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlslap.1*
%{_mandir}/man1/my_print_defaults.1*

%{_libdir}/mysql/mysqlbug
%{_libdir}/mysql/mysql_config


%files libs
%defattr(-,root,root)
%doc COPYING

# although the default my.cnf contains only server settings, we put it in the
# libs package because it can be used for client settings too.
%config(noreplace) /etc/my.cnf

%dir %{_libdir}/mysql
%{_libdir}/mysql/libmysqlclient*.so.*
/etc/ld.so.conf.d/*

%dir %{_datadir}/mysql
%{_datadir}/mysql/english
%lang(cs) %{_datadir}/mysql/czech
%lang(da) %{_datadir}/mysql/danish
%lang(nl) %{_datadir}/mysql/dutch
%lang(et) %{_datadir}/mysql/estonian
%lang(fr) %{_datadir}/mysql/french
%lang(de) %{_datadir}/mysql/german
%lang(el) %{_datadir}/mysql/greek
%lang(hu) %{_datadir}/mysql/hungarian
%lang(it) %{_datadir}/mysql/italian
%lang(ja) %{_datadir}/mysql/japanese
%lang(ko) %{_datadir}/mysql/korean
%lang(no) %{_datadir}/mysql/norwegian
%lang(no) %{_datadir}/mysql/norwegian-ny
%lang(pl) %{_datadir}/mysql/polish
%lang(pt) %{_datadir}/mysql/portuguese
%lang(ro) %{_datadir}/mysql/romanian
%lang(ru) %{_datadir}/mysql/russian
%lang(sr) %{_datadir}/mysql/serbian
%lang(sk) %{_datadir}/mysql/slovak
%lang(es) %{_datadir}/mysql/spanish
%lang(sv) %{_datadir}/mysql/swedish
%lang(uk) %{_datadir}/mysql/ukrainian
%{_datadir}/mysql/charsets

%files server
%defattr(-,root,root)
%doc support-files/*.cnf my-51-verbose.cnf

%config(noreplace) %{_sysconfdir}/logrotate.d/mysqld
%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_fix_privilege_tables
%{_bindir}/mysql_install_db
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_upgrade
%{_bindir}/mysql_zap
%{_bindir}/mysqlbug
%{_bindir}/mysqldumpslow
%{_bindir}/mysqld_multi
%{_bindir}/mysqld_safe
%{_bindir}/mysqlhotcopy
%{_bindir}/mysqltest
%{_bindir}/innochecksum
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip

/usr/libexec/mysqld
/usr/libexec/mysqlmanager

%attr(0755,mysql,mysql) %dir %{_localstatedir}/lib/mysqltmp
%attr(0755,mysql,mysql) %dir %{_localstatedir}/lib/mysqllogs
%dir %{_libdir}/mysql/plugin

%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysql_fix_privilege_tables.1*
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlbug.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqld_multi.1*
%{_mandir}/man1/mysqld_safe.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlman.1*
%{_mandir}/man1/mysql_setpermission.1*
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolve_stack_dump.1*
%{_mandir}/man1/resolveip.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man8/mysqld.8*
%{_mandir}/man8/mysqlmanager.8*

%{_datadir}/mysql/errmsg.txt
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_fix_privilege_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/my-*.cnf
%{_datadir}/mysql/config.*.ini

/etc/rc.d/init.d/mysqld
%config(noreplace) %{_sysconfdir}/sysconfig/mysqld
%attr(0755,mysql,mysql) %dir /var/run/mysqld
%attr(0755,mysql,mysql) %dir /var/lib/mysql
%attr(0640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) /var/log/mysqld.log

# Plugins
%{_bindir}/archive_reader
%{_libdir}/mysql/plugin/ha_archive.so*
%{_libdir}/mysql/plugin/ha_blackhole.so*
%{_libdir}/mysql/plugin/ha_example.so*
%{_libdir}/mysql/plugin/ha_innodb_plugin.so*

%files devel
%defattr(-,root,root)
/usr/include/mysql
/usr/share/aclocal/mysql.m4
%{_libdir}/mysql/*.a
%{_libdir}/mysql/libmysqlclient*.so

%files embedded
%defattr(-,root,root)
%doc COPYING
%{_libdir}/mysql/libmysqld.so.*

%files embedded-devel
%defattr(-,root,root)
%{_libdir}/mysql/libmysqld.so
%{_bindir}/mysql_client_test_embedded
%{_bindir}/mysqltest_embedded
%{_mandir}/man1/mysql_client_test_embedded.1*
%{_mandir}/man1/mysqltest_embedded.1*

%files bench
%defattr(-,root,root)
%{_datadir}/sql-bench

%files test
%defattr(-,root,root)
%{_bindir}/mysql_client_test
%attr(-,mysql,mysql) %{_datadir}/mysql-test
%{_mandir}/man1/mysql_client_test.1.gz


%changelog
* Mon Sep 23 2013 Ben Harper <ben.harper@rackspace.com> - 5.1.72-1.ius
- Latest soruce from upstream, full changelog found at:
  http://dev.mysql.com/doc/relnotes/mysql/5.1/en/news-5-1-72.html

* Mon Sep 16 2013 Ben Harper <ben.harper@rackspace.com> - 5.1.71-2.ius
- add mysqld.sysconfig to mysql51-server
- increase timeouts in mysql.init

* Fri Aug 02 2013 Ben Harper <ben.harper@rackspace.com> - 5.1.71-1.ius
- Latest soruce from upstream, full changelog found at:
  http://dev.mysql.com/doc/relnotes/mysql/5.1/en/news-5-1-71.html

* Tue Jun 04 2013 Ben Harper <ben.harper@rackspace.com> - 5.1.70-1.ius
- Latest soruce from upstream, full changelog found at:
  http://dev.mysql.com/doc/relnotes/mysql/5.1/en/news-5-1-70.html

* Thu Apr 18 2013 Ben Harper <ben.harper@rackspace.com> - 5.1.69-1.ius
- Latest soruce from upstream, full changelog found at:
  http://dev.mysql.com/doc/relnotes/mysql/5.1/en/news-5-1-69.html
- Patch318 add as SSL_OP_NO_COMPRESSION is not available for RHEL 5 openssl

* Mon Feb 04 2013 Ben Harper <ben.harper@rackspace.com> - 5.1.68-1.ius
- Latest soruce from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-68.html
  
* Fri Dec 21 2012 Ben Harper <ben.harper@rackspace.com> - 5.1.67-1.ius
- Latest soruce from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-67.html

* Mon Oct 01 2012 Ben Harper <ben.harper@rackspace.com> - 5.1.66-1.ius
- Latest soruce from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-66.html

* Thu Aug 09 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.65-1.ius
- Latest soruce from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-65.html

* Mon May 07 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.63-1.ius
- Latest soruce from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-63.html

* Wed May 02 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.62-4.ius
- Remove libpcap Requires per https://bugs.launchpad.net/ius/+bug/992718

* Wed Apr 18 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.62-3.ius
- Remove plugin_dir and federated load from cnf

* Tue Apr 10 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.62-2.ius
- Removing old psa-compat package

* Fri Mar 23 2012 BJ Dierkes <wdierkes@rackspace.com> - 5.1.62-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-62.html

* Thu Jan 12 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.61-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-61.html
- Update to patch mysql-5.1.61-disabled_tests.patch

* Wed Jan 04 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.60-2.ius
- Removing userdel from %%postun server per 
  https://bugs.launchpad.net/ius/+bug/898228

* Tue Jan 03 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.60-1.ius
- Needed to append libfederated*string.o to rm line,
  this resolves MySQL Bug #48960

* Mon Sep 19 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.59-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-59.html

* Wed Jul 06 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.58-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-58.html
- Removing Patch316: mysql-5.1.54-disabled_tests.patch,
  test structure has changed in 5.1.58
- Adding Patch317: mysql-5.1.58-disabled_tests.patch

* Mon May 09 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.57-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-57.html

* Mon Mar 07 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.56-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-56.html

* Wed Feb 09 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.55-1.ius
- Latest sources from upstream, full changelog found at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-55.html

* Tue Jan 11 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.54-2.ius
- Renamed Patch316: mysql-5.1.50-disabled_tests.patch to
  mysql-5.1.54-disabled_tests.patch
- Removed %%doc EXCEPTIONS-CLIENT

* Tue Jan 11 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.1.54-1.ius
- Latest sources from upstream. Full change log available at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-54.html
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-53.html
- Support for the IBMDB2I storage engine has been removed.
- The pstack library was nonfunctional and has been removed, 
  along with the --with-pstack option for configure
- Commented Patch10: mysql-strmov.patch
- Commented Patch16: mysql-lowercase-bug.patch
- Commented Patch316: mysql-5.1.50-disabled_tests.patch

* Tue Nov 02 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.52-1.ius
- Latest sources from upstream.  Full change log available at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-52.html  
- Add explicit version-release to obsoleted plugins under -server
- No longer Obsolete: mysqlclient16-devel (under -devel)
- Backporting changes from Fedora packages (including the following) 
- Allow init script's STARTTIMEOUT/STOPTIMEOUT to be overridden from 
  sysconfig.  Related: #609734
- Bring init script into some modicum of compliance with Fedora/LSB 
  standards Related: #557711, #562749
- Duplicate COPYING and EXCEPTIONS-CLIENT in -libs and -embedded subpackages,
  to ensure they are available when any subset of mysql RPMs are installed,
  per revised packaging guidelines

* Tue Sep 28 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.51-1.ius
- Latest sources from upstream.  Full changelog available at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-51.html
- Actually include mysqllogs directory with files.  Resolves LP#646980
- No longer Obsoletes: mysql-client mysql-perl
- No longer Obsoletes: MySQL <= %%{version}
- No longer Obsoletes: mysqlclient16
- Removed Patch5: mysql-install-test.patch

* Thu Sep 09 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.50-1.ius
- Latest sources from upstream.  Full changelog available at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-50.html
- Removed Patch13: mysql-expired-certs.patch
- Added Patch316: mysql-5.1.50-disabled_tests.patch

* Wed Aug 11 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.49-3.ius
- Make base package conflict with psa < 9.5

* Wed Jul 28 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.49-2.ius
- Added -psa-compat package, resolves LP#610824

* Fri Jul 23 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.49-1.ius
- Latest sources from upstream

* Thu Jun 24 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.48-2.ius
- Rebuild against 'i386' mock config

* Tue Jun 22 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.48-1.ius
- Latest sources from upstream.  Full changelog available at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-48.html

* Mon Jun 21 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.47-3.ius
- No longer "Require: mysql >= 5.0" as we only build for RHEL 5+
- No longer "Require: mysqlclient15-devel"

* Tue Jun 08 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.47-2.ius
- Add --with-plugin-partition (static is the only option) 
- Add "innodb = FORCE" to my.cnf configs
- Fix bogus perl requires (updated Source999: filter-requires-mysql.sh)

* Fri May 21 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.47-1.ius
- Latest sources from upstream.  Full changelog available at:
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-47.html
- This update resolves the following security issues:
  CVE-2010-1848, CVE-2010-1850, CVE-2010-1849   
- Build federated storage engine static since MySQL is dragging their 
  feet to fix it in 5.1 for nearly 2 years now.  MySQL Bug #40942.
- Removed Patch7: mysql-plugin-bug.patch
- Add hack to remove ha_federated.o (MySQL Bug #48960), and build
  federated storage engine static

* Mon May 18 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.46-1.ius
- Latest sources
- No longer package plugins separately, -server obsoletes previous 
  plugin subpackages
- Remove Patch14: mysql-charset-bug.patch (applied upstream)
- Chopping changelog of all entries before 5.1

* Fri May 15 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.45-4.2.ius
- Fixed source numbers to match Fedora changes

* Mon May 10 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.45-3.ius
- Removed broken federated plugin

* Mon Apr 26 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.45-2.ius
- Update to MySQL 5.1.45, for various fixes described at
  http://dev.mysql.com/doc/refman/5.1/en/news-5-1-45.html
- Added the following patches (backported from Fedora 12):
    Patch1: mysql-ssl-multilib.patch
    Patch4: mysql-testing.patch
    Patch5: mysql-install-test.patch
    Patch6: mysql-stack-guard.patch
    Patch7: mysql-plugin-bug.patch
    Patch8: mysql-setschedparam.patch (Related: BZ#477624)
    Patch10: mysql-strmov.patch
    Patch11: mysql-signal-align.patch
    Patch12: mysql-cve-2008-7247.patch (MySQL Bug #39277)
    Patch13: mysql-expired-certs.patch
    Patch14: mysql-charset-bug.patch (MySQL Bug #45058)
    Patch15: mysql-no-docs.patch
    Patch16: mysql-lowercase-bug.patch
- Remove Patch207: mysql-5.0.41-compress-test.patch
- Remove mysql.info, which is not freely redistributable
  Resolves: BZ#560181
- Emit explicit error message if user tries to build RPM as root
  Related: BZ#558915
- Change %%define to %%global per Fedora Packaging Guidelines
- Remove ndb cluster (has not been built for a while anyway)
- Remove el3 hacks (no longer build for el3)
- Add --with-big-tables, --with-embedded-server
- Remove explicit --with-named-thread-libs
- Add sub packages embedded, embedded-devel, test
- Add libtoolize, aclocal, automake, autoconf, autoheader (per Fedora)
- Add Source9: mysql-embedded-check.c, and work-around to build mysqld.so

* Wed Mar 17 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.45-1.ius
- Latest sources from upstream.
- Fix plugin build options
- Remove option plugin condition checks, make innodb always build
- Removed federated since MySQL doesn't seem to care about fixing it.

* Mon Mar 01 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.44-1.ius
- Latest sources from upstream.
- Removed Patch316: mysql-5.1.43-ssl_cert.patch (applied upstream)
- Removed Patch317: mysql-5.1.42-bug50018.patch (applied upstream)

* Mon Feb 01 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.43-1.ius
- Latest sources from upstream
- Added Patch316: mysql-5.1.43-ssl_cert.patch
- Added Patch317: mysql-5.1.42-bug50018.patch
- Conflicts: psa 
- Fixed plugin configure options

* Tue Jan 05 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.1.42-1.ius
- Latest sources from upstream, resolves LP#502099
- Explicity set -g 27 guid when adding mysql group, resolves LP#499650

* Wed Nov 25 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.41-2.ius
- Build with innodb plugin by default.

* Tue Nov 24 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.41-1.ius
- Latest sources from upstream.
- Adding skip-name-resolve and tmpdir settings to my.cnf
- Create /var/lib/mysqltmp per new cnf settings.

* Tue Nov 03 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.40-1.ius
- Latest sources from upstream.

* Fri Sep 25 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.39-1.ius
- Latest sources from upstream.
- Added _with_innodb_plugin build option, but left disabled by default
  due to MySQL's claim that it is of beta quality.

* Mon Aug 31 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.37-2.1.ius
- Updated mysql configs slighly

* Mon Aug 25 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.37-2.ius
- Install storage/archive/archive_reader with plugins-archive 
  package, resolves internal Rackspace tracker [#1387].
- BuildRequires: coreutils

* Thu Aug 06 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.37-1.ius
- Latest sources from upstream
- Added /etc/sysconfig/mysqld with ability to set UMASK and UMASK_DIR
  which is sourced by the mysqld init script.
- Changing comment line for 'The IUS Community Project'
- On %%post(server) do a condrestart rather than restart
- Explicitly add the mysql group in %%post (before the mysql user
  is added)

* Fri Jul 24 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.36-2.ius
- Repackaging for IUS

* Thu Jul 09 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.36-1.1.rs
- Adding --enable-community-features and --enable-profiling explicitly

* Thu Jul 02 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.36-1.rs
- Latest upstream sources.
- Removed Patch315: mysql-5.1.34-bug42749.patch (applied upstream)

* Mon Jun 29 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.34-2.rs
- Adding mysql-5.1.34-bug42749.patch

* Mon May 11 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.34-1.3.rs
- No longer send output of init script to /dev/null.

* Tue May 05 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.34-1.2.rs
- Install EL5 mysqld.init file as /etc/init.d/mysqld, and install MySQL's
  version of the init script to the doc dir.  Remaining inline with Redhat.
  The init script has been modified to exit 0 on 'stop' if the process
  is already stopped.

* Mon May 04 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.34-1.1.rs
- Updating Source2: mysql.logrotate resolves tracker [#1272] (again)

* Wed Apr 29 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.34-1.rs
- Latest sources from upstream.
- Removed Patch314: mysql-5.1.32-disabled_tests.patch
- Added Rackspace comment and version suffix
- Updated Source2: mysql.logrorate resolves tracker [#1272]
- Conflicts: psa < 8.1 resolves tracker [#1225]
- Updated default my.cnf, and adding my.cnf-verbose to %%doc
- Removed Source7: my.cnf-psa (no longer need a specific plesk config)

* Wed Mar 04 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.32-1.1.rs
- Latest sources from upstream.
- Added Patch314: mysql-5.1.32-disabled_tests.patch
- Removed Patch303: mysql-5.1.22-rc-libtool.patch
- Removed Patch304: mysql-5.0.37-testing.patch
- Removed Patch218: mysql-5.0.75-openssl.patch (applied upstream)
- Resolved [#671] - Init script not restarting on upgrade. 

* Mon Feb 09 2009 BJ Dierkes <wdierkes@rackspace.com> - 5.1.31-1.rs
- Adding /var/lib/mysqllogs for specific logging (bin-log, etc)
- Modified /etc/logrotate.d/mysqld to include slow-log in /var/lib/mysqllogs
- Updated my.cnf-new (default) configuration.
- Requires: mysqlclient15 regardless of OS.
- Obsoletes: mysqlclient16
- devel packages obsoletes mysqlclient16-devel
- do not build cluster packages by default.
- Removed Patch313: mysql-5.1.29-rc-disabled_tests.patch
- lograte changes: No rotations of the mysql error log (this is fundamentally 
  broken anyway).  dropped notifempty (logrotate even if the slowquery log 
  is empty=failed last rotation).  changed compress to delaycompress (delay 
  compres  sing an open file, hopefully flush wont' fail twice in a row).  
  changed last-action to postrotate (to attempt flush before any compressing).
- Added Patch218: mysql-5.0.75-openssl.patch
- This update brings Rackspace MySQL 5.1 packages inline with MySQL 5.0
  changes.
- Resolves Rackspace Tracker [#1120] Latest 5.1.31 source available upstream.
  Ref: http://dev.mysql.com/doc/refman/5.1/en/news-5-1-31.html

* Wed Nov 26 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.30-1.rs
- Latest sources from upstream.

* Fri Nov 21 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.29-2.2.rs
- Do a restart rather than condrestart in postun. 
  Resolves bug [#1033] [MySQL 5.1] Error running mysql_upgrade
- Add proper defattr's to plugins file list

* Tue Nov 18 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.29-2.1.rs
- Updating disabled test cases.

* Fri Nov 14 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.29-2.rs
- Added Patch313: mysql-5.1.29-rc-disabled_tests.patch (bug#37075)

* Mon Oct 27 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.29-1.rs
- Latest release candidate sources

* Thu Oct 23 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.28-1.rs
- Latest release candidate sources
- Removed Patch306: mysql-5.1.26-rc-disabled-tests.patch
- Removed Patch307: mysql-5.1.25-rc-rpl_slave_status.patch
- Removed Patch308: mysql-5.1.26-rc-mysqlslap.patch
- Removed Patch309: mysql-5.1.26-rc-rpl_insert.patch
- Removed Patch310: mysql-5.1.26-rc-rpl_row_basic.patch
- Removed Patch312: mysql-5.1.26-rc-rpl_disabled_tests.patch
- Replaced Patch311: mysql-5.0.67-mysqld_safe.patch with 
  mysql-5.1.28-rc-mysqld_safe.patch
- Removed workaround for mkinstalldirs

* Tue Aug 26 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.26-1.2.rs
- Adding Patch311: mysql-5.0.67-mysqld_safe.patch 
- Adding Patch312: mysql-5.1.26-rc-rpl_disabled_tests.patch

* Tue Jul 29 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.26-1.1.rs
- Added Patch309: mysql-5.1.26-rc-rpl_insert.patch
- Added Patch310: mysql-5.1.26-rc-rpl_row_basic.patch MySQL Bug#37884.

* Thu Jul 24 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.26-1.rs
- Latest sources
- Requires: mysql >= 5.0 (don't want/can't upgrade from < 5.0 directly). 
  Resolves RS Bug [#677] [MySQL 5.1] mysql_upgrade borks on EL4.
- Modified mysql.logrotate to use --defaults=/root/.my.cnf.  Resolves 
  RS Bug [#632] [MySQL 5.x] Rotation of the slow query log is empty.
- BuildRequires: gcc
- Replaced Patch306: mysql-5.1.25-rc-disabled-tests.patch with 
  Patch306: mysql-5.1.26-rc-disabled-tests.patch
- Added Patch308: mysql-5.1.26-rc-mysqlslap.patch 

* Wed Jul 23 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.25-1.2.rs
- Change notice in post script to reference mysql_upgrade and not 
  mysql_fix_privilege_tables.  Also, must pass '-t /tmp' to mysql_upgrade.
- Added Source6: my.cnf-new (default), Source7: my.cnf-psa, Source3 is now 
  my.cnf-stock and only installed on el3 (if this even builds on el3 of course).

* Mon Jun 30 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.25-rc.1.1.rs
- BuildRequires/Requires: libpcap (el5)
- Added Patch307: mysql-5.1.25-rc-rpl_slave_status.patch
- Use init script from MySQL sources rather than non-lsb compliant Redhat
  version.  Still install old version to init.d/mysqld-redhat (if its preferred).
  This also Resolves RS Bug [#265] [MySQL] Remove -R from startup script.

* Tue Jun 24 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.25-rc.1.rs
- Latest RC sources
- Added -felide-constructors to CXXFLAGS
- Removed Patch305: mysql-5.1.24-disabled-tests.patch and replaced with
  Patch306: mysql-5.1.25-rc-disabled-tests.patch  

* Wed May 29 2008 BJ Dierkes <wdierkes@rackspace.com> - 5.1.24-rc.1.rs
- Latest sources from MySQL upstream (Release Cadidate)
- Replaced Patch201: mysql-5.0.27-libdir.patch with
  Patch201: mysql-5.1.24-libdir.patch
- Adding Patch305: mysql-5.1.24-disabled-tests.patch
- Adding clustering to be more in line with MySQL packages: clusterstorage
  clustermanagement, clustertools, clusterextra.
- Adding separate packages for built plugins: plugins-archive, plugins-blackhole
  plugins-example, and plugins-federated.
- Provides mysqlclient16{-devel}
- Requires mysqlclient15{-devel} on el5

* Mon Oct 08 2007 BJ Dierkes <wdierkes@rackspace.com> - 5.1.22-rc.1.rs
- Latest sources from MySQL upstream (Release Candidate)
- Patch Patch303: mysql-5.0.33-libtool.patch re-written as
  Patch303: mysql-5.1.22-rc-libtool.patch
- Removed patch Patch205: mysql-5.0.27-no-atomic.patch (applied upstream)
- Removed Patch6: mysql-rpl_ddl.patch, Patch7: mysql-rpl-test.patch
  (rpl tests no longer exist).
- Removed Patch209: mysql-5.0.45-disabled-tests.patch
- Configure option --with-openssl deprecated, modified to be --with-ssl

