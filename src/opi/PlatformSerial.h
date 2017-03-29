

#ifndef PLATFORMSERIAL_H
#define PLATFORMSERIAL_H

#define CLK_WIDTH 120

#include <IPlatformSerial.h>

class PlatformSerial : public IPlatformSerial
{
 public:
    PlatformSerial(int clk_pin, int dat_pin);

    bool init(void);

    void send(unsigned char *buf, size_t len);
    
    int gpio_clk;
    int gpio_dat;

    ~PlatformSerial();
};

#endif /* PLATFORMSERIAL_H */
