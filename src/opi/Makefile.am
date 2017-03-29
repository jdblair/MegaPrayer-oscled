noinst_LIBRARIES = libPlatformSerial.a
libPlatformSerial_a_SOURCES = PlatformSerialFactory.cpp PlatformSerial.h PlatformSerial.cpp event_gpio.c common.c gpio_lib.c gpio_lib.h
bin_PROGRAMS = test
test_SOURCES = gpio_lib.c test.c
libPlatformSerial_a_CXXFLAGS = -I$(top_srcdir)/src @AM_CXXFLAGS@
