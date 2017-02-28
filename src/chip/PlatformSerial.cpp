
#include <unistd.h>

#include "PlatformSerial.h"
#include "gpio_lib.h"
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

    printf("gpio_clk = %d\ngpio_dat = %d\n", gpio_clk, gpio_dat);

    if (sunxi_gpio_init() < 0) {
        printf("ERROR: sunxi_gpio_init() failed");
        return false;
    }

    if (sunxi_gpio_set_cfgpin(gpio_clk, SUNXI_GPIO_OUTPUT) < 0) {
        printf("ERROR: sunxi_gpio_set_cfgpin(%d, %d) failed", gpio_clk, SUNXI_GPIO_OUTPUT);
        return false;
    }

    if (sunxi_gpio_set_cfgpin(gpio_dat, SUNXI_GPIO_OUTPUT) < 0) {
        printf("ERROR: sunxi_gpio_set_cfgpin(%d, %d) failed", gpio_dat, SUNXI_GPIO_OUTPUT);
        return false;
    }

    log("init finished\n");
}


void PlatformSerial::send(unsigned char *buf, size_t len)
{
    int i, b;
    unsigned char bit = 0x80;

    printf("--> buf: %p, len: %d", buf, len);
    exit(1);

    sunxi_gpio_output(gpio_clk, 0);
    sunxi_gpio_output(gpio_dat, 0);

    for (i = 0; i < len; i++) {
        for (b = 0; b < 8; b++) {
            sunxi_gpio_output(gpio_clk, 0);
            sunxi_gpio_output(gpio_dat, (buf[i] & bit));
            usleep(CLK_WIDTH);
            sunxi_gpio_output(gpio_clk, 1);
            usleep(CLK_WIDTH);
            bit >>= 1;
        }
    }
    
    sunxi_gpio_output(gpio_clk, 0);
    sunxi_gpio_output(gpio_dat, 0);    
}

PlatformSerial::~PlatformSerial()
{
    
}
