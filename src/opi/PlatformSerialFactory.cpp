/*
 * chip/PlatformSerialFactory.cpp
 *
 * Creates a PlatformSerial object for the CHiP computer.
 *
 */

#include <PlatformSerialFactory.h>
#include <PlatformSerial.h>

#include <err.h>

std::shared_ptr<IPlatformSerial> const PlatformSerialFactory::create_platform_serial(int const iface_num)
{
    std::shared_ptr<PlatformSerial> ser;

    switch (iface_num) {
    case 0:
        ser.reset(new PlatformSerial(3, 5));
        break;
    case 1:
        ser.reset(new PlatformSerial(7, 12));
        break;
    case 2:
        ser.reset(new PlatformSerial(11, 13));
        break;
    case 3:
        ser.reset(new PlatformSerial(16, 18));
        break;
    case 4:
        ser.reset(new PlatformSerial(8, 10));
        break;
    }

    if (ser->init() < 0) {
        err(1, "PlatformSerial->init() failed");
        return NULL;
    }

    return ser;
}
