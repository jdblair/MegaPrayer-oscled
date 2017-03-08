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
    int method_led(lo_arg **argv);

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

 private:
    int m_port;
    std::shared_ptr<lo::ServerThread> m_st;
    
    std::atomic<int> received;

    int m_iface_count;

    std::vector<std::shared_ptr<led_interface>> m_led_ifaces;
};




#endif /* OSCSERVER_H */
