export VERSION=-4.8
export HOST=arm-linux-gnueabihf
export CC=${HOST}-gcc${VERSION}
export CXX=${HOST}-g++${VERSION}
export CFLAGS="-L$(pwd)/lib/${HOST}/lib -L/opt/ola/lib -I$(pwd)/lib/arm-linux-gnueabihf/include -I/opt/ola/include"
export CXXFLAGS="-L$(pwd)/lib/${HOST}/lib -L/opt/ola/lib -I$(pwd)/lib/arm-linux-gnueabihf/include -I/opt/old/include"
export PREFIX=$(pwd)/lib/${HOST}
