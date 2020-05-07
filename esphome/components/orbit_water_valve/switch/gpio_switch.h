#pragma once

#include "esphome/core/component.h"
#include "esphome/components/switch/switch.h"

namespace esphome {
namespace orbit_water_valve {

enum OrbitSwitchRestoreMode {
  GPIO_SWITCH_RESTORE_DEFAULT_OFF,
  GPIO_SWITCH_RESTORE_DEFAULT_ON,
  GPIO_SWITCH_ALWAYS_OFF,
  GPIO_SWITCH_ALWAYS_ON,
};

class OrbitSwitch : public switch_::Switch, public Component {
 public:
  void set_pin_a(GPIOPin *pin) { pin_a = pin; }
  void set_pin_b(GPIOPin *pin) { pin_b = pin; }

  void set_restore_mode(OrbitSwitchRestoreMode restore_mode);

  // ========== INTERNAL METHODS ==========
  // (In most use cases you won't need these)
  float get_setup_priority() const override;

  void setup() override;
  void dump_config() override;
  void set_interlock(const std::vector<Switch *> &interlock);
  void set_interlock_wait_time(uint32_t interlock_wait_time) { interlock_wait_time_ = interlock_wait_time; }

 protected:
  void write_state(bool state) override;

  GPIOPin *pin_a;
  GPIOPin *pin_b;
  OrbitSwitchRestoreMode restore_mode_{GPIO_SWITCH_RESTORE_DEFAULT_OFF};
  std::vector<Switch *> interlock_;
  uint32_t interlock_wait_time_{0};
};

}  // namespace gpio
}  // namespace esphome
