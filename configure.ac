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

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_FILES([
 Makefile
 src/Makefile
 src/chip/Makefile
 src/skeleton/Makefile
])
AC_OUTPUT
