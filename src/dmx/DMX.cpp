
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

void DMXSerial::send(unsigned char const *buf, size_t const len) {
    std::cout << "DMX: send()" << std::endl;
    size_t buf_len(len);
    const size_t MAX_VALUES_USED = 4; // r g b w

    if (len > MAX_VALUES_USED) {
	cerr << "Hey! More than one light specified for the cross spotlights, but I'm only using the first one !" << endl;
	for(int i =0; i<len; i++) {
	    std::cout << (int) buf[i] << " ";
	}
	std::cout << endl;
    }


    if (len < MAX_VALUES_USED) {
	cerr << "Hey! I need at least " << MAX_VALUES_USED << " data bytes, but I only got " << len << " bytes!! Exiting DMX::send." << endl;
	return;
    }

    // ----- begin buffer changed check
    // most of the time there is no change to buf
    // this check avoids calling the update machinery if there has been no change

    if (len > m_last_buf_len) {
        m_last_buf = static_cast<unsigned char *>(realloc(m_last_buf, len));
        m_last_buf_len = len;
    }

    bool buf_changed = false;
    for (int i = 0; i < MAX_VALUES_USED; i++) {
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

    uint8_t red = buf[0];
    uint8_t green = buf[1];
    uint8_t blue = buf[2];
    uint8_t white = buf[3];

    std::string data(16, 0);
   
    cout << "DMX: light=" << m_light_id 
	 << " r=" << (uint32_t)red 
	 << " g=" << (uint32_t)green 
	 << " b=" << (uint32_t)blue 
	 << " w=" << (uint32_t)white
	 << endl; 

    ola::DmxBuffer buffer(data);

    buffer.SetChannel(0, 255);
    buffer.SetChannel(8, 255);

    int channel_offset = m_light_id*DMX::CHANNELS_PER_LIGHT;
    cout << "Channel: " << DMX::RED + channel_offset
	 << " Value: " << (uint32_t)red << endl;

    buffer.SetChannel(DMX::RED + channel_offset, red);
    buffer.SetChannel(DMX::GREEN + channel_offset, green);
    buffer.SetChannel(DMX::BLUE + channel_offset, blue);
    buffer.SetChannel(DMX::WHITE + channel_offset, white);

    m_dmx.send_dmx(buffer);

}

void DMX::send_dmx(ola::DmxBuffer& buffer) {

    if (!ola_client.SendDmx(universe, buffer)) {
	cerr << "Send DMX failed" << endl;
	exit(1);
    }
}

