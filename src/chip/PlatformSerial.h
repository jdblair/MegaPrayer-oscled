

#ifndef PLATFORMSERIAL_H
#define PLATFORMSERIAL_H

#define CLK_WIDTH 5

#include <IPlatformSerial.h>

class PlatformSerial : public IPlatformSerial
{
 public:
    PlatformSerial(void);

    bool init(const std::string& gpio_clk,
              const std::string& gpio_dat);

    void send(unsigned char *buf, size_t len);
    
    int gpio_clk;
    int gpio_dat;

    ~PlatformSerial();
};

#endif /* PLATFORMSERIAL_H */
