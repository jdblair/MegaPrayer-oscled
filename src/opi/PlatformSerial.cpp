
#include <unistd.h>

#include "PlatformSerial.h"
#include "gpio_lib.h"
#include "common.h"
#include "event_gpio.h"


PlatformSerial::PlatformSerial(int const clk_pin, int const dat_pin) :
    gpio_clk(clk_pin), gpio_dat(dat_pin)
{
}


bool PlatformSerial::init(void)
{
    if (sunxi_gpio_init() < 0) {
        printf("ERROR: sunxi_gpio_init() failed");
        return false;
    }

    gpio_export(gpio_clk);
    gpio_export(gpio_dat);
    gpio_set_direction(gpio_clk, 1);
    gpio_set_direction(gpio_dat, 1);
    
    log("init finished\n");

    return true;
}


void PlatformSerial::send(unsigned char const *buf, size_t const len)
{
    size_t i;
    int b;
    unsigned char bit;
    
    sunxi_gpio_output(gpio_clk, 0);
    sunxi_gpio_output(gpio_dat, 0);

    for (i = 0; i < len; i++) {
        bit = 0x80;
        for (b = 0; b < 8; b++) {
            //printf("%d & %d = %d\n", buf[i], bit, buf[i] & bit);
            sunxi_gpio_output(gpio_clk, 0);
            sunxi_gpio_output(gpio_dat, (buf[i] & bit));
            for (int delay = CLK_WIDTH; delay; delay--);
            sunxi_gpio_output(gpio_clk, 1);
            for (int delay = CLK_WIDTH; delay; delay--);
            bit >>= 1;
        }
    }
    
    sunxi_gpio_output(gpio_clk, 0);
    sunxi_gpio_output(gpio_dat, 0);

    usleep(500);
}

PlatformSerial::~PlatformSerial()
{
    
}
