#pragma once

#include "esphome/core/component.h"
#include "esphome/core/log.h"

#define RECEIVER_PIN 4  // any intterupt able pin
#define TRANSMITTER_PIN -1

// LOG Levels:
//  - ERROR: ESP_LOGE
//  - WARNING: ESP_LOGW
//  - INFO: ESP_LOGI
//  - DEBUG: ESP_LOGD
//  - VERBOSE: ESP_LOGV
//  - VERY_VERBOSE: ESP_LOGVV

#include <ESPiLight.h>

namespace esphome {
namespace andrea {

// callback function. It is called on successfully received and parsed rc signal
void rfRawCallback(const uint16_t* codes, size_t length) {
  // print pulse lengths
  ESP_LOGD("andrea","RAW signal: ");
  for (unsigned int i = 0; i < length; i++) {
    ESP_LOGD("andrea","%x",codes[i]);
    ESP_LOGD("andrea"," ");
  }
}
  
// callback function. It is called on successfully received and parsed rc signal
void rfCallback(const String &protocol, const String &message, int status,
                size_t repeats, const String &deviceID) {
  ESP_LOGD("andrea","RF signal arrived [%s][%d] (%d) %s",
            protocol.c_str(), // protocoll used to parse
            deviceID.c_str(),  // value of id key in json message
            status,  // status of message, depending on repeat, either:
                         // FIRST   - first message of this protocoll within the
                         //           last 0.5 s
                         // INVALID - message repeat is not equal to the
                         //           previous message
                         // VALID   - message is equal to the previous message
                         // KNOWN   - repeat of a already valid message  
            message.c_str());  // message in json format
  
  // check if message is valid and process it
  if (status == VALID) {
    ESP_LOGD("andrea","Valid message: [%s] %s", protocol.c_str(), message.c_str());
  }
}

class AndreaComponent :  Component {
    ESPiLight *ep = NULL;
 public:
  AndreaComponent(GPIOPin *pin) {
        ESP_LOGD("andrea", "configure espilight");
        ep = new ESPiLight(TRANSMITTER_PIN);
        ep->initReceiver(pin->get_pin());
        ep->setCallback(rfCallback);
  }

  void loop() {
      if(ep) ep->loop();
      delay(2);
  }
};



}  // namespace andrea
}  // namespace esphome




