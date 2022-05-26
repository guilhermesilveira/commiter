sudo apt update
sudo apt-get install -y cmake libssh2 pkg-config

wget https://github.com/libgit2/libgit2/archive/refs/tags/v1.4.3.zip
unzip -q v1.4.3.zip
mkdir -p libgit2-1.4.3/build
pushd libgit2-1.4.3/build || exit 1
cmake ..
cmake --build .
sudo cmake --install .
sudo ldconfig
python -c 'import pygit2'
popd || exit 1

# Very often the "make" is followed by "sudo make install" and very often the include files are then put in "/usr/local/include" and the libraries in "/usr/local/lib".
#This is to separate from libraries installed from the repositories which mainly uses "/usr/include" and "/usr/lib

#sudo apt-get install -y libgit2-dev
