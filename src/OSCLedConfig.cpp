
#include <getopt.h>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <err.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "json/json.h"
#include "config.h"

#include "OSCLedConfig.hpp"

using namespace std;

// string constants used for config file parsing
const string OSCLedConfig::KEY_DEFAULTS = "defaults";
const string OSCLedConfig::KEY_ID = "id";
const string OSCLedConfig::KEY_STATION = "station";
const string OSCLedConfig::KEY_IFACE = "interface";
const string OSCLedConfig::KEY_IP = "ip";
const string OSCLedConfig::KEY_PORT = "port";
const string OSCLedConfig::KEY_LEDS_PER_BEAD = "leds_per_bead";
const string OSCLedConfig::KEY_BEAD_COUNT = "bead_count";
const string OSCLedConfig::KEY_BEAD_BASE = "bead_base";
const string OSCLedConfig::KEY_DAEMONIZE = "daemonize";
const string OSCLedConfig::KEY_IFACE_ID = "id";
const string OSCLedConfig::KEY_IFACE_LED_BASE = "led_base";
const string OSCLedConfig::KEY_IFACE_LED_COUNT = "led_count";
const string OSCLedConfig::KEY_IFACE_REVERSED = "reversed";


OSCLedConfig::OSCLedConfig()
{
    // set all configuration defaults
    // this can be over-ridden by the "defaults" section of the config file
    m_default.id = 0;
    m_default.ip = string("127.0.0.1");
    m_default.port = 5005;
    m_default.leds_per_bead = 8;
    m_default.bead_count = 10;
    m_default.bead_base = 0;

    m_cmd_line_config.config_file = string("/etc/mp/config.json");
    m_cmd_line_config.id = 0;
    m_cmd_line_config.daemonize = false;
    m_cmd_line_config.port = 5005;
    m_cmd_line_config.config_file_set = false;
    m_cmd_line_config.id_set = false;
    m_cmd_line_config.daemonize_set = false;
    m_cmd_line_config.ip_set = false;
    m_cmd_line_config.port_set = false;
}


// FIXME: this doesn't do any error checking
// if the file fails to load we get an empty json_root
bool OSCLedConfig::json_parse()
{
    struct stat stat_buf;
    if (stat(m_cmd_line_config.config_file.c_str(), &stat_buf) != 0) {
        err(1, "%s", m_cmd_line_config.config_file.c_str()); // does not return
        return false;
    }

    ifstream config_doc(m_cmd_line_config.config_file, ifstream::binary);
    bool rc = false;

    try {
        config_doc >> json_root;
    } catch (const std::exception &e) {
        cout << "Error parsing " << m_cmd_line_config.config_file << ":" << endl;
        cout << e.what();
        exit(1);
    }

    if (json_root.isMember(KEY_DEFAULTS))
        rc = json_parse_station_values(json_root[KEY_DEFAULTS], m_default);

    if (rc == false) {
        cout << "json_parse_station_values() returned false" << endl;
        return false;
    }

    rc = json_parse_station();

    return rc;
}


// this is used to parse both the default station config and the
// actual station config
bool OSCLedConfig::json_parse_station_values(Json::Value s, OSCLedConfig::station_config& config)
{
    // note that "id" cannot be set in the default
    m_config.ip = s.get(KEY_IP, m_default.ip).asString();
    m_config.port = s.get(KEY_PORT, m_default.port).asInt();
    m_config.leds_per_bead = s.get(KEY_LEDS_PER_BEAD, m_default.leds_per_bead).asInt();
    m_config.bead_count = s.get(KEY_BEAD_COUNT, m_default.bead_count).asInt();
    m_config.bead_base = s.get(KEY_BEAD_BASE, m_default.bead_base).asInt();
    m_config.daemonize = s.get(KEY_DAEMONIZE, m_default.daemonize).asBool();

    // over-ride with command line arguments
    if (m_cmd_line_config.ip_set)
        m_config.ip = m_cmd_line_config.ip;

    if (m_cmd_line_config.port_set)
        m_config.port = m_cmd_line_config.port;

    if (m_cmd_line_config.daemonize_set)
        m_config.daemonize = m_cmd_line_config.daemonize;
    
    if (s.isMember(KEY_IFACE)) {
        // protect against being called more than once by removing all
        // existing elements from the interface vector
        m_config.interface.clear();

        for (auto i = s[KEY_IFACE].begin(); i != s[KEY_IFACE].end(); i++) {
            shared_ptr<struct interface_config> iface_ptr;
            iface_ptr.reset(new struct interface_config);
            m_config.interface.push_back(iface_ptr);

            iface_ptr->id = i->get(KEY_IFACE_ID, 0).asInt();
            iface_ptr->led_base = i->get(KEY_IFACE_LED_BASE, 0).asInt();
            iface_ptr->led_count = i->get(KEY_IFACE_LED_COUNT, 10).asInt();
            iface_ptr->reversed = i->get(KEY_IFACE_REVERSED, false).asBool();
        }
    }

    // cout << "json_parse_station_values():" << endl;
    // cout << config.ip << endl;
    // cout << config.port << endl;
    // cout << config.leds_per_bead << endl;
    // cout << config.bead_count << endl;
    // cout << config.bead_base << endl;
    // cout << config.daemonize << endl;

    return true;
}

// find the current station and parse the values
bool OSCLedConfig::json_parse_station()
{
    if (json_root.isMember(KEY_STATION)) {
        json_station = json_root[KEY_STATION];
        for (auto i = json_station.begin(); i != json_station.end(); i++) {
            if (i->get(KEY_ID, 0).asInt() == m_config.id) {
                json_parse_station_values(*i, m_default);
                return true;
            }
        }
    }

    // station not found
    return false;
}

const Json::Value OSCLedConfig::json_interface(const int num)
{
    const Json::Value station = json_parse_station();

    if (station.isMember(KEY_IFACE)) {
        const Json::Value interface = station[KEY_IFACE];
        for (auto i = interface.begin(); i != interface.end(); i++) {
            if (station.isMember(KEY_IFACE_ID)) {
                if (i->get(KEY_IFACE_ID, 0).asInt() == num) {
                    return *i;
                }
            }
        }
    }

    return Json::Value();
}


bool OSCLedConfig::getopt(int argc, char * const argv[])
{
    int c;
    
    while (1) {
        int option_index = 0;
        static struct option long_options[] = {
            {"version", no_argument, 0, 'v'},
            {"config", required_argument, 0, 'c'},
            {"id", required_argument, 0, 'i'},
            {"daemonize", no_argument, 0, 'd'},
            {"ip", required_argument, 0, 'I'},
            {"port", required_argument, 0, 'p'},
            {0, 0, 0}
        };
        
        c = getopt_long(argc, argv, "vc:i:d", long_options, &option_index);
        if (c == -1)
            break;
        
        switch (c) {
        case 'c':
            m_cmd_line_config.config_file = string(optarg);
            m_cmd_line_config.config_file_set = true;
            break;

        case 'i':
            // using sscanf() b/c i don't want to deal with cross-linking boost::lexical_cast
            if (sscanf(optarg, "%d", &m_cmd_line_config.id) != 1) {
                err(1, "can't parse --id/-i argument");
                return false;  // err() doesn't return
            }
            m_cmd_line_config.id_set = true;
            
            break;
        
        case 'd':
            cout << "damonize = true\n";
            m_cmd_line_config.daemonize = true;
            m_cmd_line_config.daemonize_set = true;
            break;

        case 'I':
            m_cmd_line_config.ip = string(optarg);
            m_cmd_line_config.ip_set = true;
            break;

        case 'p':
            if (sscanf(optarg, "%d", &m_cmd_line_config.port) != 1) {
                err(1, "can't parse --port/-p argument");
                return false;  // err() doesn't return
            }
            m_cmd_line_config.port_set = true;

        case 'v':
            cout << PACKAGE_STRING << " " << USE_PLATFORM_SERIAL << " " << GIT_HASH << endl;
            exit(0);
            break;

        case '?':
            break;

        case -1:
            break;
        }
        
    }

    return true;
}

