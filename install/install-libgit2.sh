sudo apt update
sudo apt-get install -y cmake libssh2 pkg-config libssh2-1-dev libssh2-1 libssl-dev

wget https://github.com/libgit2/libgit2/archive/refs/tags/v1.4.3.zip
unzip -q v1.4.3.zip
mkdir -p libgit2-1.4.3/build
pushd libgit2-1.4.3/build || exit 1
#cmake ..
#cmake --build .
cmake -DUSE_SSH=ON ..
cmake --build .
sudo cmake --install .
#cmake --build . --target install
#cmake -DUSE_SSH=ON --build . --target install
sudo ldconfig
python -c 'import pygit2'
python -c 'import pygit2; bool(pygit2.features & pygit2.GIT_FEATURE_SSH)'
popd || exit 1

# Very often the "make" is followed by "sudo make install" and very often the include files are then put in "/usr/local/include" and the libraries in "/usr/local/lib".
#This is to separate from libraries installed from the repositories which mainly uses "/usr/include" and "/usr/lib

#sudo apt-get install -y libgit2-dev
