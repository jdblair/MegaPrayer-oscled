
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <syslog.h>

#include "IPlatformSerial.h"
#include "PlatformSerialFactory.h"
#include "OSCServer.h"
#include "OSCLedConfig.hpp"

#include <memory>
#include <atomic>

#include "config.h"

using namespace std;


// used to exit the main process on SIGINT and SIGKILL
static atomic<bool> running;


void sig_handler(int signo)
{
    cout << "sig_handler " << signo << endl;

    switch (signo) {
    case SIGINT:
    case SIGKILL:
        running = 0;
        break;
    }
}


static void daemonize()
{
    pid_t pid;

    pid = fork();

    if (pid < 0)
        exit(EXIT_FAILURE);

    if (pid > 0)
        exit(EXIT_SUCCESS);

    signal(SIGCHLD, SIG_IGN);    
}


void startup_lightshow(OSCServer &server, OSCLedConfig &config)
{
    auto station = config.get_station();

    server.test_sequence();

    // display version number
    server.set_all_led(OSCServer::led_t(0, 0, 0));
    server.show_value(config.m_version.minor, 4, station.bead_base, OSCServer::led_t(0, 0, 255), OSCServer::led_t(255, 0, 0));
    server.show_value(config.m_version.major, 4, station.bead_base + 5, OSCServer::led_t(0, 0, 255), OSCServer::led_t(255, 0, 0));

    // give us a chance to see the version number
    sleep(5);
}


int main(int argc, char **argv)
{
    OSCLedConfig &config = OSCLedConfig::getInstance();

    // signal handler
    signal(SIGINT, sig_handler);
    signal(SIGKILL, sig_handler);

    // parse command line and json config
    config.getopt(argc, argv);
    config.json_parse();

    PlatformSerialFactory ser_factory;
    OSCServer server(&running, config.get_station().ip, config.get_station().port);
    server.set_base_bead(config.get_station().bead_base);
    server.set_leds_per_bead(config.get_station().leds_per_bead);

    for (auto i = config.get_station().interface.begin(); i != config.get_station().interface.end(); i++) {
        std::shared_ptr<IPlatformSerial> ser = ser_factory.create_platform_serial((*i)->id);
        if ( ser) {
        server.bind(ser, *(*i));
        cout << "created iface: " << (*i)->id <<
            ", led_base: " << (*i)->led_base <<
            ", led_count: " << (*i)->led_count <<
            ", reversed: " << (*i)->reversed <<
            ", led_type: " << (*i)->led_type <<
            ", byte_order: " << (*i)->byte_order << endl;
        } else {
            cout << "interface id " << (*i)->id << " does not exist" << endl;
        }
    }

    if (config.get_station().daemonize) {
        daemonize();
    }

    running = 1;

    startup_lightshow(server, config);

    server.start();
    //cout << "after server start\n";

    while (running) {
        sleep(1);
    }

    cout << "exiting." << endl;
    exit(0);
}

