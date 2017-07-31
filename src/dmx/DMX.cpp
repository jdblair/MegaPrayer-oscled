
#include <iostream>
#include <math.h>
#include <mutex>
#include <stdlib.h>
#include <thread>
#include <unistd.h>

#include <ola/DmxBuffer.h>
#include <ola/Logging.h>
#include <ola/client/StreamingClient.h>

#include "DMX.hpp"

#include "stdlib.h"
#include "stdio.h"
#include "string.h"

using namespace std;

/*
  This module speaks DMX to spotlights via Open Lighting https://wiki.openlighting.org/

 */


void DMX::init() {
    std::cout << "DMX: init()" << std::endl;
    // DMX "universe" to use for sending data.
    // In OLA, this is configured with ola_patch
    universe = 0;

    // turn on OLA logging
    ola::InitLogging(ola::OLA_LOG_WARN, ola::OLA_LOG_STDERR);
    blackout_buffer.Blackout(); // Set all channels to 0

    // Setup the client; this connects to the OLA server
    if (!ola_client.Setup()) {
        std::cerr << "OLA DMX Setup failed" << endl;
        exit(1);
    }

    // Black the lights out
    blackout_buffer.SetChannel(0, 0);
    send_dmx(blackout_buffer);
}

DMX::DMX() : m_led(0,0,0),
	     ola_client((ola::client::StreamingClient::Options())) {}

void dump_buf(unsigned char const *buf, size_t const buf_len) {
	for(int i=0; i<buf_len; i++) {
	    std::cout << (int) buf[i] << " ";
	}
	std::cout << endl;
}

void DMXSerial::send(unsigned char const *buf, size_t const buf_len) {
    std::cout << "DMX: send()" << std::endl;
    // Maximum number of lights in a DMX universe is 512
    unsigned long MAX_DMX_CHANNELS = 512;

    const size_t OSC_VALUES_USED = 5; // red green blue white strobe
    
    if (buf_len % OSC_VALUES_USED != 0) {
	cerr << "DMX: Hey! Incomplete number of bytes per light! (You need " << OSC_VALUES_USED
	     << " bytes per light)." << endl;

	dump_buf(buf, buf_len);
    }

    if (buf_len > OSC_VALUES_USED*MAX_DMX_CHANNELS) {
	cerr << "DMX: Hey! Too many lights for a MX universe. Using first 512" << endl;
	dump_buf(buf, buf_len);
    }

/*
    // ----- begin buffer changed check
    // most of the time there is no change to buf
    // this check avoids calling the update machinery if there has been no change

    if (len > m_last_buf_len) {
        m_last_buf = static_cast<unsigned char *>(realloc(m_last_buf, len));
        m_last_buf_len = len;
    }

    bool buf_changed = false;
    for (int i = 0; i < OSC_VALUES_USED; i++) {
        if (m_last_buf[i] != buf[i]) {
            buf_changed = true;
            break;
        }
    }

    if (buf_changed) {
        memcpy(m_last_buf, buf, len);
    } else {
        return;
    }

    // ----- end buffer changed check
    */

    std::string data(8 * ((buf_len/8) + 1), 0);

    int num_lights = std::min(MAX_DMX_CHANNELS, buf_len / OSC_VALUES_USED);
    ola::DmxBuffer buffer(data);

    for(int light_id = 0; light_id<num_lights; light_id++) {

	int osc_offset = OSC_VALUES_USED * light_id;

	uint8_t red = buf[0 + osc_offset];
	uint8_t green = buf[1 + osc_offset];
	uint8_t blue = buf[2 + osc_offset];
	uint8_t white = buf[3 + osc_offset];
	uint8_t strobe = buf[4 + osc_offset];
   
	cout << "DMX: light=" << (uint32_t)light_id
	     << " r=" << (uint32_t)red 
	     << " g=" << (uint32_t)green 
	     << " b=" << (uint32_t)blue 
	     << " w=" << (uint32_t)white
	     << " strobe=" << (uint32_t)strobe
	     << endl; 

	int channel_offset = light_id * DMX::CHANNELS_PER_LIGHT;
	cout << "Red Channel: " << (uint32_t)(DMX::RED + channel_offset)
	     << " Value: " << (uint32_t)red << endl;

	buffer.SetChannel(0 + channel_offset, 255);

	buffer.SetChannel(DMX::RED + channel_offset, red);
	buffer.SetChannel(DMX::GREEN + channel_offset, green);
	buffer.SetChannel(DMX::BLUE + channel_offset, blue);
	buffer.SetChannel(DMX::WHITE + channel_offset, white);
	buffer.SetChannel(DMX::STROBE + channel_offset, strobe);
    }

    m_dmx.send_dmx(buffer);

}

void DMX::send_dmx(ola::DmxBuffer& buffer) {

    if (!ola_client.SendDmx(universe, buffer)) {
	cerr << "Send DMX failed" << endl;
	exit(1);
    }
}

