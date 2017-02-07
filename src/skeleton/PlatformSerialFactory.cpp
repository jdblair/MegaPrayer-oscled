/*
 * skeleton/PlatformSerialFactory.cpp
 *
 * Creates a skeleton PlatformSerial object.
 * The skeleton PlatformSerial stubs out all IPlatformSerial methods.
 *
 */

#include <PlatformSerialFactory.h>
#include <PlatformSerial.h>

std::shared_ptr<IPlatformSerial> PlatformSerialFactory::create_platform_serial(int iface_num)
{
    std::shared_ptr<PlatformSerial> ser(new PlatformSerial);
    ser->iface_num = iface_num;

    return ser;
}
    
