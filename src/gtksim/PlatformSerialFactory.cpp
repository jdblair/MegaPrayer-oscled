/*
 * skeleton/PlatformSerialFactory.cpp
 *
 * Creates a skeleton PlatformSerial object.
 * The skeleton PlatformSerial stubs out all IPlatformSerial methods.
 *
 */

#include <PlatformSerialFactory.h>
#include <GtkSim.hpp>

#include <iostream>

using namespace std;

std::shared_ptr<IPlatformSerial> PlatformSerialFactory::create_platform_serial(int iface_num)
{
    std::shared_ptr<GtkSimSerial> ser;
    GtkSim &sim = GtkSim::getInstance();

    switch (iface_num) {
    case 0:
        ser.reset(new GtkSimSerial(0, 29, true));
        break;
    case 1:
        ser.reset(new GtkSimSerial(30, 59, false));
        break;
    }

    return ser;
}
    
