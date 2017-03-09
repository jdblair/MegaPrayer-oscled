
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "IPlatformSerial.h"
#include "PlatformSerialFactory.h"
#include "OSCServer.h"

#include <memory>

#include "config.h"


int main(int argc, char **argv)
{
    PlatformSerialFactory ser_factory;
    std::shared_ptr<IPlatformSerial> ser0 = ser_factory.create_platform_serial(0);
    std::shared_ptr<IPlatformSerial> ser1 = ser_factory.create_platform_serial(1);

    OSCServer server(5005);
    server.set_base_bead(0);
    server.set_leds_per_bead(8);
    server.bind(ser0, 0, 240, true);
    server.bind(ser1, 240, 240, false);

    server.start();

    while (1) {
        sleep(1);
    }
}

