
#include <lo/lo.h>
#include <lo/lo_cpp.h>
#include <err.h>
#include <unistd.h>

#include <vector>
#include <atomic>
#include <iostream>

#include "IPlatformSerial.h"
#include "OSCServer.h"

using namespace std;

OSCServer::led_interface::led_interface(std::shared_ptr<IPlatformSerial> ser, int base, int len, bool reverse) :
    m_ser(ser), m_base(base), m_len(len), m_reverse(reverse) {
    led_buf = new uint8_t[(m_len * 3)];

    // initialize leds with zero-value leds
    for (auto i = 0; i < len; i++) {
        leds.push_back(led_t(0,0,0));
    }

    t_update = std::thread(&OSCServer::led_interface::update_thread, this);
};


OSCServer::led_interface::~led_interface() {
    run_update_thread = false;
    t_update.join();
    delete led_buf;
}


OSCServer::OSCServer(int port) : m_port(port)
{
    cout << "starting server on port " << port << endl;

    received = 0;
    m_iface_count = 0;

    //m_st.reset(new lo::ServerThread("225.0.0.37", port));
    m_st.reset(new lo::ServerThread(port));

    if (!m_st->is_valid()) {
        err(1, "can't create liblo server thread");
        return;
    }

    m_st->add_method("/led", "iiii", 
                    [this](lo_arg **argv, int)  {this->osc_method_led(argv);});
    m_st->add_method("/ledf", "ifff", 
                    [this](lo_arg **argv, int)  {this->osc_method_led_float(argv);});
    m_st->add_method("/bead", "iiii", 
                    [this](lo_arg **argv, int)  {this->osc_method_bead(argv);});
    m_st->add_method("/beadf", "ifff", 
                     [this](lo_arg **argv, int)  {this->osc_method_bead_float(argv);});

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
    cout << "/led (" << ++received << "): "
         << argv[0]->i << ", " 
         << argv[1]->i << ", " 
         << argv[2]->i << ", "
         << argv[3]->i << endl;
    
    auto n = argv[0]->i;
    set_led(n, led_t(argv[1]->i, argv[2]->i, argv[3]->i));

    return 0;
}


int OSCServer::osc_method_led_float(lo_arg **argv)
{
    cout << "/ledf (" << ++received << "): "
         << argv[0]->i << ", " 
         << argv[1]->f << ", " 
         << argv[2]->f << ", "
         << argv[3]->f << endl;
    
    auto n = argv[0]->i;
    set_led(n, led_t(argv[1]->f * 255,
                     argv[2]->f * 255,
                     argv[3]->f * 255));

    return 0;
}


int OSCServer::osc_method_bead(lo_arg **argv)
{
    cout << "/bead (" << ++received << "): "
         << argv[0]->i << ", " 
         << argv[1]->i << ", " 
         << argv[2]->i << ", "
         << argv[3]->i << endl;
    
    auto n = argv[0]->i * m_leds_per_bead;
    for (int offset = 0; offset < m_leds_per_bead; offset++) {
        set_led(n + offset, led_t(argv[1]->i, argv[2]->i, argv[3]->i));
    }        

    // for (auto it = m_led_ifaces.begin(); it != m_led_ifaces.end(); ++it) {
    //     (*it)->update_led_buf();
    // }

    return 0;
}


int OSCServer::osc_method_bead_float(lo_arg **argv)
{
    cout << "/beadf (" << ++received << "): "
         << argv[0]->i << ", " 
         << argv[1]->f << ", " 
         << argv[2]->f << ", "
         << argv[3]->f << endl;
    
    auto n = argv[0]->i * m_leds_per_bead;
    for (int offset = 0; offset < m_leds_per_bead; offset++) {
        set_led(n + offset, led_t(argv[1]->f * 255, argv[2]->f * 255, argv[3]->f * 255));
    }        

    return 0;
}


// create an led_interface and added to m_led_ifaces
int OSCServer::bind(shared_ptr<IPlatformSerial> ser, int base, int len, bool reverse)
{
    shared_ptr<led_interface> led_iface(new led_interface(ser, base, len, reverse));
    
    m_led_ifaces.push_back(led_iface);

    m_iface_count++;
    
    return m_iface_count;
}


void OSCServer::led_interface::set_led(int offset, led_t led)
{
    //cout << "set_led(" << offset << "," << int(led.r)  << "," << int(led.g)  << "," << int(led.b)  << ")" << endl;

    lock_guard<mutex> lock(led_buf_mutex);
    leds.at(offset) = led;
}


void OSCServer::led_interface::update_led_buf()
{
    size_t i = 0;
    lock_guard<mutex> lock(led_buf_mutex);
    for (auto it = leds.begin(); it != leds.end(); ++it) {
        //cout << "update:" << ": " << int(it->r) << ", " << int(it->g) << ", " << int(it->b) << endl;
        led_buf[i] = it->r;
        led_buf[i+1] = it->g;
        led_buf[i+2] = it->b;
        i += 3;
    }
    m_ser->send(led_buf, m_len * 3);
}


void OSCServer::led_interface::update_thread()
{
    run_update_thread = true;

    // this should update 10 to 20 times / second
    while (run_update_thread) {
        update_led_buf();
        usleep(50000);
    }
}
