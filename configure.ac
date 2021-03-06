AC_INIT([oscled], [1.0], [jdb@moship.net], [oscled], [https://github.com/jdblair/MegaPrayer-oscled])
AM_INIT_AUTOMAKE([-Wall -Werror foreign])
AC_PROG_CC
AC_PROG_CXX
AC_PROG_RANLIB
AM_PROG_AR

AC_SUBST([AM_CXXFLAGS], [-std=c++11])

git_hash=m4_esyscmd_s([git describe --always])
AC_DEFINE_UNQUOTED([GIT_HASH], "$git_hash", [Git hash prefix])

AC_ARG_ENABLE([serial],
        [AS_HELP_STRING([--enable-serial],
                [specify the platform serial interface])],
        [],
        [enable_serial=skeleton])
AC_DEFINE_UNQUOTED([USE_PLATFORM_SERIAL], "$enable_serial", [platform serial interface])
PLATFORM_SERIAL=$enable_serial
AC_SUBST(PLATFORM_SERIAL)

PLATFORM_SERIAL_LIBS=''
if test "x$enable_serial" = "xgtksim"; then
   PKG_CHECK_MODULES([GTK], [gtk+-2.0])
   PKG_CHECK_MODULES([GOOCANVAS], [goocanvas])
   PKG_CHECK_MODULES([GLIB], [glib-2.0])
   PLATFORM_SERIAL_LIBS="$GOOCANVAS_LIBS"
fi

if test "x$enable_serial" = "xdmx"; then
   PKG_CHECK_MODULES([OLA], [libola])
   PKG_CHECK_MODULES([PROTOBUF], [protobuf])
   PLATFORM_SERIAL_LIBS="$OLA_LIBS"
fi
AC_SUBST(PLATFORM_SERIAL_LIBS)

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


AC_CONFIG_HEADERS([config.h])
AC_CONFIG_FILES([
 Makefile
 src/Makefile
 src/gtksim/Makefile
 src/opi/Makefile
 src/rpi/Makefile
 src/skeleton/Makefile
 src/dmx/Makefile
])
AC_OUTPUT
