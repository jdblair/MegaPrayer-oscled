
#ifndef GTKSIM_H
#define GTKSIM_H

#include <vector>
#include <string>
#include <memory>
#include <mutex>
#include <atomic>

#include <goocanvas.h>

#include "IPlatformSerial.h"

gboolean gtksim_update_beads(gpointer user_data);

typedef struct led {
    led(uint8_t r_arg, uint8_t g_arg, uint8_t b_arg) :
        r(r_arg), g(g_arg), b(b_arg) {};
    void set(uint8_t r_arg, uint8_t g_arg, uint8_t b_arg) {
        r = r_arg; g = g_arg; b = b_arg; };
    uint8_t r;
    uint8_t g;
    uint8_t b;
} led_t;


// GtkSim is a singleton class that owns the on-screen GTK simulation.
// There is only one of these even though there are an arbitrary number
// of GtkSimSerial interfaces.
class GtkSim
{
public:
    static GtkSim& getInstance() {
        static GtkSim instance;
        return instance;
    }

    void main();
    void start();

    static const size_t BEAD_COUNT=60;

    std::vector<led_t> m_leds;

    GooCanvasItem *g_beads[BEAD_COUNT];
    GValue m_bead_values[BEAD_COUNT];
    int m_leds_per_bead;
    void set_leds_per_bead(int leds_per_bead);
    
    void update_beads();

    std::atomic<bool> m_gtk_ready;

private:
    GtkSim();

 public:    
    GtkSim(GtkSim const&)          = delete;
    void operator=(GtkSim const&)  = delete;

};

// GtkSimSerial implements the IPlatformSerial interface, simulating a physical
// serial interface. The bytes received in send() are assumed to be a single
// LED string update and are converted back to an array of bead colors based on 
// GtkSim::m_leds_per_bead.
class GtkSimSerial : public IPlatformSerial
{
private:
    std::shared_ptr<GtkSim> m_sim;

public:
    GtkSimSerial(int base, int len, bool reversed) :
        m_led_low(base), m_len(len), m_led_reversed(reversed)
    {
        m_led_high = m_led_low + m_len;
        m_sim.reset(&GtkSim::getInstance());
        m_last_buf = NULL;
        m_last_buf_len = 0;
    };

    void send(unsigned char *buf, size_t len);
    ~GtkSimSerial() {
        free(m_last_buf);
    };

private:
    int m_len;
    int m_led_low;
    int m_led_high;
    bool m_led_reversed;

    unsigned char *m_last_buf;
    size_t m_last_buf_len;
};


#endif /* GTKSIM_H */
