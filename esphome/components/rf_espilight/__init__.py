import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import remote_base
from esphome.const import CONF_BUFFER_SIZE, CONF_DUMP, CONF_FILTER, CONF_ID, CONF_IDLE, \
    CONF_PIN, CONF_TOLERANCE

AUTO_LOAD = ['remote_base']
rf_espilight_ns = cg.esphome_ns.namespace('rf_espilight')
RFESPiLightComponent = rf_espilight_ns.class_('RFESPiLightComponent',
                                                    remote_base.RemoteReceiverBase,
                                                    cg.Component)

MULTI_CONF = True
CONFIG_SCHEMA = remote_base.validate_triggers(cv.Schema({
    cv.GenerateID(): cv.declare_id(RFESPiLightComponent),
    cv.Required(CONF_PIN): cv.All(pins.internal_gpio_input_pin_schema,
                                  pins.validate_has_interrupt),
    cv.Optional(CONF_DUMP, default=[]): remote_base.validate_dumpers,
    cv.Optional(CONF_TOLERANCE, default=25): cv.All(cv.percentage_int, cv.Range(min=0)),
    cv.SplitDefault(CONF_BUFFER_SIZE, esp32='10000b', esp8266='1000b'): cv.validate_bytes,
    cv.Optional(CONF_FILTER, default='50us'): cv.positive_time_period_microseconds,
    cv.Optional(CONF_IDLE, default='10ms'): cv.positive_time_period_microseconds,
}).extend(cv.COMPONENT_SCHEMA))


def to_code(config):
    pin = yield cg.gpio_pin_expression(config[CONF_PIN])
    var = cg.new_Pvariable(config[CONF_ID], pin)

    yield remote_base.build_dumpers(config[CONF_DUMP])
    yield remote_base.build_triggers(config)
    yield cg.register_component(var, config)

    cg.add(var.set_tolerance(config[CONF_TOLERANCE]))
    cg.add(var.set_buffer_size(config[CONF_BUFFER_SIZE]))
    cg.add(var.set_filter_us(config[CONF_FILTER]))
    cg.add(var.set_idle_us(config[CONF_IDLE]))
