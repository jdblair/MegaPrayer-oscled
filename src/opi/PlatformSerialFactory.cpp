/*
 * chip/PlatformSerialFactory.cpp
 *
 * Creates a PlatformSerial object for the CHiP computer.
 *
 */

#include <PlatformSerialFactory.h>
#include <PlatformSerial.h>

std::shared_ptr<IPlatformSerial> const PlatformSerialFactory::create_platform_serial(int const iface_num)
{
    std::shared_ptr<PlatformSerial> ser;

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
