
#include <stdio.h>
#include <stdlib.h>

#include "common.h"
#include "event_gpio.h"

void main(int argc, char **argv)
{
    int gpio = lookup_gpio_by_name(argv[1]);

    gpio_export(gpio);
    gpio_set_direction(gpio, 1);
    gpio_set_value(gpio, atoi(argv[2]));
    event_cleanup();
}
