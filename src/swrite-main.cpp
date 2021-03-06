
#include <stdio.h>
#include <stdlib.h>
#include <IPlatformSerial.h>
#include <PlatformSerialFactory.h>

#include <memory>

#include "config.h"


int main(int argc, char **argv)
{
    PlatformSerialFactory ser_factory;

    printf("using serial interface: %s\n", argv[1]);

    std::shared_ptr<IPlatformSerial> ser = ser_factory.create_platform_serial(atoi(argv[1]));

    unsigned char led_array[256];

    int i;
    for (i = 2; i < argc; i++) {
        led_array[i - 2] = atoi(argv[i]);
    }

    printf("argc: %d, led_array = %p\n", argc, led_array);
    ser->send(led_array, argc - 2);
}

