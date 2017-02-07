

#ifndef PLATFORMSERIAL_H
#define PLATFORMSERIAL_H

#include <IPlatformSerial.h>

class PlatformSerial : public IPlatformSerial
{
 public:
    PlatformSerial(void);

    bool init(const std::string& gpio_clk,
             const std::string& gpio_dat);

    void send_bytes(size_t len, unsigned char byte[]);
    void log(std::string msg);

    ~PlatformSerial();
};

#endif /* PLATFORMSERIAL_H */
