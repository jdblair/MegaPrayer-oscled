
#include <stdio.h>
#include <stdlib.h>

#include <fcntl.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
#include <stdint.h>

// From GPIO example code by Dom and Gert van Loo on elinux.org:
#define PI1_BCM2708_PERI_BASE 0x20000000
#define PI1_GPIO_BASE         (PI1_BCM2708_PERI_BASE + 0x200000)
#define PI2_BCM2708_PERI_BASE 0x3F000000
#define PI2_GPIO_BASE         (PI2_BCM2708_PERI_BASE + 0x200000)
#define BLOCK_SIZE            (4*1024)
#define INP_GPIO(g)          *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g)          *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))

static volatile unsigned
  *gpio = NULL, // Memory-mapped GPIO peripheral
  *gpioSet,     // Write bitmask of GPIO pins to set here
  *gpioClr;     // Write bitmask of GPIO pins to clear here

static uint8_t isPi2 = 0; // For clock pulse timing & stuff

int main (int argv, char *argc[])
{
    int fd;

    uint32_t dataMask;
    uint32_t clockMask;
    uint8_t dataPin;
    uint8_t clockPin;
    uint8_t value;

    dataPin = atoi(argc[1]);
    value = atoi(argc[2]);

    if((fd = open("/dev/mem", O_RDWR | O_SYNC)) < 0) {
        printf("Can't open /dev/mem (try 'sudo')\n");
        return -1;
    }
    isPi2 = 1;
    gpio  = (volatile unsigned *)mmap( // Memory-map I/O
                                      NULL,                 // Any adddress will do
                                      BLOCK_SIZE,           // Mapped block length
                                      PROT_READ|PROT_WRITE, // Enable read+write
                                      MAP_SHARED,           // Shared w/other processes
                                      fd,                   // File to map
                                      isPi2 ?
                                      PI2_GPIO_BASE :      // -> GPIO registers
                                      PI1_GPIO_BASE);
    close(fd);              // Not needed after mmap()

    if(gpio == MAP_FAILED) {
        err("Can't mmap()");
        return -1;
    }

    gpioSet = &gpio[7];
    gpioClr = &gpio[10];

    dataMask  = 1 << dataPin;
    //clockMask = 1 << clockPin;

    INP_GPIO(dataPin);  OUT_GPIO(dataPin);
    //INP_GPIO(clockPin); OUT_GPIO(clockPin);

    //*gpioClr = dataMask | clockMask; // data+clock LOW
    
    if (value == 0) {
        printf("clear pin\n");
        *gpioClr = dataMask;
    } else {
        printf("set pin\n");
        *gpioSet = dataMask;
    }
}
 
