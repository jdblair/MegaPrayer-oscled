

#ifndef IPLATFORMSERIAL_H
#define IPLATFORMSERIAL_H

#include <string>
#include <stdlib.h>
#include <sys/time.h>
#include <stdio.h>

#include <iostream>

#ifdef DEBUG
#define log(msg) _log(msg)
#else
#define log(msg)
#endif

class IPlatformSerial
{
 public:
    IPlatformSerial() {};
    virtual void send(unsigned char *buf, size_t len) {
        std::cout << "IPlatformSerial not over-ridden" << std::endl;
    }

    // general purpose logging function for debugging
    void _log(std::string msg) {
        struct timeval tv;
        if (gettimeofday(&tv, NULL) < 0) {
            return;
        }
        
        printf("%ld.%ld %s\n", tv.tv_sec, tv.tv_usec, msg.c_str());
    };

    virtual ~IPlatformSerial() {};
};

#endif /* IPLATFORMSERIAL_H */
