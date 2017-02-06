
#include <stdio.h>
#include <stdlib.h>
#include <IPlatformSerial.h>
#include <chip/PlatformSerial.h>

#include <memory>


int main(int argc, char **argv)
{
    PlatformSerial ser = PlatformSerial();
    ser.init("CSID0", "CSID1");


    int i;
    for (i = 1; i < argc; i++) {
        //printf("send %s\n", argv[i]);
        ser.send_byte(atoi(argv[i]));
    }
}

