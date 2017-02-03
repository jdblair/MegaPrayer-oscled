

#ifndef PLATFORMSERIAL_H
#define PLATFORMSERIAL_H

class PlatformSerial : public IPlatformSerial
{
 public:
    PlatformSerial(void);

    bool init(const std::string& gpio_clk,
             const std::string& gpio_dat);

    void send_byte(unsigned char byte);

    int gpio_clk = -1;
    int gpio_dat = -1;

    ~PlatformSerial();
};

#endif /* PLATFORMSERIAL_H */
