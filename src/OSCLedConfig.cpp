
#include <getopt.h>
#include <iostream>
#include <fstream>
#include <string>
#include <locale>
#include <stdio.h>
#include <err.h>
#include <algorithm>

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

#include "json/json.h"
#include "config.h"

#include "OSCLedConfig.hpp"

using namespace std;

// string constants used for config file parsing
const string OSCLedConfig::KEY_GLOBAL = "global";
const string OSCLedConfig::KEY_ID = "id";
const string OSCLedConfig::KEY_STATION = "station";
const string OSCLedConfig::KEY_IFACE = "interface";
const string OSCLedConfig::KEY_IP = "ip";
const string OSCLedConfig::KEY_PORT = "port";
const string OSCLedConfig::KEY_LEDS_PER_BEAD = "leds_per_bead";
const string OSCLedConfig::KEY_BEAD_COUNT = "bead_count";
const string OSCLedConfig::KEY_BEAD_BASE = "bead_base";
const string OSCLedConfig::KEY_DAEMONIZE = "daemonize";
const string OSCLedConfig::KEY_STARTUP_TEST = "startup_test";
const string OSCLedConfig::KEY_IFACE_ID = "id";
const string OSCLedConfig::KEY_IFACE_LED_BASE = "led_base";
const string OSCLedConfig::KEY_IFACE_LED_COUNT = "led_count";
const string OSCLedConfig::KEY_IFACE_REVERSED = "reversed";
const string OSCLedConfig::KEY_IFACE_BYTE_ORDER = "byte_order";
const string OSCLedConfig::KEY_IFACE_BRIGHTNESS = "brightness";
const string OSCLedConfig::KEY_IFACE_LED_TYPE = "led_type";
const string OSCLedConfig::KEY_IFACE_XFORM = "xform";
const string OSCLedConfig::KEY_IFACE_XFORM_R = "r";
const string OSCLedConfig::KEY_IFACE_XFORM_G = "g";
const string OSCLedConfig::KEY_IFACE_XFORM_B = "b";
const string OSCLedConfig::KEY_IFACE_CLASS = "class";
const string OSCLedConfig::KEY_IFACE_WHITE_BOOST = "white_boost";

OSCLedConfig::OSCLedConfig()
{
    // set all configuration defaults
    // this can be over-ridden by the "defaults" section of the config file
    m_default.iface_class = string("rosary");
    m_default.id = 0;
    m_default.ip = string("127.0.0.1");
    m_default.port = string("5005");
    m_default.leds_per_bead = 8;
    m_default.bead_count = 10;
    m_default.bead_base = 0;
    m_default.byte_order = string("rgb");
    m_default.led_type = string("ws2801");
    m_default.brightness = 31;
    m_default.xform.r = 1.0;
    m_default.xform.g = 1.0;
    m_default.xform.b = 1.0;
    m_default.white_boost = 1.0;

    m_config.ip = string("127.0.0.1");
    m_config.port = string("5005");

    m_cmd_line_config.config_file = string("/etc/mp/config.json");
    m_cmd_line_config.id = 0;
    m_cmd_line_config.daemonize = false;
    m_cmd_line_config.startup_test = false;
    m_cmd_line_config.ip = string("127.0.0.1");
    m_cmd_line_config.port = string("5005");
    m_cmd_line_config.config_file_set = false;
    m_cmd_line_config.daemonize_set = false;
    m_cmd_line_config.startup_test_set = false;
    m_cmd_line_config.ip_set = false;
    m_cmd_line_config.port_set = false;

    // parse the PACKAGE_VERSION (x.y)
    m_version.major = 0;
    m_version.minor = 0;
    if (sscanf(PACKAGE_VERSION, "%d.%d", &m_version.major, &m_version.minor) != 2) {
        cout << "can't parse PACKAGE_VERSION = " << PACKAGE_VERSION << endl;
    }
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

    if (json_root.isMember(KEY_GLOBAL)) {
        //cout << "m_default.xform.r: " << m_default.xform.r << endl; 
        rc = json_parse_station_values(json_root[KEY_GLOBAL], m_default);
    }

    if (rc == false) {
        cout << "json_parse_station_values() returned false" << endl;
        return false;
    }

    rc = json_parse_station();

    return rc;
}


bool OSCLedConfig::json_parse_linear_xform(Json::Value s, OSCLedConfig::linear_xform &xform)
{
    xform.r = s.get(KEY_IFACE_XFORM_R, m_default.xform.r).asFloat();
    xform.g = s.get(KEY_IFACE_XFORM_G, m_default.xform.g).asFloat();
    xform.b = s.get(KEY_IFACE_XFORM_B, m_default.xform.b).asFloat();

    return true;
}


// this is used to parse both the default station config and the
// actual station config
bool OSCLedConfig::json_parse_station_values(Json::Value s, OSCLedConfig::station_config &config)
{
    // note that "id" cannot be set in the default
    config.ip = s.get(KEY_IP, m_default.ip).asString();
    config.port = s.get(KEY_PORT, m_default.port).asString();
    config.leds_per_bead = s.get(KEY_LEDS_PER_BEAD, m_default.leds_per_bead).asInt();
    config.bead_count = s.get(KEY_BEAD_COUNT, m_default.bead_count).asInt();
    config.bead_base = s.get(KEY_BEAD_BASE, m_default.bead_base).asInt();
    config.daemonize = s.get(KEY_DAEMONIZE, m_default.daemonize).asBool();
    config.startup_test = s.get(KEY_STARTUP_TEST, m_default.startup_test).asBool();
    config.led_type = s.get(KEY_IFACE_LED_TYPE, m_default.led_type).asString();
    config.byte_order = s.get(KEY_IFACE_BYTE_ORDER, m_default.byte_order).asString();
    config.brightness = s.get(KEY_IFACE_BRIGHTNESS, m_default.brightness).asInt();
        
    // parse linear_xform
    config.xform = m_default.xform;
    if (s.isMember(KEY_IFACE_XFORM)) {
        json_parse_linear_xform(s.get(KEY_IFACE_XFORM, ""), config.xform);
    }


    // over-ride with command line arguments
    if (m_cmd_line_config.ip_set)
        config.ip = m_cmd_line_config.ip;

    if (m_cmd_line_config.port_set)
        config.port = m_cmd_line_config.port;

    if (m_cmd_line_config.daemonize_set)
        config.daemonize = m_cmd_line_config.daemonize;
    
    if (m_cmd_line_config.startup_test_set)
        config.startup_test = m_cmd_line_config.startup_test;
    
    if (s.isMember(KEY_IFACE)) {
        // protect against being called more than once by removing all
        // existing elements from the interface vector
        config.interface.clear();

        for (auto i = s[KEY_IFACE].begin(); i != s[KEY_IFACE].end(); i++) {
            shared_ptr<struct interface_config> iface_ptr;
            iface_ptr.reset(new struct interface_config);
            config.interface.push_back(iface_ptr);

            iface_ptr->id = i->get(KEY_IFACE_ID, 0).asInt();
            iface_ptr->iface_class = i->get(KEY_IFACE_CLASS, m_default.iface_class).asString();
            iface_ptr->led_base = i->get(KEY_IFACE_LED_BASE, 0).asInt();
            iface_ptr->led_count = i->get(KEY_IFACE_LED_COUNT, 10).asInt();
            iface_ptr->reversed = i->get(KEY_IFACE_REVERSED, false).asBool();
            iface_ptr->led_type = i->get(KEY_IFACE_LED_TYPE, m_default.led_type).asString();
            iface_ptr->byte_order = i->get(KEY_IFACE_BYTE_ORDER, m_default.byte_order).asString();
            iface_ptr->brightness = i->get(KEY_IFACE_BRIGHTNESS, m_default.brightness).asInt();

            // parse linear_xform
            iface_ptr->xform = config.xform;
            if (i->isMember(KEY_IFACE_XFORM)) {
                json_parse_linear_xform(i->get(KEY_IFACE_XFORM, ""), iface_ptr->xform);
            }
            iface_ptr->led_type = i->get(KEY_IFACE_LED_TYPE, "ws2801").asString();
            iface_ptr->byte_order = i->get(KEY_IFACE_BYTE_ORDER, "rgb").asString();
            iface_ptr->brightness = i->get(KEY_IFACE_BRIGHTNESS, 31).asInt();
            iface_ptr->iface_class = i->get(KEY_IFACE_CLASS, "bead").asString();
            iface_ptr->white_boost = i->get(KEY_IFACE_WHITE_BOOST, m_default.white_boost).asFloat();

            // cout << "iface_class: " << iface_ptr->iface_class << endl;

            // normalize strings to lower case
            transform(iface_ptr->byte_order.begin(), iface_ptr->byte_order.end(), iface_ptr->byte_order.begin(), ::tolower);
            transform(iface_ptr->led_type.begin(), iface_ptr->led_type.end(), iface_ptr->led_type.begin(), ::tolower);
        }
    }

    // cout << "parse_station_config: " << endl;
    // cout << "ip: " << config.ip << endl; 
    // cout << "json_parse_station_values():" << endl;
    // cout << "ip: " << config.ip << endl;
    // cout << "port: " << config.port << endl;
    // cout << "leds_per_bead: " << config.leds_per_bead << endl;
    // cout << "bead_count: " << config.bead_count << endl;
    // cout << "bead_base: " << config.bead_base << endl;
    // cout << "daemonize: " << config.daemonize << endl;
    // cout << "byte_order: " << config.byte_order << endl;
    // cout << "led_type: " << config.led_type << endl;
    // cout << "xform: " << config.xform.r << ", " << config.xform.g << ", " << config.xform.b << endl;

    return true;
}

// find the current station and parse the values
bool OSCLedConfig::json_parse_station()
{
    if (json_root.isMember(KEY_STATION)) {
        json_station = json_root[KEY_STATION];
        for (auto i = json_station.begin(); i != json_station.end(); i++) {
            if (i->get(KEY_ID, 0).asInt() == m_station_id) {
                json_parse_station_values(*i, m_config);
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
            {"test", no_argument, 0, 't'},
            {"help", no_argument, 0, 'h'},
            {0, 0, 0}
        };
        
        c = getopt_long(argc, argv, "vc:i:I:dhp:t", long_options, &option_index);
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
            m_station_id = m_cmd_line_config.id;
            break;
        
        case 'd':
            cout << "damonize = true\n";
            m_cmd_line_config.daemonize = true;
            m_cmd_line_config.daemonize_set = true;
            break;

        case 't':
            cout << "test = true\n";
            m_cmd_line_config.startup_test = true;
            m_cmd_line_config.startup_test_set = true;
            break;

        case 'I':
            m_cmd_line_config.ip = string(optarg);
            m_cmd_line_config.ip_set = true;
            break;

        case 'p':
            m_cmd_line_config.port = string(optarg);
            m_cmd_line_config.port_set = true;
            break;

        case 'v':
            // these macros are defined in config.h
            cout << PACKAGE_STRING << " " << USE_PLATFORM_SERIAL << " " << GIT_HASH << endl;
            exit(0);
            break;

        case 'h':
            cout << PACKAGE_STRING << " " << USE_PLATFORM_SERIAL << " " << GIT_HASH << endl
                 << "usage: " << string(argv[0]) << " -v -c <config.json> -i <ip address> -p <port> -d -h: " << endl
                 << "   --version    version string" << endl
                 << "   --config     json configuration file (" << m_cmd_line_config.config_file << ")" << endl
                 << "   --id         station id (" << m_cmd_line_config.id << ")" << endl
                 << "   --daemonize  detach process from terminal (" << (m_config.daemonize ? "true" : "false") << ")" << endl
                 << "   --ip         ip address to bind to (" << m_config.ip << ")" << endl
                 << "   --port       port to bind to (" << m_config.port << ")" << endl
                 << "   --test       enable startup test sequence" << endl
                 << "   --help       this help message" << endl
                 << endl;
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

