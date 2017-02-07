
#include <unistd.h>
#include <sys/time.h>
#include <stdio.h>

#include "PlatformSerial.h"

void PlatformSerial::log(std::string msg)
{
    struct timeval tv;
    if (gettimeofday(&tv, NULL) < 0) {
        return;
    }

    printf("%ld.%ld %s\n", tv.tv_sec, tv.tv_usec, msg.c_str());
}


PlatformSerial::PlatformSerial(void)
{
}

bool PlatformSerial::init(const std::string& gpio_clk_str,
                          const std::string& gpio_dat_str)
{
    return true;
}


void PlatformSerial::send_bytes(size_t len, unsigned char byte[])
{
}


PlatformSerial::~PlatformSerial()
{
}
