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
        ser.reset(new PlatformSerial(12, 11));
        break;
    case 1:
        ser.reset(new PlatformSerial(6, 7));
        break;
    case 2:
        ser.reset(new PlatformSerial(1, 0));
        break;
    case 3:
        ser.reset(new PlatformSerial(19, 18));
        break;
    case 4:
        ser.reset(new PlatformSerial(198, 199));
        break;
    }

    if (ser->init() < 0) {
        err(1, "PlatformSerial->init() failed");
        return NULL;
    }

    return ser;
}
