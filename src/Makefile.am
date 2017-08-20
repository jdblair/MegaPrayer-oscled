SUBDIRS = @PLATFORM_SERIAL@
bin_PROGRAMS = swrite oscled oscconfig # test
swrite_SOURCES = swrite-main.cpp PlatformSerialFactory.h IPlatformSerial.h
swrite_LDADD = @PLATFORM_SERIAL@/libPlatformSerial.a -lpthread @PLATFORM_SERIAL_LIBS@
oscled_SOURCES = OSCServer.cpp OSCServer.h OSCLedConfig.cpp OSCLedConfig.hpp jsoncpp.cpp oscled-main.cpp PlatformSerialFactory.h IPlatformSerial.h
oscled_LDADD = @PLATFORM_SERIAL@/libPlatformSerial.a -lpthread @PLATFORM_SERIAL_LIBS@
oscled_SYSCONF = oscled.json
oscconfig_SOURCES = oscledconfig-main.cpp OSCLedConfig.cpp OSCLedConfig.hpp jsoncpp.cpp
oscconfig_LDADD = @PLATFORM_SERIAL@/libPlatformSerial.a -lpthread @PLATFORM_SERIAL_LIBS@
# test_SOURCES = CircularBuffer.cpp Test_CircularBuffer.cpp runTest.cpp
# test_LDADD = -lcppunit -lpthread
# # this next flag is apparently needed to work around a bug in g++4.8
# test_LDFLAGS = -Wl,--no-as-needed

