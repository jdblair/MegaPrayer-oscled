

#ifndef IPLATFORMSERIAL_H
#define IPLATFORMSERIAL_H

class IPlatformSerial
{
 public:
    virtual void send_byte(char byte) = 0;

    virtual ~IPlaformSerial() {};
};

#endif /* IPLATFORMSERIAL_H */
