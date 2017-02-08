
#include <unistd.h>
#include <sys/time.h>
#include <stdio.h>

#include "PlatformSerial.h"

PlatformSerial::PlatformSerial()
{
}

void PlatformSerial::send_bytes(size_t len, unsigned char *byte)
{
    size_t i;

    log("send_bytes()");

    for (i = 0; i < len; i++) {
        printf("%d ", byte[i]);
    }
    printf("\n");
}


PlatformSerial::~PlatformSerial()
{
}
