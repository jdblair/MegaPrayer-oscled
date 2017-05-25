/*
 * rpi/PlatformSerialFactory.cpp
 *
 * Creates a Raspberry Pi PlatformSerial object.
 *
 */

#include <PlatformSerialFactory.h>
#include <PiGPIOSerial.h>
#include <err.h>

std::shared_ptr<IPlatformSerial> const PlatformSerialFactory::create_platform_serial(int const iface_num)
{
    std::shared_ptr<PiGPIOSerial> ser;

    switch (iface_num) {
    case 0:
        ser.reset(new PiGPIOSerial(2, 3));
        break;
    case 1:
        ser.reset(new PiGPIOSerial(5, 6));
        break;
    }

    if (ser->init() < 0) {
        err(1, "PiGPIOSerial->init() failed");
        return NULL;
    }

    return ser;
}
    

