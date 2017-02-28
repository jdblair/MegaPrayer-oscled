
#include <stdio.h>
#include <stdlib.h>
#include <IPlatformSerial.h>
#include <PlatformSerialFactory.h>

#include <memory>

#include "config.h"


int main(int argc, char **argv)
{
    PlatformSerialFactory ser_factory;
    std::shared_ptr<IPlatformSerial> ser = ser_factory.create_platform_serial(0);

    unsigned char led_array[256];

    int i;
    for (i = 1; i < argc; i++) {
        led_array[i - 1] = atoi(argv[i]);
    }

    printf("argc: %d, led_array = %p\n", argc, led_array);
    ser->send(led_array, argc - 1);
}

