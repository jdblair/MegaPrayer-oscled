

#ifndef PLATFORMSERIAL_H
#define PLATFORMSERIAL_H

#include <IPlatformSerial.h>

class PlatformSerial : public IPlatformSerial
{
 public:
    PlatformSerial(void);

    void send_bytes(size_t len, unsigned char byte[]);

    int iface_num;

    ~PlatformSerial();
};

#endif /* PLATFORMSERIAL_H */
