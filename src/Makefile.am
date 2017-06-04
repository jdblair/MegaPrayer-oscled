SUBDIRS = @PLATFORM_SERIAL@
bin_PROGRAMS = swrite oscled # test
swrite_SOURCES = swrite-main.cpp PlatformSerialFactory.h IPlatformSerial.h
swrite_LDADD = @PLATFORM_SERIAL@/libPlatformSerial.a -lpthread $(GOOCANVAS_LIBS)
oscled_SOURCES = OSCServer.cpp OSCServer.h OSCLedConfig.cpp OSCLedConfig.hpp jsoncpp.cpp oscled-main.cpp PlatformSerialFactory.h IPlatformSerial.h
oscled_LDADD = @PLATFORM_SERIAL@/libPlatformSerial.a -lpthread $(GOOCANVAS_LIBS)
oscled_SYSCONF = oscled.json
EXTRA_DIST = gtksim json opi rpi skeleton
# test_SOURCES = CircularBuffer.cpp Test_CircularBuffer.cpp runTest.cpp
# test_LDADD = -lcppunit -lpthread
# # this next flag is apparently needed to work around a bug in g++4.8
# test_LDFLAGS = -Wl,--no-as-needed

