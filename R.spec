Name: R
Version: 2.8.0
Release: 1%{?dist}
Summary: A language for data analysis and graphics
URL: http://www.r-project.org
Source0: ftp://cran.r-project.org/pub/R/src/base/R-2/R-%{version}.tar.gz
Source1: macros.R
Source2: R-make-search-index.sh
Patch1: R-2.7.2-filter_asoption.patch
# fix bzlib2 detection, sent upstream 10-26-2008
Patch2: R-2.8.0-HAVE_BZLIB_H.patch
License: GPLv2+
Group: Applications/Engineering
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gcc-gfortran
BuildRequires: gcc-c++, tetex-latex, texinfo-tex 
BuildRequires: libpng-devel, libjpeg-devel, readline-devel
BuildRequires: tcl-devel, tk-devel, ncurses-devel
BuildRequires: blas >= 3.0, pcre-devel, zlib-devel
BuildRequires: java-1.5.0-gcj, lapack-devel
BuildRequires: libSM-devel, libX11-devel, libICE-devel, libXt-devel
BuildRequires: bzip2-devel, libXmu-devel, cairo-devel
BuildRequires: gcc-objc
# R-devel will pull in R-core
Requires: R-devel = %{version}-%{release}
# libRmath-devel will pull in libRmath
Requires: libRmath-devel = %{version}-%{release}

%description
This is a metapackage that provides both core R userspace and 
all R development components.

R is a language and environment for statistical computing and graphics. 
R is similar to the award-winning S system, which was developed at 
Bell Laboratories by John Chambers et al. It provides a wide 
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package core
Summary: The minimal R components necessary for a functional runtime
Group: Applications/Engineering
Requires: xdg-utils, cups

# These are the submodules that R-core provides. Sometimes R modules say they
# depend on one of these submodules rather than just R. These are provided for 
# packager convenience.
Provides: R-base = %{version}
Provides: R-boot = 1.2
Provides: R-class = 7.2
Provides: R-cluster = 1.11.11
Provides: R-codetools = 0.2
Provides: R-datasets = %{version}
Provides: R-foreign = 0.8
Provides: R-graphics = %{version}
Provides: R-grDevices = %{version}
Provides: R-grid = %{version}
Provides: R-KernSmooth = 2.22
Provides: R-lattice = 0.17
Provides: R-MASS = 7.2
Provides: R-methods = %{version}
Provides: R-mgcv = 1.4
Provides: R-nlme = 3.1
Provides: R-nnet = 7.2
Provides: R-rpart = 3.1
Provides: R-spatial = 7.2
Provides: R-splines = %{version}
Provides: R-stats = %{version}
Provides: R-stats4 = %{version}
Provides: R-survival = 2.34
Provides: R-tcltk = %{version}
Provides: R-tools = %{version}
Provides: R-utils = %{version}
Provides: R-VR = 7.2

%description core
A language and environment for statistical computing and graphics.
R is similar to the award-winning S system, which was developed at
Bell Laboratories by John Chambers et al. It provides a wide
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%package devel
Summary: files for development of R packages.
Group: Applications/Engineering
Requires: R-core = %{version}-%{release}
# You need all the BuildRequires for the development version
Requires: gcc-c++, gcc-gfortran, tetex-latex, texinfo 
Requires: libpng-devel, libjpeg-devel, readline-devel, ncurses-devel
Requires: libSM-devel, libX11-devel, libICE-devel, libXt-devel
Requires: bzip2-devel, libXmu-devel, cairo-devel
Requires: tcl-devel, tk-devel, pkgconfig

%description devel
Install R-devel if you are going to develop or compile R packages.

%package -n libRmath
Summary: standalone math library from the R project
Group: Development/Libraries

%description -n libRmath
A standalone library of mathematical and statistical functions derived
from the R project.  This packages provides the shared libRmath library.

%package -n libRmath-devel
Summary: standalone math library from the R project
Group: Development/Libraries
Requires: libRmath = %{version}, pkgconfig

%description -n libRmath-devel
A standalone library of mathematical and statistical functions derived
from the R project.  This packages provides the static libRmath library
and header files.

%prep
%setup -q
%patch1 -p1 -b .filter-little-out
%patch2 -p1 -b .BZLIB_H

# Filter false positive provides.
cat <<EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} \
| grep -v 'File::Copy::Recursive' | grep -v 'Text::DelimMatch'
EOF
%define __perl_provides %{_builddir}/R-%{version}/%{name}-prov
chmod +x %{__perl_provides}

# Filter unwanted Requires:
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} \
| grep -v 'perl(Text::DelimMatch)'
EOF
%define __perl_requires %{_builddir}/R-%{version}/%{name}-req
chmod +x %{__perl_requires}

%build
# Add PATHS to Renviron for R_LIBS
echo 'R_LIBS=${R_LIBS-'"'%{_libdir}/R/library:%{_datadir}/R/library'"'}' >> etc/Renviron.in

export R_PDFVIEWER="%{_bindir}/xdg-open"
export R_PRINTCMD="lpr"
export R_BROWSER="%{_bindir}/xdg-open"

case "%{_target_cpu}" in
      x86_64|mips64|ppc64|powerpc64|sparc64|s390x)
          export CC="gcc -m64"
          export CXX="g++ -m64"
          export F77="gfortran -m64"
          export FC="gfortran -m64"
      ;;
      ia64|alpha|sh*)
          export CC="gcc"
          export CXX="g++"
          export F77="gfortran"
          export FC="gfortran"
      ;;
      *)
          export CC="gcc -m32"
          export CXX="g++ -m32"
          export F77="gfortran -m32"
          export FC="gfortran -m32"
      ;;    
esac

export FCFLAGS="%{optflags}"
( %configure \
    --with-system-zlib --with-system-bzlib --with-system-pcre \
    --with-lapack \
    --with-tcl-config=%{_libdir}/tclConfig.sh \
    --with-tk-config=%{_libdir}/tkConfig.sh \
    --enable-R-shlib \
    rdocdir=%{_docdir}/R-%{version} \
    rincludedir=%{_includedir}/R \
    rsharedir=%{_datadir}/R) \
 | grep -A30 'R is now' - > CAPABILITIES
make 
(cd src/nmath/standalone; make)
#make check-all
make pdf
make info

%install
make DESTDIR=${RPM_BUILD_ROOT} install install-info install-pdf
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir.old
install -p CAPABILITIES ${RPM_BUILD_ROOT}%{_docdir}/R-%{version}

#Install libRmath files
(cd src/nmath/standalone; make install DESTDIR=${RPM_BUILD_ROOT})

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/R/lib" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

mkdir -p $RPM_BUILD_ROOT%{_datadir}/R/library

# Install rpm helper macros
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm/
install -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/

# Install rpm helper script
mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm/
install -m0755 %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/rpm/

# Fix multilib
touch -r NEWS ${RPM_BUILD_ROOT}%{_docdir}/R-%{version}/CAPABILITIES
touch -r NEWS doc/manual/*.pdf
touch -r NEWS $RPM_BUILD_ROOT%{_bindir}/R

# Fix html/packages.html
# We can safely use RHOME here, because all of these are system packages.
sed -i 's|\..\/\..|%{_libdir}/R|g' $RPM_BUILD_ROOT%{_docdir}/R-%{version}/html/packages.html

for i in $RPM_BUILD_ROOT%{_libdir}/R/library/*/html/*.html; do
	sed -i 's|\..\/\..\/..\/doc|%{_docdir}/R-%{version}|g' $i
done

%files
# Metapackage

%files core
%defattr(-, root, root, -)
%{_bindir}/R
%{_bindir}/Rscript
%{_datadir}/R
%dir %{_libdir}/R
%{_libdir}/R/bin
%{_libdir}/R/etc
%{_libdir}/R/lib
%{_libdir}/R/library
%{_libdir}/R/modules
%{_libdir}/R/COPYING
%{_libdir}/R/NEWS
%{_libdir}/R/SVN-REVISION
/usr/lib/rpm/R-make-search-index.sh
%{_infodir}/R-*.info*
%{_sysconfdir}/rpm/macros.R
%{_mandir}/man1/*
%{_docdir}/R-%{version}
%docdir %{_docdir}/R-%{version}
/etc/ld.so.conf.d/*

%files devel
%defattr(-, root, root, -)
%{_libdir}/pkgconfig/libR.pc
%{_includedir}/R

%files -n libRmath
%defattr(-, root, root, -)
%{_libdir}/libRmath.so

%files -n libRmath-devel
%defattr(-, root, root, -)
%{_libdir}/libRmath.a
%{_includedir}/Rmath.h
%{_libdir}/pkgconfig/libRmath.pc

%clean
rm -rf ${RPM_BUILD_ROOT};

%post core
# Create directory entries for info files
# (optional doc files, so we must check that they are installed)
for doc in admin exts FAQ intro lang; do
   file=%{_infodir}/R-${doc}.info.gz
   if [ -e $file ]; then
      /sbin/install-info ${file} %{_infodir}/dir 2>/dev/null || :
   fi
done
/sbin/ldconfig
R CMD javareconf > /dev/null 2>&1 || exit 0

# Update package indices
%__cat %{_libdir}/R/library/*/CONTENTS > %{_docdir}/R-%{version}/html/search/index.txt 2>/dev/null
# Don't use .. based paths, substitute RHOME
sed -i "s!../../..!%{_libdir}/R!g" %{_docdir}/R-%{version}/html/search/index.txt

# This could fail if there are no noarch R libraries on the system.
%__cat %{_datadir}/R/library/*/CONTENTS >> %{_docdir}/R-%{version}/html/search/index.txt 2>/dev/null || exit 0
# Don't use .. based paths, substitute /usr/share/R
sed -i "s!../../..!/usr/share/R!g" %{_docdir}/R-%{version}/html/search/index.txt


%preun core
if [ $1 = 0 ]; then
   # Delete directory entries for info files (if they were installed)
   for doc in admin exts FAQ intro lang; do
      file=%{_infodir}/R-${doc}.info.gz
      if [ -e ${file} ]; then
         /sbin/install-info --delete R-${doc} %{_infodir}/dir 2>/dev/null || :
      fi
   done
fi

%postun core
/sbin/ldconfig

%post -n libRmath
/sbin/ldconfig

%postun -n libRmath
/sbin/ldconfig

%changelog
* Sun Oct 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.8.0-1
- Update to 2.8.0
- New subpackage layout: R-core is functional userspace, R is metapackage 
  requiring everything
- Fix system bzip2 detection

* Thu Oct 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.2-2
- fix sh compile (bz 464055)

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.2-1
- update to 2.7.2
- fix spec for alpha compile (bz 458931)
- fix security issue in javareconf script (bz 460658)

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.1-1
- update to 2.7.1

* Wed May 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-5
- add cairo-devel to BR/R, so that cairo backend gets built

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-4
- fixup sed invocation added in -3
- make -devel package depend on base R = version-release
- fix bad paths in package html files

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-3
- fix poorly constructed file paths in html/packages.html (bz 442727)

* Tue May 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-2
- add patch from Martyn Plummer to avoid possible bad path hardcoding in 
  /usr/bin/Rscript
- properly handle ia64 case (bz 446181)

* Mon Apr 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-1
- update to 2.70
- rcompgen is no longer a standalone package
- redirect javareconf to /dev/null (bz 442366)

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.2-1
- properly version the items in the VR bundle
- 2.6.2
- don't use setarch for java setup
- fix R post script file

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-4
- multilib handling (thanks Martyn Plummer)
- Update indices in the right place.

* Mon Jan  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-3
- move INSTALL back into R main package, as it is useful without the 
  other -devel bits (e.g. installing noarch package from CRAN)

* Tue Dec 11 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-2
- based on changes from Martyn Plummer <martyn.plummer@r-project.org>
- use configure options rdocdir, rincludedir, rsharedir 
- use DESTDIR at installation
- remove obsolete generation of packages.html
- move header files and INSTALL R-devel package

* Mon Nov 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.1-1
- bump to 2.6.1

* Tue Oct 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-3.1
- fix missing perl requires

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-3
- fix multilib conflicts (bz 343061)

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-2
- add R CMD javareconf to post (bz 354541)
- don't pickup bogus perl provides (bz 356071)
- use xdg-open, drop requires for firefox/evince (bz 351841)

* Thu Oct  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.6.0-1
- bump to 2.6.0

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.1-3
- fix license tag
- rebuild for ppc32

* Thu Jul  5 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.1-2
- add rpm helper macros, script

* Mon Jul  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.1-1
- drop patch, upstream fixed
- bump to 2.5.1

* Mon Apr 30 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.0-2
- patch from Martyn Plummer fixes .pc files
- add new BR: gcc-objc

* Wed Apr  25 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.0-1
- bump to 2.5.0

* Tue Mar  13 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-4
- get rid of termcap related requires, replace with ncurses
- use java-1.5.0-gcj instead of old java-1.4.2
- add /usr/share/R/library as a valid R_LIBS directory for noarch bits

* Sun Feb  25 2007 Jef Spaleta <jspaleta@gmail.com> 2.4.1-3
- rebuild for reverted tcl/tk

* Fri Feb  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-2
- rebuild for new tcl/tk

* Tue Dec 19 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.1-1
- bump to 2.4.1
- fix install-info invocations in post/preun (bz 219407)

* Fri Nov  3 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.0-2
- sync with patched 2006-11-03 level to fix PR#9339

* Sun Oct 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.4.0-1
- bump for 2.4.0

* Wed Sep 12 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.1-2
- bump for FC-6

* Fri Jun  2 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.1-1
- bump to 2.3.1

* Tue Apr 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.0-2
- fix ppc build for FC-4 (artificial bump for everyone else)

* Mon Apr 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.0-1
- bump to 2.3.0 (also, bump module revisions)

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-5
- now BR is texinfo-tex, not texinfo in rawhide

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-4
- bump for FC-5

* Mon Jan  9 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-3
- fix BR: XFree86-devel for FC-5

* Sat Dec 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-2
- missing BR: libXt-devel for FC-5

* Tue Dec 20 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.1-1
- bump to 2.2.1

* Thu Oct  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.0-2
- use fixed system lapack for FC-4 and devel

* Thu Oct  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.2.0-1
- bump to 2.2.0

* Mon Jul  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.1-2
- fix version numbers on supplemental package provides

* Mon Jun 20 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.1-1
- bugfix update

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-51
- proper library handling

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-50
- 2.1.0, fc4 version.
- The GNOME GUI is unbundled, now provided as a package on CRAN

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-50
- big bump. This is the fc4 package, the fc3 package is 2.0.1-11
- enable gnome gui, add requires as needed

* Thu Apr 14 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-10
- bump for cvs errors

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-9
- fix URL for Source0

* Mon Apr 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-8
- spec file cleanup

* Fri Apr  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-7
- use evince instead of ggv
- make custom provides for R subfunctions

* Wed Mar 30 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-6
- configure now calls --enable-R-shlib

* Thu Mar 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.1-5
- cleaned up package for Fedora Extras

* Mon Feb 28 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.4
- Fixed file ownership in R-devel and libRmath packages

* Wed Feb 16 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.3
- R-devel package is now a stub package with no files, except a documentation
  file (RPM won't accept sub-packages with no files). R now conflicts
  with earlier (i.e 0:2.0.1-0.fdr.2) versions of R-devel.
- Created libRmath subpackage with shared library.

* Mon Jan 31 2005 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.2
- Created R-devel and libRmath-devel subpackages

* Mon Nov 15 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.1-0.fdr.1
- Built R 2.0.1

* Wed Nov 10 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.3
- Set R_PRINTCMD at configure times so that by default getOption(printcmd)
  gives "lpr".
- Define macro fcx for all Fedora distributions. This replaces Rinfo

* Tue Oct 12 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.2
- Info support is now conditional on the macro Rinfo, which is only
  defined for Fedora 1 and 2. 

* Thu Oct 7 2004 Martyn Plummer <plummer@iarc.fr> 0:2.0.0-0.fdr.1
- Built R 2.0.0
- There is no longer a BUGS file, so this is not installed as a 
  documentation file.

* Mon Aug  9 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.1-0.fdr.4
- Added gcc-g++ to the list of BuildRequires for all platforms.
  Although a C++ compiler is not necessary to build R, it must
  be present at configure time or R will not be correctly configured
  to build packages containing C++ code.

* Thu Jul  1 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.1-0.fdr.3
- Modified BuildRequires so we can support older Red Hat versions without
  defining any macros.

* Mon Jun 23 2004 Martyn Plummer <plummner@iarc.fr> 0:1.9.1-0.fdr.2
- Added libtermcap-devel as BuildRequires for RH 8.0 and 9. Without
  this we get no readline support.

* Mon Jun 21 2004 Martyn Plummer <plummner@iarc.fr> 0:1.9.1-0.fdr.1
- Build R 1.9.1
- Removed Xorg patch since fix is now in R sources

* Mon Jun 14 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.4
- Added XFree86-devel as conditional BuildRequires for rh9, rh80

* Wed Jun 08 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.3
- Corrected names for fc1/fc2/el3 when using conditional BuildRequires
- Configure searches for C++ preprocessor and fails if we don't have
  gcc-c++ installed. Added to BuildRequires for FC2.

* Tue Jun 08 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.2
- Added patch to overcome problems with X.org headers (backported
  from R 1.9.1; patch supplied by Graeme Ambler)
- Changed permissions of source files to 644 to please rpmlint

* Tue May 03 2004 Martyn Plummer <plummer@iarc.fr> 0:1.9.0-0.fdr.1
- R.spec file now has mode 644. Previously it was unreadable by other
  users and this was causing a crash building under mach.
- Changed version number to conform to Fedora conventions. 
- Removed Provides: and Obsoletes: R-base, R-recommended, which are
  now several years old. Nobody should have a copy of R-base on a 
  supported platform.
- Changed buildroot to Fedora standard
- Added Requires(post,preun): info
- Redirect output from postinstall/uninstall scripts to /dev/null
- Added BuildRequires tags necessary to install R with full 
  capabilities on a clean mach buildroot. Conditional buildrequires
  for tcl-devel and tk-devel which were not present on RH9 or earlier.

* Thu Apr 01 2004 Martyn Plummer <plummer@iarc.fr>
- Added patch to set environment variable LANG to C in shell wrapper,
  avoiding warnings about UTF-8 locale not being supported

* Mon Mar 15 2004 Martyn Plummer <plummer@iarc.fr>
- No need to export optimization flags. This is done by %configure
- Folded info installation into %makeinstall 
- Check that RPM_BASE_ROOT is not set to "/" before cleaning up

* Thu Feb 03 2004 Martyn Plummer <plummer@iarc.fr>
- Removed tcl-devel from BuildRequires

* Tue Feb 03 2004 Martyn Plummer <plummer@iarc.fr>
- Changes from James Henstridge <james@daa.com.au> to allow building on IA64:
- Added BuildRequires for tcl-devel tk-devel tetex-latex
- Use the %configure macro to call the configure script
- Pass --with-tcl-config and --with-tk-config arguments to configure
- Set rhome to point to the build root during "make install"

* Wed Jan 07 2004 Martyn Plummer <plummer@iarc.fr>
- Changed obsolete "copyright" field to "license"

* Fri Nov 21 2003 Martyn Plummer <plummer@iarc.fr>
- Built 1.8.1
