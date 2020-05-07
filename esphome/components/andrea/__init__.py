import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.const import CONF_BUFFER_SIZE, CONF_DUMP, CONF_FILTER, CONF_ID, CONF_IDLE, \
    CONF_PIN, CONF_TOLERANCE

AUTO_LOAD = []
andrea_ns = cg.esphome_ns.namespace('andrea')
AndreaComponent = andrea_ns.class_('AndreaComponent', cg.Component)

# MULTI_CONF = True
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(AndreaComponent),
    cv.Required(CONF_PIN): cv.All(pins.internal_gpio_input_pin_schema)
}).extend(cv.COMPONENT_SCHEMA)


def to_code(config):
    pin = yield cg.gpio_pin_expression(config[CONF_PIN])
    var = cg.new_Pvariable(config[CONF_ID], pin)
    yield cg.register_component(var, config)
