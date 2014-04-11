#!/bin/sh

for ETAGS in etags.emacs etags ; do
 test -x /usr/bin/$ETAGS && exec /usr/bin/$ETAGS ${1+"$@"}
done

exit 1
