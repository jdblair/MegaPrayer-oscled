

#ifndef PLATFORMSERIAL_H
#define PLATFORMSERIAL_H

#include <IPlatformSerial.h>

class PlatformSerial : public IPlatformSerial
{
 public:
    PlatformSerial(void);

    void send(unsigned char const *buf, size_t const len);

    int iface_num;

    ~PlatformSerial();
};

#endif /* PLATFORMSERIAL_H */
