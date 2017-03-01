SUBDIRS = @PLATFORM_SERIAL@
bin_PROGRAMS = led
led_SOURCES = main.cpp CircularBuffer.cpp
led_LDADD = @PLATFORM_SERIAL@/libPlatformSerial.a -lpthread
