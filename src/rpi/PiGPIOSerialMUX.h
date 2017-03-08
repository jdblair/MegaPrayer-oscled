

#ifndef PIGPIOSERIALMUX_H
#define PIGPIOSERIALMUX_H

#include <IPlatformSerial.h>
#include <stdint.h>

#include <vector>

#include "CircularBuffer.h"

// singleton class
// initializes the gpio interface and owns the thread that sets the gpio data
class PiGPIOSerialMUXMain
{
 public:
    static PiGPIOSerialMUXMain& getInstance()
    {
        static PiGPIOSerialMUXMain  instance; // Guaranteed to be destroyed.
        // Instantiated on first use.
        return instance;
    };

    int init();

    void set_iface(int clk_pin, int dat_pin, std::shared_ptr<CircularBuffer> buf);

 private:
    PiGPIOSerialMUXMain() : initialized(false) {};
    
    // memory addresses used to manipulate the GPIO states
    volatile uint32_t *gpio;
    volatile uint32_t *gpio_set;
    volatile uint32_t *gpio_clr;
    
    bool initialized;
    
    typedef struct iface {
        // these values identify the interface
        int dat_pin;
        int clk_pin;
        std::shared_ptr<CircularBuffer> buf;
        
        // these values used by the transmit loop
        uint32_t dat_mask;
        uint32_t clk_mask;
        //bool ready;
        uint8_t next_byte;
    } iface_t;
    
    // list of all GPIO serial interfaces
    std::vector<iface_t> ifaces;
    
    uint32_t send_next_byte();
    
 public:    
    PiGPIOSerialMUXMain(PiGPIOSerialMUXMain const&)               = delete;
    void operator=(PiGPIOSerialMUXMain const&)  = delete;
    
    // Note: Scott Meyers mentions in his Effective Modern
    //       C++ book, that deleted functions should generally
    //       be public as it results in better error messages
    //       due to the compilers behavior to check accessibility
    //       before deleted status
};


class PiGPIOSerialMUX : public IPlatformSerial
{
 public:
    PiGPIOSerialMUX(int clk_pin, int dat_pin);
    
    void send(unsigned char *buf, size_t len);

    int iface_num;

    ~PiGPIOSerialMUX();

 private:

    std::shared_ptr<CircularBuffer> m_buf;

    uint8_t m_dat_pin;
    uint8_t m_clk_pin;
    
};

#endif /* PIGPIOSERIALMUX_H */
