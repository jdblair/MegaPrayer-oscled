

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

    void send_bytes(size_t len, unsigned char byte[]);
    void log(std::string msg);

    int gpio_clk;
    int gpio_dat;

    ~PlatformSerial();
};

#endif /* PLATFORMSERIAL_H */
