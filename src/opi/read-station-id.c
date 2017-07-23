#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "common.h"
#include "gpio_lib.h"

/**
 ** to build:
 **   arm-linux-gnueabihf-gcc common.c gpio_lib.h gpio_lib.c test.c -lpthread -o station_id
 **/

static int station_gpios[] = { 2, 13, 14, 10 };
static int station_gpio_count = 4;

int main(int argc, char **argv)
{
    int station_id = 0;
    int units = 1;
    int i;
    
    sunxi_gpio_init();

    /* configure all pins for pull-up */
    for (i = 0; i < station_gpio_count; i++) {
        sunxi_gpio_set_cfgpin(station_gpios[i], 0);
        sunxi_gpio_pullup(station_gpios[i], 1);
    }

    /* now read all the pins and compute the value */
    for (i = 0; i < station_gpio_count; i++) {
        station_id += sunxi_gpio_input(station_gpios[i]) * units;
        units = units *= 2;
    }

    printf("%d\n", station_id);

    return(0);
}
