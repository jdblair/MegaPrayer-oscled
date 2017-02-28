

#ifndef PLATFORMSERIAL_H
#define PLATFORMSERIAL_H

#include <IPlatformSerial.h>

class PlatformSerial : public IPlatformSerial
{
 public:
    PlatformSerial(void);

    void send(unsigned char *buf, size_t len);

    int iface_num;

    ~PlatformSerial();
};

#endif /* PLATFORMSERIAL_H */
