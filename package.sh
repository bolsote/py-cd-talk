#!/bin/sh

WHEELS=wheelstash/
PKG=pkgstage
PREFIX=${PKG}/usr/local/ensign

rm -fr wheels
pip wheel --wheel-dir=${WHEELS} .
pip install --use-wheel --no-index --find-links=${WHEELS} ensign

cp dev.ini README.* ${PREFIX}
rm -fr ${PREFIX}/log

find ${PREFIX}/bin -type f -exec sed -i.bak "s:/.*/usr/local/ensign:/usr/local/ensign:g" {} +
rm -f ${PREFIX}/bin/*.bak

find ${PREFIX} -type f -or -type l | awk '{ sub(/pkgstage/, ""); print }' > plist
pkg create -M .pkgfiles/MANIFEST -p plist -r ${PKG} -o .

mkdir bin
mv ensign-*.txz bin/

rm -fr pkgstage
