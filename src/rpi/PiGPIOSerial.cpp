
#include <unistd.h>
#include <sys/time.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <err.h>

#include "PiGPIOSerial.h"


// From GPIO example code by Dom and Gert van Loo on elinux.org:
#define PI1_BCM2708_PERI_BASE 0x20000000
#define PI1_GPIO_BASE         (PI1_BCM2708_PERI_BASE + 0x200000)
#define PI2_BCM2708_PERI_BASE 0x3F000000
#define PI2_GPIO_BASE         (PI2_BCM2708_PERI_BASE + 0x200000)
#define BLOCK_SIZE            (4*1024)
#define INP_GPIO(g)          *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g)          *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))

#define CLK_WIDTH             400

PiGPIOSerial::PiGPIOSerial(int clk_pin, int dat_pin) : m_clk_pin(clk_pin), m_dat_pin(dat_pin)
{
}


int PiGPIOSerial::init()
{
    int fd;

    if((fd = open("/dev/mem", O_RDWR | O_SYNC)) < 0) {
        err(1, "Can't open /dev/mem (try 'sudo')\n");
        return -1;
    }
    gpio  = (volatile unsigned *)mmap( // Memory-map I/O
                                      NULL,                 // Any adddress will do
                                      BLOCK_SIZE,           // Mapped block length
                                      PROT_READ|PROT_WRITE, // Enable read+write
                                      MAP_SHARED,           // Shared w/other processes
                                      fd,                   // File to map
                                      PI2_GPIO_BASE);
    close(fd);              // Not needed after mmap()

    if(gpio == MAP_FAILED) {
    err(1, "Can't mmap()");
        return -1;
    }

    gpio_set = &gpio[7];
    gpio_clr = &gpio[10];

    dat_mask  = 1 << m_dat_pin;
    clk_mask = 1 << m_clk_pin;

    INP_GPIO(m_dat_pin); OUT_GPIO(m_dat_pin);
    INP_GPIO(m_clk_pin); OUT_GPIO(m_clk_pin);

    *gpio_clr = dat_mask | clk_mask; // data + clock LOW
}


void PiGPIOSerial::send(unsigned char *buf, size_t len)
{
    size_t i;
    int b;
    int delay;
    unsigned char bit_mask;
    
    *gpio_clr = clk_mask | dat_mask;

    for (i = 0; i < len; i++) {
        bit_mask = 0x80;
        for (b = 0; b < 8; b++) {
            *gpio_clr = clk_mask;  /* clk = 0 */
            if (buf[i] & bit_mask) {
                *gpio_set = dat_mask;  /* dat = 1 */
            } else {
                *gpio_clr = dat_mask;  /* dat = 0 */
            }
            for (delay = CLK_WIDTH; delay--; delay);
            *gpio_set = clk_mask; /* clk = 1 */
            for (delay = CLK_WIDTH; delay--; delay);
            bit_mask >>= 1;
        }
    }
    *gpio_clr = clk_mask;
}


PiGPIOSerial::~PiGPIOSerial()
{
}

