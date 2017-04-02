/*
 * skeleton/PlatformSerialFactory.cpp
 *
 * Creates a skeleton PlatformSerial object.
 * The skeleton PlatformSerial stubs out all IPlatformSerial methods.
 *
 */

#include "PlatformSerialFactory.h"
#include "GtkSim.hpp"

#include <iostream>

using namespace std;

// GTKSim version of PlatformSerialFactory
std::shared_ptr<IPlatformSerial> PlatformSerialFactory::create_platform_serial(int iface_num)
{
    std::shared_ptr<GtkSimSerial> ser;

    GtkSim &sim = GtkSim::getInstance();

    sim.set_leds_per_bead(8);

    switch (iface_num) {
    case 0:
        ser.reset(new GtkSimSerial(0, 239, true));
        break;
    case 1:
        ser.reset(new GtkSimSerial(240, 240, false));
        break;
    }

    return ser;
}
    
