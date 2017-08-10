# Introduction

*oscled* is the LED control software for the [MegaPrayer
 Rosary](http://www.hatchfund.org/project/megaprayer).

# License

oscled is licensed for use under the GNU Public License V2.

# Building

oscled is a C++ project that is configured using autotools.

## Prerequisites

* g++
* arm-linux-gnueabihf c++ cross-compiler (to build oscled for ARM boards)
* make
* autoconf
* automake 
* [liblo](https://github.com/radarsat1/liblo/)
* gtk+ and goocanvas
* tkinter
* python 3

This should install everything necessary on Ubuntu, with the exception of liblo, python 3, and tkinter:

`apt-get install build-essential autoconf libgoocanvas-dev g++-arm-linux-gnueabihf`

### Building liblo

Download liblo from github at 
https://github.com/radarsat1/liblo

Extract the files and cd into the directory

```
./configure
make
make check
sudo make install
```

## Generate the configure script

At the top level, run:

```
autoreconf --install
```

This will generate the configure script.

## Configuring

Here are some easy recipes:

### GtkSim (the GTK2+ Rosary Simulator)

*From the top-level directory:*

```
mkdir build-gtksim-x86
cd build-gtksim-x86
../configure --enable-serial=gtksim
make
```

### Orange Pi

To configure to cross-compile for arm (set VERSION to the version of gcc you have installed):

```
export VERSION=-4.9
export HOST=arm-linux-gnueabihf
export CC=${HOST}-gcc${VERSION}
export CXX=${HOST}-g++${VERSION}
export CFLAGS="-L$(pwd)/lib/${HOST}/lib -I$(pwd)/lib/arm-linux-gnueabihf/include"
export CXXFLAGS="-L$(pwd)/lib/${HOST}/lib -I$(pwd)/lib/arm-linux-gnueabihf/include"
export PREFIX=$(pwd)/lib/${HOST}
```

This is provided in the `env.sh` script at the top level of the repo.

To cross-compile for the orange pi:

```
mkdir build-opi-arm
cd build-opi-arm
../configure --enable-serial=opi --host $HOST
make
```

### Open Lighting (OLA) DMX control

You will need install OLA's prerequisites, and then build OLA for your system.

#### Installing the OLA package

If you don't want to build OLA:

```
$ cat /etc/apt/sources.list
deb http://apt.openlighting.org/ubuntu trusty main

sudo apt-get install ola
```

#### Prerequisites & Build

```
sudo apt-get install libcppunit-doc libcppunit-dev libossp-uuid-dev libossp-uuid16 libprotoc-dev libftdi-dev

git clone https://github.com/OpenLightingProject/ola.git

cd ola
git log # Tested at: 7eb53beeaa577aab2e2196303a8beae492b637ad

./configure --enable-python-libs && make -j2 check
sudo (make install && ldconfig)

```

#### Configure OLA

TODO


#### Mapping Your devices


### Testing OLA

```
cd MegaPrayer-oscled/python 
oscsend localhost 5005 /beadf ifff 0 1 1 1
aqk@monolith ~/code/MegaPrayer-oscled/python $ oscsend localhost 5005 /update

cd code/MegaPrayer-oscled/python 
$ python3 server.py --ip 127.0.0.1 --port=5005

Make first light cyan, and second light green:
src/swrite 0  0 255 255 10 0 0 255 0 10 0

swrite [interface] r g b w s    r g b w s
red green blue white strobe

Make the first light strobe white
src/swrite 0 255 255 255 255 255
```


# python/mp.py

mp.py is the MegaPrayer control program.

## Dependencies

* python3
* pythonosc

### pythonosc

Download and install [pythonosc](https://pypi.python.org/pypi/python-osc).

Note: I found that the libosc package had to be installed as root, but this resulted in the wrong
file permissions for ` /usr/local/lib/python3.4/dist-packages/pythonosc/`.

If, after installing the library, python tells you the library is not found, add world read permissions:

```
chmod a+r -R /usr/local/lib/python3.4/dist-packages/pythonosc/
```
