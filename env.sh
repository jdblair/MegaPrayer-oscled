export VERSION=-4.9
export HOST=arm-linux-gnueabihf
export CC=${HOST}-gcc${VERSION}
export CXX=${HOST}-g++${VERSION}
export CFLAGS="-L$(pwd)/lib/${HOST}/lib -I$(pwd)/lib/arm-linux-gnueabihf/include"
export CXXFLAGS="-L$(pwd)/lib/${HOST}/lib -I$(pwd)/lib/arm-linux-gnueabihf/include"
export PREFIX=$(pwd)/lib/${HOST}
