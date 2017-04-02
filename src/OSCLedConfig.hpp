
#ifndef _OSCLEDCONFIG_HPP_
#define _OSCLEDCONFIG_HPP_

#include <vector>
#include <memory>

#include "json/json.h"

class OSCLedConfig
{
public:
    static OSCLedConfig& getInstance() {
        static OSCLedConfig instance;
        return instance;
    }

    struct cmd_line_config {
        std::string config_file;
        bool config_file_set;
        int id;
        bool id_set;
        bool daemonize;
        bool daemonize_set;
        std::string ip;
        bool ip_set;
        int port;
        bool port_set;
    };

    struct interface_config {
        int id;
        int led_base;
        int led_count;
        bool reversed;
    };

    struct station_config {
        int id;
        std::string ip;
        int port;
        int leds_per_bead;
        int bead_count;
        int bead_base;
        bool daemonize;
        std::vector<std::shared_ptr<struct interface_config>> interface;
    };

    bool getopt(int argc, char * const argv[]);
    bool json_parse();
    bool json_parse_station();
    bool json_parse_station_values(Json::Value s, OSCLedConfig::station_config& config);

    const Json::Value json_interface(const int num);

    Json::Value json_root;
    Json::Value json_station;
    Json::Value json_defaults;

    struct station_config m_default;
    struct station_config m_config;
    struct cmd_line_config m_cmd_line_config;

    const struct station_config& get_station() { return m_config; };

    // string contants used for config file parsing
    static const std::string KEY_DEFAULTS;
    static const std::string KEY_ID;
    static const std::string KEY_STATION;
    static const std::string KEY_IFACE;
    static const std::string KEY_IP;
    static const std::string KEY_PORT;
    static const std::string KEY_LEDS_PER_BEAD;
    static const std::string KEY_BEAD_COUNT;
    static const std::string KEY_BEAD_BASE;
    static const std::string KEY_DAEMONIZE;
    static const std::string KEY_IFACE_ID;
    static const std::string KEY_IFACE_LED_BASE;
    static const std::string KEY_IFACE_LED_COUNT;
    static const std::string KEY_IFACE_REVERSED;
    
private:
    OSCLedConfig();

public:
    OSCLedConfig(OSCLedConfig const&) = delete;
    void operator=(OSCLedConfig const&) = delete;
};


#endif /* _OSCLEDCONFIG_HPP_ */