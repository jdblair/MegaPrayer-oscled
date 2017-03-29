
#include <stdio.h>
#include <stdlib.h>

#include "common.h"
#include "event_gpio.h"

void main(int argc, char **argv)
{
    sunxi_gpio_init();
    
    /* int gpio = lookup_gpio_by_name(argv[1]); */
    
    /* if (gpio < 0) { */
    /*     printf("undefined gpio: %s\n", argv[1]); */
    /*     exit(1); */
    /* } */

    int gpio;
    gpio = atoi(argv[1]);
    
    printf("gpio: %d\n", gpio);
        
    gpio_export(gpio);
    gpio_set_direction(gpio, 1);
    gpio_set_value(gpio, atoi(argv[2]));
    event_cleanup();
}
