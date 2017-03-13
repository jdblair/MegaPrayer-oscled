AC_INIT([led], [1.0], [jdb@moship.net])
AM_INIT_AUTOMAKE([-Wall -Werror foreign])
AC_PROG_CC
AC_PROG_CXX
AC_PROG_RANLIB
AM_PROG_AR

AC_SUBST([AM_CXXFLAGS], [-std=c++11])

AC_ARG_ENABLE([serial],
        [AS_HELP_STRING([--enable-serial],
                [specify the platform serial interface])],
        [],
        [enable_serial=skeleton])
AC_DEFINE_UNQUOTED([USE_PLATFORM_SERIAL], "$enable_serial", [platform serial interface])
PLATFORM_SERIAL=$enable_serial
AC_SUBST(PLATFORM_SERIAL)

AC_ARG_ENABLE(debug, [  --enable-debug          Enable debug compiler flags])
if test x"$enable_debug" = "xyes"; then

    for i in $CFLAGS; do
        if ! ((test x"$i" = x-g) || (test x"$i" = x-O2)); then
            CF="$CF $i"
        fi
    done
	CFLAGS="$CF -O0 -g -Wall -Werror -DDEBUG"
    CF=""
    for i in $CXXFLAGS; do
        if ! ((test x"$i" = x-g) || (test x"$i" = x-O2)); then
            CF="$CF $i"
        fi
    done
	CXXFLAGS="$CF -O0 -g -Wall -Werror -DDEBUG"
fi

AC_CHECK_LIB(lo,lo_server_thread_new,[],
        [AC_MSG_ERROR([unable to find liblo osc server library (see http://liblo.sourceforge.net/)])],[-lpthread])

AC_ARG_WITH([gtk], AS_HELP_STRING([--with-gtk], [Build with the GTK+ interface (required for gtksim)]))

AS_IF([test "x$with_gtk" = "xyes"], [
   PKG_CHECK_MODULES([GTK], [gtk+-2.0])
   PKG_CHECK_MODULES([GOOCANVAS], [goocanvas])
])

PKG_CHECK_MODULES([GLIB], [glib-2.0])
PKG_CHECK_MODULES([JSONCPP], [jsoncpp])

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_FILES([
 Makefile
 src/Makefile
 src/chip/Makefile
 src/rpi/Makefile
 src/skeleton/Makefile
 src/gtksim/Makefile
])
AC_OUTPUT
