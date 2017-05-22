#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "common.h"
#include "gpio_lib.h"

/**
 ** to build:
 **   arm-linux-gnueabihf-gcc common.c gpio_lib.h gpio_lib.c test.c -lpthread -o test-gpio
 **
 ** usage:
 **   output: ./test 12 out <value>
 **              0    1  2    3
 **   input:  ./test 12 in [up|down]
 **
 ** there is no error checking! ymmv!
 **/

void main(int argc, char **argv)
{
    
    sunxi_gpio_init();
    
    int gpio;
    gpio = atoi(argv[1]);
    
    if (strcasecmp("out", argv[2]) == 0) {
        /* output */
        printf("gpio OUTPUT: %d\n", gpio);
        
        // set as an output
        sunxi_gpio_set_cfgpin(gpio, 1);
        // turn output to arg
        sunxi_gpio_output(gpio, atoi(argv[3]));
    } else {
        /* input*/
        printf("gpio %d INPUT ", gpio);
        
        // set as an input
        sunxi_gpio_set_cfgpin(gpio, 0);
        
        if (strcasecmp("up", argv[3]) == 0) {
            printf("pull-up: ");
            sunxi_gpio_pullup(gpio, 1);
        } else {
            printf("pull-down: ");
            sunxi_gpio_pullup(gpio, 0);
        }
        
        printf("%d\n", sunxi_gpio_input(gpio));
        
    }
    sleep(1);
    
}
