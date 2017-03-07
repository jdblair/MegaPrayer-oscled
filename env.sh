#export CC=arm-linux-gnueabi-gcc-4.7
#export CXX=arm-linux-gnueabi-g++-4.7
export CC=arm-linux-gnueabihf-gcc-4.8
export CXX=arm-linux-gnueabihf-g++-4.8
export CFLAGS="-L$(pwd)/lib/arm-linux-gnueabihf/lib -I$(pwd)/lib/arm-linux-gnueabihf/include"
export CXXFLAGS="-L$(pwd)/lib/arm-linux-gnueabihf/lib -I$(pwd)/lib/arm-linux-gnueabihf/include"
