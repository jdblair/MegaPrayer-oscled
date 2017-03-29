
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
static atomic<int> running;


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
    OSCServer server(config.get_station().port);
    server.set_base_bead(config.get_station().bead_base);
    server.set_leds_per_bead(config.get_station().leds_per_bead);

    for (auto i = config.get_station().interface.begin(); i != config.get_station().interface.end(); i++) {
        std::shared_ptr<IPlatformSerial> ser = ser_factory.create_platform_serial((*i)->id);
        server.bind(ser, (*i)->led_base, (*i)->led_count, (*i)->reversed);
        cout << "created iface: " << (*i)->id <<
            ", led_base: " << (*i)->led_base <<
            ", led_count: " << (*i)->led_count <<
            ", reversed: " << (*i)->reversed << endl;
    }

    if (config.get_station().daemonize) {
        daemonize();
    } else {
        server.start();
    }

    running = 1;
    while (running) {
        sleep(1);
    }

    cout << "exiting." << endl;
    exit(0);
}

