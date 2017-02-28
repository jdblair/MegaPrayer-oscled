/*
 * rpi/PlatformSerialFactory.cpp
 *
 * Creates a Raspberry Pi PlatformSerial object.
 *
 */

#include <PlatformSerialFactory.h>
#include <PiGPIOSerial.h>
#include <err.h>

std::shared_ptr<IPlatformSerial> PlatformSerialFactory::create_platform_serial(int iface_num)
{
    std::shared_ptr<PiGPIOSerial> ser(new PiGPIOSerial(2, 3));
    ser->iface_num = iface_num;
    if (ser->init() < 0) {
        err(1, "PiGPIOSerial->init() failed");
        return NULL;
    }

    return ser;
}
    

