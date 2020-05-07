import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import switch
from esphome.const import CONF_ID, CONF_INTERLOCK, CONF_PIN_A, CONF_PIN_B, CONF_RESTORE_MODE

from .. import orbit_water_valve_ns

OrbitSwitch = orbit_water_valve_ns.class_('OrbitSwitch', switch.Switch, cg.Component)
OrbitSwitchRestoreMode = orbit_water_valve_ns.enum('OrbitSwitchRestoreMode')

RESTORE_MODES = {
    'RESTORE_DEFAULT_OFF': OrbitSwitchRestoreMode.GPIO_SWITCH_RESTORE_DEFAULT_OFF,
    'RESTORE_DEFAULT_ON': OrbitSwitchRestoreMode.GPIO_SWITCH_RESTORE_DEFAULT_ON,
    'ALWAYS_OFF': OrbitSwitchRestoreMode.GPIO_SWITCH_ALWAYS_OFF,
    'ALWAYS_ON': OrbitSwitchRestoreMode.GPIO_SWITCH_ALWAYS_ON,
}

CONF_INTERLOCK_WAIT_TIME = 'interlock_wait_time'
CONFIG_SCHEMA = switch.SWITCH_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(OrbitSwitch),
    cv.Required(CONF_PIN_A): pins.gpio_output_pin_schema,
    cv.Required(CONF_PIN_B): pins.gpio_output_pin_schema,
    cv.Optional(CONF_RESTORE_MODE, default='RESTORE_DEFAULT_OFF'):
        cv.enum(RESTORE_MODES, upper=True, space='_'),
    cv.Optional(CONF_INTERLOCK): cv.ensure_list(cv.use_id(switch.Switch)),
    cv.Optional(CONF_INTERLOCK_WAIT_TIME, default='0ms'): cv.positive_time_period_milliseconds,
}).extend(cv.COMPONENT_SCHEMA)


def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield switch.register_switch(var, config)

    pin_a = yield cg.gpio_pin_expression(config[CONF_PIN_A])
    pin_b = yield cg.gpio_pin_expression(config[CONF_PIN_B])
    cg.add(var.set_pin_a(pin_a))
    cg.add(var.set_pin_b(pin_b))

    cg.add(var.set_restore_mode(config[CONF_RESTORE_MODE]))

    if CONF_INTERLOCK in config:
        interlock = []
        for it in config[CONF_INTERLOCK]:
            lock = yield cg.get_variable(it)
            interlock.append(lock)
        cg.add(var.set_interlock(interlock))
        cg.add(var.set_interlock_wait_time(config[CONF_INTERLOCK_WAIT_TIME]))
