/*
 * chip/PlatformSerialFactory.cpp
 *
 * Creates a PlatformSerial object for the CHiP computer.
 *
 */

#include <PlatformSerialFactory.h>
#include <PlatformSerial.h>

std::shared_ptr<IPlatformSerial> PlatformSerialFactory::create_platform_serial(int iface_num)
{
    std::shared_ptr<PlatformSerial> ser(new PlatformSerial);

    if (ser->init("CSID0", "CSID1") == false) {
        return NULL;
    }
    
    return ser;
}
