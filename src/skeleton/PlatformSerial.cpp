
#include <unistd.h>
#include <sys/time.h>
#include <stdio.h>

#include "PlatformSerial.h"

PlatformSerial::PlatformSerial()
{
}


void PlatformSerial::send(unsigned char *buf, size_t len)
{
    size_t i;

    log("send_bytes()");

    for (i = 0; i < len; i++) {
        printf("%d ", buf[i]);
    }
    printf("\n");
}


PlatformSerial::~PlatformSerial()
{
}
