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
    std::shared_ptr<PlatformSerial> ser(new PlatformSerial(12, 11));

    if (ser->init() == false) {
        return NULL;
    }
    
    return ser;
}
