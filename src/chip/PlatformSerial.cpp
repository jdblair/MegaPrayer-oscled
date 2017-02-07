
#include <unistd.h>

#include "PlatformSerial.h"
#include "common.h"
#include "event_gpio.h"


PlatformSerial::PlatformSerial(void)
{
    gpio_clk = -1;
    gpio_dat = -1;
}

bool PlatformSerial::init(const std::string& gpio_clk_str,
                          const std::string& gpio_dat_str)
{
    gpio_clk = lookup_gpio_by_name(gpio_clk_str.c_str());
    gpio_dat = lookup_gpio_by_name(gpio_dat_str.c_str());

    if ((gpio_clk < 0) ||
        (gpio_dat < 0)) {
        return false;
    }

    gpio_export(gpio_clk);
    gpio_set_direction(gpio_clk, 1);

    gpio_export(gpio_dat);
    gpio_set_direction(gpio_dat, 1);

    gpio_set_value(gpio_clk, 0);
    gpio_set_value(gpio_dat, 0);
    usleep(5000);  // the first data pulse is always too long withouth this wait
    
}


void PlatformSerial::send_bytes(size_t len, unsigned char byte[])
{
    int i, b;
    unsigned char bit = 0x80;

    gpio_set_value(gpio_clk, 0);
    gpio_set_value(gpio_dat, 0);

    for (i = 0; i < len; i++) {
        for (b = 0; b < 8; b++) {
            gpio_set_value(gpio_clk, 0);
            gpio_set_value(gpio_dat, (byte[i] & bit));
            usleep(CLK_WIDTH);
            gpio_set_value(gpio_clk, 1);
            usleep(CLK_WIDTH);
            bit >>= 1;
        }
    }
    
    gpio_set_value(gpio_clk, 0);
    gpio_set_value(gpio_dat, 0);    
}


PlatformSerial::~PlatformSerial()
{
    event_cleanup();
}
