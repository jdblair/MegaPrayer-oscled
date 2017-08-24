

#ifndef PLATFORMSERIAL_H
#define PLATFORMSERIAL_H

#define CLK_WIDTH 500

#include <IPlatformSerial.h>

class PlatformSerial : public IPlatformSerial
{
 public:
    PlatformSerial(int const clk_pin, int const dat_pin);

    bool init(void);

    void send(unsigned char const *buf, size_t const len);
    
    int gpio_clk;
    int gpio_dat;

    ~PlatformSerial();
};

#endif /* PLATFORMSERIAL_H */
