
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


OSCServer::led_interface::led_interface(std::shared_ptr<IPlatformSerial> ser,
                                        OSCLedConfig::interface_config &cfg) :
    m_ser(ser) {

    m_base = cfg.led_base;
    m_len = cfg.led_count;
    m_reverse = cfg.reversed;
    
    led_buf = new uint8_t[(m_len * 3)];

    // initialize leds with zero-value leds
    for (auto i = 0; i < m_len; i++) {
        leds.push_back(led_t(0,0,0));
    }

    t_update = std::thread(&OSCServer::led_interface::update_thread, this);

    // make sure offset are defined
    m_r_offset = 0;
    m_g_offset = 1;
    m_b_offset = 2;

    // parse byte_order string
    for (int i = 0; i < cfg.byte_order.length(); i++) {
        switch (cfg.byte_order[i]) {
        case 'r':
        case 'R':
            m_r_offset = i;
            break;
        case 'g':
        case 'G':
            m_g_offset = i;
            break;
        case 'b':
        case 'B':
            m_b_offset = i;
            break;
        }
    }

};


OSCServer::led_interface::~led_interface() {
    run_update_thread = false;
    t_update.join();
    delete led_buf;
}


OSCServer::OSCServer(string ip, string port) : m_ip(ip), m_port(port)
{
    received = 0;
    m_iface_count = 0;
    
    lo_server_thread osc_st;
    struct sockaddr_in sa;
    
    // is ip a multicast address?
    inet_pton(AF_INET, ip.c_str(), &(sa.sin_addr));  // convert to 4-byte ipv4 address
    uint32_t addr = ntohl(sa.sin_addr.s_addr);       // cast as uint32_t
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
        // (*it)->update_led_buf();
        (*it)->notify_update_thread();
    }
}

// create an led_interface and added to m_led_ifaces
int OSCServer::bind(shared_ptr<IPlatformSerial> ser,  OSCLedConfig::interface_config &cfg)
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


void OSCServer::led_interface::set_led(int offset, led_t led)
{
    //cout << "set_led(" << offset << "," << int(led.r)  << "," << int(led.g)  << "," << int(led.b)  << ")" << endl;

    lock_guard<mutex> lock(led_buf_mutex);
    leds.at(offset) = led;
}


void OSCServer::led_interface::update_led_buf()
{
    size_t i = 0;
    {
        lock_guard<mutex> lock(led_buf_mutex);
        for (auto it = leds.begin(); it != leds.end(); ++it) {
            //cout << "update:" << ": " << int(it->r) << ", " << int(it->g) << ", " << int(it->b) << endl;
            
            led_buf[i + m_r_offset] = it->r;
            led_buf[i + m_g_offset] = it->g;
            led_buf[i + m_b_offset] = it->b;
            i += 3;
        }
    }
    m_ser->send(led_buf, m_len * 3);
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
