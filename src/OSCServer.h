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
#include <atomic>

#include "IPlatformSerial.h"
#include "OSCLedConfig.hpp"


class OSCServer {
 public:
    typedef struct led {
    led(uint8_t r_arg, uint8_t g_arg, uint8_t b_arg, uint8_t brightness_arg=0xff) :
        r(r_arg), g(g_arg), b(b_arg), brightness(brightness_arg) {};
        uint8_t r;
        uint8_t g;
        uint8_t b;
        uint8_t brightness;  // used by apa102 LEDs, value is 0 to 31
    } led_t;

    OSCServer(std::atomic<bool> *running, std::string ip, std::string port);

    int bind(std::shared_ptr<IPlatformSerial> const ser, OSCLedConfig::interface_config const &cfg);
    int drop_interfaces();
    void start() { m_st->start(); };
    int osc_method_led(lo_arg **argv);
    int osc_method_led_float(lo_arg **argv);
    int osc_method_bead(lo_arg **argv);
    int osc_method_bead_float(lo_arg **argv);
    int osc_method_update(lo_arg **argv);
    void set_led(int n, led_t led);
    void set_all_led(led_t led);
    void test_sequence();
    
    class ILEDDataFormat {
    public:
        uint8_t *buf;
        size_t buf_len;

    protected:
        OSCLedConfig::interface_config m_cfg;

    public:        
    ILEDDataFormat(OSCLedConfig::interface_config const &cfg) :
        m_cfg(cfg) {};

        uint8_t *get_buf() { return buf; };
        size_t get_buf_len() { return buf_len; };
        virtual void update(std::vector<led_t> const &leds) {
            std::cout << "ILEDDataFormat not over-ridden" << std::endl;
        }
        ~ILEDDataFormat() { if (buf) delete buf; };
    };

    class LEDDataFormatFactory {
    public:
        LEDDataFormatFactory() {};
        std::shared_ptr<OSCServer::ILEDDataFormat> create_led_format(OSCLedConfig::interface_config const &cfg);
    };
        
    class LEDFormat_WS2801 : public ILEDDataFormat {
    public:
        LEDFormat_WS2801(OSCLedConfig::interface_config const &cfg);
        void update(std::vector<led_t> const &leds);
    private:
        int m_r_offset;
        int m_g_offset;
        int m_b_offset;
    };
        
    class LEDFormat_APA102 : public ILEDDataFormat {
    public:
        LEDFormat_APA102(OSCLedConfig::interface_config const &cfg);
        void update(std::vector<led_t> const &leds);
    private:
        int m_brightness;
    };

        
    // led_interface encapsulates the physical serial interface and the state
    // of all connected LED modules.
    class led_interface {
    public:
        void update_thread();

        led_interface(std::shared_ptr<IPlatformSerial> const ser, OSCLedConfig::interface_config const &cfg);

        ~led_interface();

        void update_led_buf();

        //int iface;
        std::shared_ptr<IPlatformSerial> m_ser;
        int m_base;
        int m_len;
        bool m_reverse;
        int m_r_offset;
        int m_g_offset;
        int m_b_offset;

        std::vector<led_t> leds;
        uint8_t *led_buf;
        std::thread t_update;
        std::atomic<bool> run_update_thread;

        std::mutex leds_mutex;

        std::mutex update_mutex;
        std::condition_variable update_cv;

        std::shared_ptr<ILEDDataFormat> m_fmt;

        void set_led(int offset, led_t led);
        void notify_update_thread();
    };

    int m_leds_per_bead;
    int m_base_bead;
    void set_leds_per_bead(int leds_per_bead) { m_leds_per_bead = leds_per_bead; };
    void set_base_bead(int base_bead) { m_base_bead = base_bead; };

 private:
    std::string m_port;
    std::string m_ip;
    std::atomic<bool> *m_running;
    std::shared_ptr<lo::ServerThread> m_st;
    
    std::atomic<int> received;

    int m_iface_count;

    std::vector<std::shared_ptr<led_interface>> m_led_ifaces;
};




#endif /* OSCSERVER_H */
