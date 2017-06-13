
#include <lo/lo.h>
#include <lo/lo_cpp.h>
#include <err.h>
#include <unistd.h>
#include <arpa/inet.h>

#include <vector>
#include <atomic>
#include <iostream>
#include <string>

#include "IPlatformSerial.h"
#include "OSCServer.h"
#include "OSCLedConfig.hpp"

using namespace std;




OSCServer::OSCServer(atomic<bool> *running, string ip, string port) : m_running(running), m_ip(ip), m_port(port)
{
    received = 0;
    m_iface_count = 0;
    
    lo_server_thread osc_st;
    struct sockaddr_in sa;
    
    // is ip a multicast address?
    inet_pton(AF_INET, ip.c_str(), &(sa.sin_addr));  // convert to 4-byte ipv4 address
    uint32_t addr = ntohl(sa.sin_addr.s_addr);       // cast as uint32_t in host byte order
    if ((addr & 0xe0000000) == 0xe0000000) {         // check high order byte == 0xe0
        cout << "starting multicast server at " << ip << ":" << port << endl;
        osc_st = lo_server_thread_new_multicast(ip.c_str(), port.c_str(), NULL);
    } else {
        // liblo doesn't actually let us bind to a specific address, so
        // specific non-multicast addresses are not supported
        cout << "starting unicast server on port " << port << endl;
        osc_st = lo_server_thread_new(port.c_str(), NULL);
    }

    if (! osc_st) {
        err(1, "can't create liblo server thread");
        return;
    }

    // make a ServerThread object from the lo_server_thread we made above
    m_st.reset(new lo::ServerThread(osc_st));

    m_st->add_method("/led", "iiii", 
                     [this](lo_arg **argv, int)  {this->osc_method_led(argv);});
    m_st->add_method("/ledf", "ifff", 
                     [this](lo_arg **argv, int)  {this->osc_method_led_float(argv);});
    m_st->add_method("/bead", "iiii", 
                     [this](lo_arg **argv, int)  {this->osc_method_bead(argv);});
    m_st->add_method("/beadf", "ifff", 
                     [this](lo_arg **argv, int)  {this->osc_method_bead_float(argv);});
    m_st->add_method("/update", "",
                     [this](lo_arg **argv, int)  {this->osc_method_update(argv);});

    m_base_bead = 0;
    m_leds_per_bead = 1;
}




void OSCServer::set_led(int n, led_t led)
{
    // search for correct led_interface, set leds
    for (auto it = m_led_ifaces.begin(); it != m_led_ifaces.end(); ++it) {
        auto iface = *it;
        if ((n >= iface->m_base) & (n < (iface->m_base + iface->m_len))) {
            n -= iface->m_base;  // normalize to vector offset
            if (iface->m_reverse) {
                n = iface->m_len - 1 - n;  // reverse
            }
            iface->set_led(n, led);
        }
    }
}


int OSCServer::osc_method_led(lo_arg **argv)
{
    // cout << "/led (" << ++received << "): "
    //      << argv[0]->i << ", " 
    //      << argv[1]->i << ", " 
    //      << argv[2]->i << ", "
    //      << argv[3]->i << endl;
    
    auto n = argv[0]->i;
    set_led(n, led_t(argv[1]->i, argv[2]->i, argv[3]->i));

    return 0;
}


int OSCServer::osc_method_led_float(lo_arg **argv)
{
    // cout << "/ledf (" << ++received << "): "
    //      << argv[0]->i << ", " 
    //      << argv[1]->f << ", " 
    //      << argv[2]->f << ", "
    //      << argv[3]->f << endl;
    
    auto n = argv[0]->i;
    set_led(n, led_t(argv[1]->f * 255,
                     argv[2]->f * 255,
                     argv[3]->f * 255));

    return 0;
}


int OSCServer::osc_method_bead(lo_arg **argv)
{
    // cout << "/bead (" << ++received << "): "
    //      << argv[0]->i << ", " 
    //      << argv[1]->i << ", " 
    //      << argv[2]->i << ", "
    //      << argv[3]->i << endl;
    
    auto n = argv[0]->i * m_leds_per_bead;
    for (int offset = 0; offset < m_leds_per_bead; offset++) {
        set_led(n + offset, led_t(argv[1]->i, argv[2]->i, argv[3]->i));
    }        

    return 0;
}


int OSCServer::osc_method_bead_float(lo_arg **argv)
{
    // cout << "/beadf (" << ++received << "): "
    //      << argv[0]->i << ", " 
    //      << argv[1]->f << ", " 
    //      << argv[2]->f << ", "
    //      << argv[3]->f << endl;
    
    auto n = argv[0]->i * m_leds_per_bead;
    for (int offset = 0; offset < m_leds_per_bead; offset++) {
        set_led(n + offset, led_t(argv[1]->f * 255, argv[2]->f * 255, argv[3]->f * 255));
    }        

    return 0;
}


int OSCServer::osc_method_update(lo_arg **argv)
{
    for (auto it = m_led_ifaces.begin(); it != m_led_ifaces.end(); ++it) {
        (*it)->notify_update_thread();
    }
}

// create an led_interface and added to m_led_ifaces
int OSCServer::bind(shared_ptr<IPlatformSerial> const ser, OSCLedConfig::interface_config const &cfg)
{
    shared_ptr<led_interface> led_iface(new led_interface(ser, cfg));
    
    m_led_ifaces.push_back(led_iface);

    m_iface_count++;
    
    return m_iface_count;
}


// remove all active LED interfaces
// this is provided to allow for the config to be reloaded w/o restarting the process
int OSCServer::drop_interfaces()
{
    m_led_ifaces.clear();
    m_iface_count=0;
}


void OSCServer::set_all_led(led_t led)
{
    for (auto it = m_led_ifaces.begin(); it != m_led_ifaces.end(); ++it) {
        auto iface = *it;
        for (int led_num = iface->m_base; led_num < iface->m_base + iface->m_len; led_num++) {
            set_led(led_num, led);
        }
        iface->notify_update_thread();
    }
}

void OSCServer::test_sequence()
{
    const int test_color_len = 7;
    led_t test_color[] = {
        {1, 0, 0},
        {0, 1, 0},
        {0, 0, 1},
        {1, 1, 0},
        {0, 1, 1},
        {1, 0, 1},
        {1, 1, 1},
    };

    // avoid a race and wait for update_thread() to spawn for all interfaces
    for (auto it = m_led_ifaces.begin(); it != m_led_ifaces.end(); ++it) {
        while (! (*it)->run_update_thread)
            usleep(100000);
    }

    // show off all our colors
    for (int color = 0; color < test_color_len; color++) {

        // fade in
        for (int brightness = 0; brightness < 255; brightness++) {
            set_all_led(led_t(test_color[color].r * brightness,
                              test_color[color].g * brightness,
                              test_color[color].b * brightness));
            usleep(6000);
        }

        usleep(20000);

        // fade out
        for (int brightness = 255; brightness > 0; brightness--) {
            set_all_led(led_t(test_color[color].r * brightness,
                              test_color[color].g * brightness,
                              test_color[color].b * brightness));
            usleep(6000);
        }

        usleep(20000);

        // break out if m_running is false
        // this is to support SIGTERM handler during test sequence
        if (! *m_running) {
            return;
        }

    }
    usleep(10000);

    // display version number
}


shared_ptr<OSCServer::ILEDDataFormat> OSCServer::LEDDataFormatFactory::create_led_format(OSCLedConfig::interface_config const &cfg)
{
    shared_ptr<OSCServer::ILEDDataFormat> fmt;

    cout << "led_type = " << cfg.led_type << endl;
    
    // ws2801 is used in the 36mm "pixel" LED modules
    if (cfg.led_type == string("ws2801")) {
        fmt.reset(new LEDFormat_WS2801(cfg));
        return fmt;
    }

    if (cfg.led_type == string("apa102")) {
        fmt.reset(new LEDFormat_APA102(cfg));
        return fmt;
    }

    cout << "unknown led_type = " << cfg.led_type << endl;

    return NULL;
}

// ws2801 is used in the 36mm "pixel" LED modules
OSCServer::LEDFormat_WS2801::LEDFormat_WS2801(OSCLedConfig::interface_config const &cfg) :
    ILEDDataFormat(cfg) {

    buf_len = cfg.led_count * 3;
    buf = new uint8_t[buf_len];

    // make sure offsets are defined
    m_r_offset = 0;
    m_g_offset = 1;
    m_b_offset = 2;

    // parse byte_order string
    for (int i = 0; i < cfg.byte_order.length(); i++) {
        switch (cfg.byte_order[i]) {
        case 'r':
            m_r_offset = i;
            break;
        case 'g':
            m_g_offset = i;
            break;
        case 'b':
            m_b_offset = i;
            break;
        }
    }
}    


void OSCServer::LEDFormat_WS2801::update(vector<led_t> const &leds)
{
    size_t i = 0;
    
    for (auto it = leds.begin(); it != leds.end(); ++it) {
        //cout << "update:" << ": " << int(it->r) << ", " << int(it->g) << ", " << int(it->b) << endl;
        
        buf[i + m_r_offset] = it->r;
        buf[i + m_g_offset] = it->g;
        buf[i + m_b_offset] = it->b;
        i += 3;
    }
}

// APA102 is used in the "dotstar" LED strips
OSCServer::LEDFormat_APA102::LEDFormat_APA102(OSCLedConfig::interface_config const &cfg) :
    ILEDDataFormat(cfg) {

    buf_len = (cfg.led_count * 4) + 8;
    buf = new uint8_t[buf_len];

    // frame header
    buf[0] = 0x00;
    buf[1] = 0x00;
    buf[2] = 0x00;
    buf[3] = 0x00;

    // frame footer
    buf[buf_len - 4] = 0xff;
    buf[buf_len - 3] = 0xff;
    buf[buf_len - 2] = 0xff;
    buf[buf_len - 1] = 0xff;

    m_brightness = cfg.brightness;
    // max value is 31
    if (m_brightness > 31) {
        m_brightness = 31;
    }
}

void OSCServer::LEDFormat_APA102::update(vector<led_t> const &leds)
{
    size_t i = 4;
    
    for (auto it = leds.begin(); it != leds.end(); ++it) {
        //cout << "update:" << ": " << int(it->r) << ", " << int(it->g) << ", " << int(it->b) << endl;
        
        // 0xff means "use the default"
        // otherwise, take the value from led_t
        // format: 111xxxxx where xxxxx = brightness
        if (it->brightness == 0xff) {
            buf[i + 0] = m_brightness | 0xe0;  
        } else {
            buf[i + 0] = it->brightness | 0xe0;
        }

        buf[i + 1] = it->b;
        buf[i + 2] = it->g;
        buf[i + 3] = it->r;
        i += 4;
    }
}


OSCServer::led_interface::led_interface(std::shared_ptr<IPlatformSerial> const ser,
                                        OSCLedConfig::interface_config const &cfg) :
    m_ser(ser) {

    run_update_thread = false;

    m_base = cfg.led_base;
    m_len = cfg.led_count;
    m_reverse = cfg.reversed;

    // initialize leds with zero-value leds
    for (auto i = 0; i < m_len; i++) {
        leds.push_back(led_t(0,0,0));
    }

    OSCServer::LEDDataFormatFactory led_fmt_factory;
    //shared_ptr<OSCServer::ILEDDataFormat> led_format(led_format = led_fmt_factory.create_led_format(cfg));
    m_fmt = led_fmt_factory.create_led_format(cfg);

    t_update = std::thread(&OSCServer::led_interface::update_thread, this);
};


OSCServer::led_interface::~led_interface() {
    run_update_thread = false;
    t_update.join();
    delete led_buf;
}


void OSCServer::led_interface::set_led(int offset, led_t led)
{
    // cout << "set_led(" << offset << "," << int(led.r)  << "," << int(led.g)  << "," << int(led.b)  << ")" << endl;

    lock_guard<mutex> lock(leds_mutex);
    leds.at(offset) = led;
}


void OSCServer::led_interface::update_led_buf()
{
    {
        lock_guard<mutex> lock(leds_mutex);
        m_fmt->update(leds);
    }
    m_ser->send(m_fmt->buf, m_fmt->buf_len);
}


void OSCServer::led_interface::update_thread()
{
    run_update_thread = true;

    while (run_update_thread) {
        // I don't care about spurious wakeups, so I won't implement
        // a "ready" variable
        {
            unique_lock<mutex> lock(update_mutex);
            update_cv.wait(lock);
            update_led_buf();
        }
    }
}


void OSCServer::led_interface::notify_update_thread()
{
    unique_lock<mutex> lock(update_mutex);
    update_cv.notify_all();
}



