#!/bin/sh

WHEELS=wheelstash/
PKG=pkgstage/

rm -fr wheels
pip wheel --wheel-dir=${WHEELS} .
pip install --use-wheel --no-index --find-links=${WHEELS} ensign
find ${PKG}usr/local/ensign -type f -or -type l | awk '{ sub(/pkgstage/, ""); print }' > plist
pkg create -M .pkgfiles/MANIFEST -p plist -r ${PKG} -o .
