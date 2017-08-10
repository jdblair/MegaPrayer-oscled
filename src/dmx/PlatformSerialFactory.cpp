/*
 * skeleton/PlatformSerialFactory.cpp
 *
 * Creates a skeleton PlatformSerial object.
 * The skeleton PlatformSerial stubs out all IPlatformSerial methods.
 *
 */

#include "PlatformSerialFactory.h"
#include "DMX.hpp"

#include <iostream>

// DMX version of PlatformSerialFactory
const std::shared_ptr<IPlatformSerial> PlatformSerialFactory::create_platform_serial(int const iface_num)
{
    std::shared_ptr<DMXSerial> ser;

    DMX &dmx = DMX::getInstance();
    dmx.init();

    // Each MegaPrayer interface is mapped to a DMX universe
    switch (iface_num) {
    case 0:
        ser.reset(new DMXSerial(dmx, 0));
        break;

    default:
	std::cerr << "ERROR: Invalid DMX interface number (" << iface_num << ")" << std::endl;
	exit(1);
    }

    return ser;
}

