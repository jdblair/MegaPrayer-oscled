
#include "PlatformSerial.h"
#include "common.h"

PlatformSerial::PlatformSerial(void)
{
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

}

void send_byte(unsigned char byte)
{

}
