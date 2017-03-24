SUBDIRS = @PLATFORM_SERIAL@
bin_PROGRAMS = swrite oscled # test
swrite_SOURCES = swrite-main.cpp 
swrite_LDADD = @PLATFORM_SERIAL@/libPlatformSerial.a -lpthread $(GOOCANVAS_LIBS)
oscled_SOURCES = oscled-main.cpp OSCServer.cpp
oscled_LDADD = @PLATFORM_SERIAL@/libPlatformSerial.a -lpthread $(GOOCANVAS_LIBS)
# test_SOURCES = CircularBuffer.cpp Test_CircularBuffer.cpp runTest.cpp
# test_LDADD = -lcppunit -lpthread
# # this next flag is apparently needed to work around a bug in g++4.8
# test_LDFLAGS = -Wl,--no-as-needed

