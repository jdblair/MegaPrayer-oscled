SUBDIRS = @PLATFORM_SERIAL@
bin_PROGRAMS = led test
led_SOURCES = main.cpp CircularBuffer.cpp
led_LDADD = @PLATFORM_SERIAL@/libPlatformSerial.a -lpthread
test_SOURCES = CircularBuffer.cpp Test_CircularBuffer.cpp runTest.cpp
test_LDADD = -lcppunit -lpthread
# this next flag is apparently needed to work around a bug in g++4.8
test_LDFLAGS = -Wl,--no-as-needed
