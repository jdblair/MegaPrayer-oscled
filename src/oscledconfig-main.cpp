
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <syslog.h>

#include "OSCServer.h"
#include "OSCLedConfig.hpp"

#include <memory>
#include <atomic>

#include "config.h"

using namespace std;


// used to exit the main process on SIGINT and SIGKILL
static atomic<bool> running;


int main(int argc, char **argv)
{
    OSCLedConfig &config = OSCLedConfig::getInstance();

    // parse command line and json config
    config.getopt(argc, argv);
    config.json_parse();
    
    cout << "cmd_line_config:" << endl <<
        "  config_file: " << config.m_cmd_line_config.config_file << endl <<
        "  id: " << config.m_cmd_line_config.id << endl <<
        "  daemonize: " << config.m_cmd_line_config.daemonize << endl <<
        "  startup_test: " << config.m_cmd_line_config.startup_test << endl <<
        "  ip: " << config.m_cmd_line_config.ip << endl <<
        "  port: " << config.m_cmd_line_config.port << endl << endl;
    
    for (auto i = config.get_station().interface.begin(); i != config.get_station().interface.end(); i++) {
        cout << "iface: " << (*i)->id << endl <<
            "  iface_class: " << (*i)->iface_class << endl <<
            "  led_base: " << (*i)->led_base << endl <<
            "  led_count: " << (*i)->led_count << endl <<
            "  reversed: " << (*i)->reversed << endl <<
            "  led_type: " << (*i)->led_type << endl <<
            "  byte_order: " << (*i)->byte_order << endl <<
            "  brightness: " << (*i)->brightness << endl <<
            "  white_boost: " << (*i)->white_boost << endl <<
            "  xform: " << (*i)->xform.r << ", " << (*i)->xform.g << ", "  << (*i)->xform.b << endl << endl;
    }

    exit(0);
}

