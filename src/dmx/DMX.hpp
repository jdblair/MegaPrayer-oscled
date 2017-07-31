#ifndef DMX_H
#define DMX_H

#include <vector>
#include <string>
#include <memory>
#include <mutex>
#include <atomic>
#include <ola/DmxBuffer.h>
#include <ola/client/StreamingClient.h>

#include "IPlatformSerial.h"
#include "OSCServer.h"

//#include "DMXSerial.hpp"

// Singleton class that owns the serial communication with the DMX512 system.
// There is only one of these even though there are an arbitrary number of DMX interfaces.

class DMX
{
public:

    typedef struct spotlight_state {
	spotlight_state() { r = 0; g = 0; b = 0; }
	spotlight_state(uint8_t r_arg, uint8_t g_arg, uint8_t b_arg) :
	    r(r_arg), g(g_arg), b(b_arg) {};
	void set(uint8_t r_arg, uint8_t g_arg, uint8_t b_arg) {
	    r = r_arg; g = g_arg; b = b_arg; };
	uint8_t r;
	uint8_t g;
	uint8_t b;
    } spotlight_state_t;

    static DMX& getInstance() {
        static DMX instance;
        return instance;
    }

    void init();
    void send(unsigned char const *buf, size_t const len);

    static const size_t BEAD_COUNT=1;

    static const int RED = 1;
    static const int GREEN = 2;
    static const int BLUE = 3;
    static const int WHITE = 4;
    static const int STROBE = 5;

    static const int CHANNELS_PER_LIGHT = 8;

    spotlight_state_t m_led;
    void send_dmx(ola::DmxBuffer& buffer);


private:
    DMX();

    unsigned char *m_last_buf;
    size_t m_last_buf_len;

    ola::client::StreamingClient ola_client;
    unsigned int universe = 0;
    ola::DmxBuffer blackout_buffer;

public:
    DMX(DMX const&)             = delete;
    void operator=(DMX const&)  = delete;

};

// DMXSerial implements the IPlatformSerial interface, simulating a physical
// serial interface. The bytes received in send() are assumed to be a single
// LED string update, applying to all spotlights in the DMX "universe"

class DMXSerial : public IPlatformSerial
{
private:
    DMX &m_dmx;
    int m_light_id;

public:
    DMXSerial(DMX &dmx, int light_id, int base, int len) :
        m_dmx(dmx), m_led_low(base), m_len(len), m_light_id(light_id)
    {
        m_led_high = m_led_low + m_len;
        m_last_buf = NULL;
        m_last_buf_len = 0;
    };

    void send(unsigned char const *buf, const size_t len);
    ~DMXSerial() {
	std::cerr << "Freeing PTR: " << (void*)m_last_buf << std::endl;
        free(m_last_buf);
    };

private:
    int m_len;
    int m_led_low;
    int m_led_high;

    unsigned char *m_last_buf;
    size_t m_last_buf_len;
};

#endif /* DMX_H */
