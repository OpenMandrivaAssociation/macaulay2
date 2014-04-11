#/bin/bash

DATE=$(date +%Y%m%d)

VERSION=1.5

MODULE="$(basename $0 -svn_checkout.sh)-$VERSION"

set -x
rm -rf $MODULE
# app
svn export  svn://svn.macaulay2.com/Macaulay2/release-branches/$VERSION/M2 $MODULE

tar cJf $MODULE-${DATE}.tar.xz $MODULE


# cleanup
rm -rf $MODULE

