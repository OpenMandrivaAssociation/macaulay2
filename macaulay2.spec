%define snap 20130401
%define svn r15955

%global emacs_sitelisp  %{_datadir}/emacs/site-lisp/
%global xemacs_sitelisp %{_datadir}/xemacs/site-packages/lisp/
%global ISSUE OpenMandriva
%global M2_machine %{_target_cpu}-Linux-%{ISSUE}

%global INFO_FILES AdjointIdeal BGG BIBasis BeginningMacaulay2 Benchmark Binomials BoijSoederberg BooleanGB Browse Bruns ChainComplexExtras CharacteristicClasses Classic ConvexInterface ConwayPolynomials Cyclotomic DGAlgebras Depth Dmodules EdgeIdeals Elimination FirstPackage FormalGroupLaws FourTiTwo FourierMotzkin GenericInitialIdeal GraphicalModels Graphics Graphs HodgeIntegrals HyperplaneArrangements IntegralClosure InvolutiveBases Kronecker KustinMiller LLLBases LexIdeals LocalRings Macaulay2Doc MapleInterface Markov ModuleDeformations MonomialAlgebras MonomialMultiplierIdeals NAGtypes NoetherNormalization NormalToricVarieties Normaliz NumericalAlgebraicGeometry OpenMath PHCpack PackageTemplate Parametrization Parsing PieriMaps Points Polyhedra Polymake Posets PrimaryDecomposition QthPower RandomCanonicalCurves RandomCurves RandomGenus14Curves RandomObjects RandomPlaneCurves RandomSpaceCurves RationalPoints ReesAlgebra Regularity SCSCP SRdeformations Schubert2 SchurFunctors SchurRings Serialization SimpleDoc SimplicialComplexes SimplicialDecomposability StatePolytope Style SymmetricPolynomials TangentCone TensorComplexes Text ToricVectorBundles Units VersalDeformations WeylGroups XML gfanInterface
 
Summary: System for algebraic geometry and commutative algebra
Name:    macaulay2
Version: 1.5
Release: 1%{?dist}

License: GPLv2 or GPLv3

URL:     http://www.math.uiuc.edu/Macaulay2/
# the SVN revision is being used as a unique ID
Source0: http://www.math.uiuc.edu/Macaulay2/Downloads/SourceCode/Macaulay2-%{version}-%{svn}-src.tar.bz2
#Source0: Macaulay2-1.5-%{svn}.tar.xz
Source1: Macaulay2-svn_checkout.sh
# TEMPORARY: remove this when Macaulay ships the updated version
Source2: Normaliz.m2

Source10: Macaulay2.png
Source11: Macaulay2.desktop
Source20: etags.sh
Source100: %{name}.rpmlintrc

Patch1: Macaulay2-1.4-xdg_open.patch
# work harder to set ADDR_NO_RANDOMIZE, http://bugzilla.redhat.com/201739
Patch2: Macaulay2-1.5-ADDR_NO_RANDOMIZE.patch
# nauty has bad licensing
Patch3:  Macaulay2-1.5-no_nauty.patch
# drop 'html-check-links' 'tests' from default make target
# the former is broken since we omit nauty (see above).
Patch4: Macaulay2-1.5-default_make_targets.patch
# disable check for gftables
Patch5: Macaulay2-1.5-no_gftables.patch
# don't use -Werror 
Patch6: Macaulay2-1.5-no_Werror.patch
# use fedora/system copy of normaliz
Patch8: Macaulay2-1.5-system_normaliz.patch
# link to gmp, not mpir to avoid possible issues with gmp'ed pari
Patch9: Macaulay2-1.5-use_gmp_instead_of_mpir.patch
# fix build against factory-3.1.5
Patch10: Macaulay2-1.5-factory_315.patch

BuildRequires: 4ti2
BuildRequires: autoconf
BuildRequires: bison
BuildRequires: blas-devel
BuildRequires: boost-devel
BuildRequires: cddlib-devel
BuildRequires: desktop-file-utils
BuildRequires: doxygen
# etags
BuildRequires: emacs-common
BuildRequires: flex
BuildRequires: flint-devel
BuildRequires: gawk
BuildRequires: gcc-gfortran
BuildRequires: gmpxx-devel
BuildRequires: gdbm-devel
BuildRequires: gfan
BuildRequires: glpk-devel
BuildRequires: info
BuildRequires: factory-static factory-devel
BuildRequires: factory-gftables
BuildRequires: libatlas-devel
BuildRequires: libatomic_ops-devel
BuildRequires: libfac-static libfac-devel
BuildRequires: lapack-devel
BuildRequires: mpfr-devel gmp-devel
BuildRequires: normaliz
BuildRequires: ntl-devel
BuildRequires: libpari-devel
BuildRequires: pkgconfig(bdw-gc) 
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(ncurses)
BuildRequires: readline-devel 
BuildRequires: texinfo
BuildRequires: time

Requires: 4ti2
Requires: gfan
Requires: factory-gftables
Requires: normaliz
# M2-help
Requires: xdg-utils
%rename macaulay2-doc

%description
Macaulay 2 is a new software system devoted to supporting research in
algebraic geometry and commutative algebra written by Daniel R. Grayson
and Michael E. Stillman

%prep
%setup -q  -n Macaulay2-%{version}-%{svn}/M2

# TEMPORARY: remove this when Macaulay ships the updated version
cp -p %{SOURCE2} Macaulay2/packages

install -p -m755 %{SOURCE20} ./etags

mkdir -p BUILD/tarfiles/

%patch1 -p1 -b .xdg_open
%patch2 -p1 -b .ADDR_NO_RANDOMIZE
%patch3 -p1 -b .no_nauty
%patch4 -p1 -b .default_make_targets
%patch5 -p1 -b .no_gftables
%patch6 -p1 -b .no_Werror
%patch8 -p1 -b .system_normaliz
%patch9 -p1 -b  .use_gmp_instead_of_mpir
%patch10 -p1 -b .factory_315

# (re)generate configure
[ -f configure -a -f include/config.h ] || make

# factory-gftables symlink
mkdir -p BUILD/%{_target_platform}/StagingArea/common/share/Macaulay2/Core
pushd    BUILD/%{_target_platform}/StagingArea/common/share/Macaulay2/Core
ln -s /usr/share/factory/gftables factory
popd

# helper binaries (4ti2, normaliz)
mkdir -p BUILD/%{_target_platform}/StagingArea/%{M2_machine}/libexec/Macaulay2/%{M2_machine}
pushd    BUILD/%{_target_platform}/StagingArea/%{M2_machine}/libexec/Macaulay2/%{M2_machine}
for bin in `rpm -ql 4ti2 | grep /usr/bin` %{_bindir}/normaliz ; do
if [ -x "${bin}" ]; then
  ln -s "${bin}"
else
  echo "WARNING: target ${bin} not executable!"
fi
done
popd

# Increase timeouts for slower CPUs (e.g., ARM)
sed -i.timeout 's/-t 350/-t 1000/' Macaulay2/m2/html.m2
touch -r Macaulay2/m2/html.m2.timeout Macaulay2/m2/html.m2


%build

# We need /sbin:. in PATH to find install-info,etags
PATH=/sbin:$(pwd):$PATH; export PATH

## configure macro currently broken, due to some odd prefix-checks.  probably fixable -- Rex
mkdir -p BUILD/%{_target_platform}
pushd BUILD/%{_target_platform}
CPPFLAGS="-I%{_includedir}/factory" \
CFLAGS="%{optflags}" \
CXXFLAGS="%{optflags}" \
LDFLAGS="$RPM_LD_FLAGS -Wl,--as-needed" \
LIBS="-lflint" \
../../configure \
  --build=%{_build} \
  --host=%{_host} \
  --with-issue=%{ISSUE} \
  --prefix=%{_prefix} \
  --disable-dumpdata \
  --enable-shared \
  --disable-fc-lib-ldflags \
  --disable-strip \
  --disable-frobby \
  --with-unbuilt-programs="cddplus gfan 4ti2 lrslib nauty normaliz" 
popd

# Not smp-safe
make Verbose=true -C BUILD/%{_target_platform}
# IgnoreExampleErrors=true


%install
# We need /sbin:. in PATH to find install-info,etags
PATH=/sbin:$(pwd):$PATH; export PATH
mkdir -p %{buildroot}%{_libexecdir}/Macaulay2

make install DESTDIR=%{buildroot} -C BUILD/%{_target_platform}
# IgnoreExampleErrors=true

# app img
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/Macaulay2.png

desktop-file-install --vendor ="" \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE11}

# Make a new home for emacs files
mkdir -p %{buildroot}%{_datadir}/Macaulay2/emacs
mv %{buildroot}%{emacs_sitelisp}/M2*.el %{buildroot}%{_datadir}/Macaulay2/emacs/
 
for dir in %{emacs_sitelisp} %{xemacs_sitelisp} ; do
  install -d -m755 %{buildroot}$dir
  pushd %{buildroot}%{_datadir}/Macaulay2/emacs
  for file in M2*.el ; do
    ln -s %{_datadir}/Macaulay2/emacs/$file %{buildroot}$dir
    touch %{buildroot}$dir/`basename $file .el`.elc
  done
  popd
done

## unpackaged files
# info dir
rm -fv %{buildroot}%{_infodir}/dir
# Empty files - indicating test passes
rm -fv %{buildroot}%{_datadir}/Macaulay2/Macaulay2Doc/basictests/*.okay


%check
time make -k check -C BUILD/%{_target_platform} ||:

%files
%{_bindir}/M2
%{_datadir}/applications/*Macaulay2.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_infodir}/*.info*
%dir %{_prefix}/lib/Macaulay2/
%{_prefix}/lib/Macaulay2/%{M2_machine}
%dir %{_libexecdir}/Macaulay2/
%{_libexecdir}/Macaulay2/%{M2_machine}
%{_mandir}/man1/*
%ghost %{emacs_sitelisp}
%ghost %{xemacs_sitelisp}
%{_datadir}/Macaulay2/
%{_docdir}/Macaulay2/
