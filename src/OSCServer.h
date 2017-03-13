/*
 * OSCServer.h
 *
 */

#ifndef OSCSERVER_H
#define OSCSERVER_H

#include <stdint.h>

#include <lo/lo.h>
#include <lo/lo_cpp.h>

#include <vector>
#include <iostream>
#include <atomic>
#include <mutex>
#include <condition_variable>
#include <thread>

#include "IPlatformSerial.h"


class OSCServer {
 private:
    typedef struct led {
    led(uint8_t r_arg, uint8_t g_arg, uint8_t b_arg) :
        r(r_arg), g(g_arg), b(b_arg) {};
        uint8_t r;
        uint8_t g;
        uint8_t b;
    } led_t;

 public:
    OSCServer(int port);

    int bind(std::shared_ptr<IPlatformSerial> ser, int base, int len, bool reverse);
    int start() { m_st->start(); };
    int osc_method_led(lo_arg **argv);
    int osc_method_led_float(lo_arg **argv);
    int osc_method_bead(lo_arg **argv);
    int osc_method_bead_float(lo_arg **argv);
    void set_led(int n, led_t led);

    class led_interface {
    public:
        void update_thread();

    led_interface(std::shared_ptr<IPlatformSerial> ser, int base, int len, bool reverse) :
        m_ser(ser), m_base(base), m_len(len), m_reverse(reverse) {
            led_buf = new uint8_t[m_len * 3];
            t_update = std::thread(&OSCServer::led_interface::update_thread, this);
        };
        
        ~led_interface() {
            run_update_thread = false;
            t_update.join();
            delete led_buf;
        }

        void update_led_buf();

        //int iface;
        std::shared_ptr<IPlatformSerial> m_ser;
        int m_base;
        int m_len;
        bool m_reverse;

        std::vector<led_t> leds;
        uint8_t *led_buf;
        std::mutex update_mutex;
        std::thread t_update;
        bool run_update_thread;

        void set_led(int offset, led_t led);
    };

    int m_leds_per_bead;
    int m_base_bead;
    void set_leds_per_bead(int leds_per_bead) { m_leds_per_bead = leds_per_bead; };
    void set_base_bead(int base_bead) { m_base_bead = base_bead; };

 private:
    int m_port;
    std::shared_ptr<lo::ServerThread> m_st;
    
    std::atomic<int> received;

    int m_iface_count;

    std::vector<std::shared_ptr<led_interface>> m_led_ifaces;
};




#endif /* OSCSERVER_H */
