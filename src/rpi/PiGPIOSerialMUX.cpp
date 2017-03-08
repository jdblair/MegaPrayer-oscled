
#include <unistd.h>
#include <sys/time.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <err.h>

#include <thread>

#include "PiGPIOSerialMUX.h"


// From GPIO example code by Dom and Gert van Loo on elinux.org:
#define PI1_BCM2708_PERI_BASE 0x20000000
#define PI1_GPIO_BASE         (PI1_BCM2708_PERI_BASE + 0x200000)
#define PI2_BCM2708_PERI_BASE 0x3F000000
#define PI2_GPIO_BASE         (PI2_BCM2708_PERI_BASE + 0x200000)
#define BLOCK_SIZE            (4*1024)
#define INP_GPIO(g)          *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g)          *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))

#define CLK_WIDTH             400

using namespace std;

// initialize the GPIO interface
int PiGPIOSerialMUXMain::init()
{
    int fd;

    if (initialized)
        return 0;

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

    initialized = true;

    return 0;
}

void PiGPIOSerialMUXMain::set_iface(int clk_pin, int dat_pin, std::shared_ptr<CircularBuffer> buf)
{
    iface_t iface;

    iface.dat_pin = dat_pin;
    iface.clk_pin = clk_pin;
    iface.buf = buf;
    iface.dat_mask = 1 << dat_pin;
    iface.clk_mask = 1 << clk_pin;

    ifaces.push_back(iface);
}

// returns non-zero when a byte is sent, zero if there is no data waiting
uint32_t PiGPIOSerialMUXMain::send_next_byte()
{
    int delay;
    uint32_t all_clr_mask = 0;
    uint32_t all_clk_mask = 0;
    bool byte_sent = false;
    
    // set-up
    for (auto it = ifaces.begin(); it != ifaces.end(); ++it) {
        // make mask of all gpios
        all_clr_mask |= it->clk_mask;
        all_clr_mask |= it->dat_mask;

        // read the next byte
        if (it->buf->read(&(it->next_byte), 1)) {
            all_clk_mask |= it->clk_mask;  // only set clk mask for ifaces with data
        } else {
            it->next_byte = 0;
        }
    }
    *gpio_clr = all_clr_mask;  // clear all gpios

    // is there any data to transmit?
    if (all_clk_mask == 0)
        return 0;

    // transmit byte
    uint8_t bit_mask = 0x80;
    int b;
    for (b = 0; b < 8; b++) {
        uint32_t all_dat_set_mask = 0;
        uint32_t all_dat_clr_mask = 0;

        *gpio_clr = all_clk_mask;  // clk = 0

        // set dat for all ifaces
        for (auto it = ifaces.begin(); it != ifaces.end(); ++it) {
            if (it->next_byte & bit_mask) {
                *gpio_set |= it->dat_mask;  // dat = 1
            } else {
                *gpio_clr |= it->dat_mask;  // dat = 0
            }
        }

        for (delay = CLK_WIDTH; delay--; delay);  // delay
        
        *gpio_set = all_clk_mask;  // clk = 1
        
        for (delay = CLK_WIDTH; delay--; delay);  // delay
        
        bit_mask >>= 1;
    }

    *gpio_clr = all_clk_mask;

    return all_clk_mask;
}






PiGPIOSerialMUX::PiGPIOSerialMUX(int clk_pin, int dat_pin) : m_clk_pin(clk_pin), m_dat_pin(dat_pin)
{
    m_buf.reset(new CircularBuffer(1024));
    PiGPIOSerialMUXMain &mux = PiGPIOSerialMUXMain::getInstance();
    mux.set_iface(clk_pin, dat_pin, m_buf);
}


void PiGPIOSerialMUX::send(unsigned char *buf, size_t len)
{
    auto to_write = len;

    // buf should fit into m_buf in one write()
    // but keep trying if it doesn't
    while (to_write > 0) {
        to_write -= m_buf->write(buf, len);
    }
}


PiGPIOSerialMUX::~PiGPIOSerialMUX()
{
}

