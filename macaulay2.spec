Name:		macaulay2
Version:	1.4
Release:	%mkrel 1
Group:		Sciences/Mathematics
License:	GPL
Summary:	A software system for research in algebraic geometry 
Source:		http://www.math.uiuc.edu/Macaulay2/Downloads/SourceCode/Macaulay2-1.4-r12617-src.tar.bz2
URL:		http://www.math.uiuc.edu/Macaulay2
Source1:	http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/Factory/factory-3-1-1.tar.gz
Source2:	http://www.mathematik.uni-kl.de/ftp/pub/Math/Singular/Libfac/libfac-3-1-1.tar.gz
Source3:	http://www.math.uiuc.edu/Macaulay2/Downloads/OtherSourceCode/1.4/frobby_v0.8.2.tar.gz
Source4:	http://www.math.uiuc.edu/Macaulay2/Downloads/OtherSourceCode/1.4/4ti2-1.3.2.tar.gz
Source5:	http://www.math.uiuc.edu/Macaulay2/Downloads/OtherSourceCode/1.4/normaliz2.5Source.zip
Source6:	http://www.math.uiuc.edu/Macaulay2/Downloads/OtherSourceCode/1.4/nauty24r2.tar.gz
Source7:	http://www.math.uiuc.edu/Macaulay2/Downloads/OtherSourceCode/1.4/lrslib-042c.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

# etags
BuildRequires:	bison flex
BuildRequires:	cddlib-devel
BuildRequires:	emacs-common
BuildRequires:	gcc-gfortran
BuildRequires:	gfan
BuildRequires:	glpk-devel
BuildRequires:	gmp-devel
BuildRequires:	gmpxx-devel
BuildRequires:	help2man
BuildRequires:	info-install
BuildRequires:	libatlas-devel
BuildRequires:	libatomic_ops-devel
BuildRequires:	libgc-devel
BuildRequires:	libgdbm-devel
BuildRequires:	liblapack-devel
BuildRequires:	libxml2-devel
BuildRequires:	mpfr-devel
BuildRequires:	ncurses-devel
BuildRequires:	ntl-devel
BuildRequires:	libpari-devel
BuildRequires:	readline-devel
BuildRequires:	singular-devel
BuildRequires:	texinfo

Requires:	cdd
Requires:	gfan

# uses smaller numbers for the test/example or x86_64 ntl will
# cause a fatal error
Patch0:		Macaulay2-1.4-ntl-5.5.2-x86_64.patch

# search cddlib headers in mandriva install directory
Patch1:		Macaulay2-1.4-cddlib.patch

# use mandriva gfan package
Patch2:		Macaulay2-1.4-gfan.patch

# use gmp
Patch3:		Macaulay2-1.4-mpir.patch
Patch4:		Macaulay2-1.4-gc.patch

%description
Macaulay 2 is a software system devoted to supporting research in algebraic
geometry  and commutative algebra, whose creation has been funded by the
National Science Foundation since 1992.
Macaulay 2 includes core algorithms for computing Gröbner bases and graded
or multi-graded free resolutions of modules over quotient rings of graded
or multi-graded polynomial rings with a monomial ordering. The core
algorithms are accessible through a versatile high level interpreted user
language with a powerful debugger supporting the creation of new classes of
mathematical objects and the installation of methods for computing
specifically with them. Macaulay 2 can compute Betti numbers, Ext,
cohomology of coherent sheaves on projective varieties, primary
decomposition of ideals, integral closure of rings, and more. 

%package	doc
Summary:	Macaulay2 documentation
Group:		Development/Other

%description	doc
Macaulay 2 is a software system devoted to supporting research in algebraic
geometry  and commutative algebra, whose creation has been funded by the
National Science Foundation since 1992.
This package provides Macaulay 2 documentation.

%prep
%setup -q -n Macaulay2-%{version}-r12617

%ifarch x86_64
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
# need install-info in $PATH
export PATH=/sbin:$PATH
mkdir -p BUILD/tarfiles
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} BUILD/tarfiles
perl -pi -e 's|(AC_SUBST\(MACHINE,").*("\))|$1%{_arch}$2|;' configure.ac

autoreconf -ifs
./configure --prefix=%{_prefix}		\
	--libdir=\${prefix}/%{_lib}	\
	--libexecdir=\${prefix}/%{_lib} \
	--disable-download

# avoid build failure due to some read only files
chmod -R u+w .
make

%install
# need install-info in $PATH
export PATH=/sbin:$PATH
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/M2
%dir %{_libdir}/Macaulay2
%{_libdir}/Macaulay2/*
%dir %{_datadir}/Macaulay2
%{_datadir}/Macaulay2/*
%{_mandir}/man1/M2.1*
%{_datadir}/emacs/site-lisp/*

%files		doc
%defattr(-,root,root)
%dir %{_docdir}/Macaulay2
%{_docdir}/Macaulay2/*
%{_infodir}/*
