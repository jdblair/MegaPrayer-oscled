
#include <memory>
#include "IPlatformSerial.h"

class PlatformSerialFactory
{
 public:
    std::shared_ptr<IPlatformSerial> create_platform_serial(int iface_num);
};
