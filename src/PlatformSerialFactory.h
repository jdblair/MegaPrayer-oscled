
#include <memory>
#include "IPlatformSerial.h"

class PlatformSerialFactory
{
 public:
    PlatformSerialFactory() {};
    std::shared_ptr<IPlatformSerial> const create_platform_serial(int const iface_num);
};
