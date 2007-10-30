PREFIX=$PWD
#SVNVER=`svn info | grep "Revision: [0-9]*" | tr -d \  | cut -f2 -d:`
SVNVER=4342
rm -rf $PREFIX/build
rm -rf $PREFIX/dist
python setup.py sdist
(cd $PREFIX/dist && tar -xzf numpy-1.0.4.dev$SVNVER.tar.gz)
(cd $PREFIX/dist/numpy-1.0.4.dev$SVNVER && python setup.py scons)

