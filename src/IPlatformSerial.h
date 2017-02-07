

#ifndef IPLATFORMSERIAL_H
#define IPLATFORMSERIAL_H

#include <string>
#include <stdlib.h>
#include <sys/time.h>
#include <stdio.h>


class IPlatformSerial
{
 public:
    IPlatformSerial() {};
    virtual void send_bytes(size_t len, unsigned char *byte) = 0;

    // general purpose logging function for debugging
    void log(std::string msg) {
        struct timeval tv;
        if (gettimeofday(&tv, NULL) < 0) {
            return;
        }
        
        printf("%ld.%ld %s\n", tv.tv_sec, tv.tv_usec, msg.c_str());
    };

    virtual ~IPlatformSerial() {};
};

#endif /* IPLATFORMSERIAL_H */
