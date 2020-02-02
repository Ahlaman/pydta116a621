from pydta116a621.const import (REGISTER_TYPE_INPUT, REGISTER_TYPE_HOLDING,
                   CONST_MAX_BATCH_READ_SIZE, CONST_MAX_INDOOR_UNIT_COUNT, CONST_CELL_BIT_SIZE,
                   INDOOR_UNIT_ID_INDEX, indoor_unit_id2index, indoor_unit_index2id,
                   CONST_REGISTER_AREA_ADAPTER_STATUS, CONST_REGISTER_AREA_INDOOR_UNIT_CONNECTION_STATE, CONST_REGISTER_AREA_INDOOR_UNIT_COMMUNICATION_STATE,
                   CONST_REGISTER_AREA_INDOOR_UNIT_ABILITY_1, CONST_REGISTER_AREA_INDOOR_UNIT_ABILITY_2,
                   CONST_REGISTER_AREA_INDOOR_UNIT_STATE_1,CONST_REGISTER_AREA_INDOOR_UNIT_STATE_2,CONST_REGISTER_AREA_INDOOR_UNIT_STATE_3,
                   CONST_REGISTER_AREA_INDOOR_UNIT_CONTROL_1,CONST_REGISTER_AREA_INDOOR_UNIT_CONTROL_2,CONST_REGISTER_AREA_INDOOR_UNIT_CONTROL_3,
                   CONST_HVAC_MODE_FAN_ONLY, CONST_HVAC_MODE_HEAT, CONST_HVAC_MODE_COOL, CONST_HVAC_MODE_AUTO, CONST_HVAC_MODE_DRY, CONST_HVAC_MODE_MAPPING,
                   CONST_FAN_MODE_AUTO, CONST_FAN_MODE_LOW,CONST_FAN_MODE_MID_LOW,CONST_FAN_MODE_MIDDLE,CONST_FAN_MODE_MID_HIGH,CONST_FAN_MODE_HIGH,CONST_FAN_MODE_MAPPING,CONST_FAN_MODE_SEG_DEF,
                   CONST_SWING_MODE_AUTO, CONST_SWING_MODE_P1,CONST_SWING_MODE_P2,CONST_SWING_MODE_P3,CONST_SWING_MODE_P4,CONST_SWING_MODE_P5,CONST_SWING_MODE_MAPPING,CONST_SWING_MODE_SEG_DEF,
                   CONST_HVAC_POWER_ON, CONST_HVAC_POWER_OFF, CONST_HVAC_POWER_MAPPING,
                   )
import logging
from pydta116a621.proxy import ModbusDataProxy, IndoorUnitInfoProxy


_LOGGER = logging.getLogger(__name__)

class RegisterAreas:
    def __init__(self, modbus_client):
        self._modbus_client = modbus_client
        self._areas = {
            CONST_REGISTER_AREA_ADAPTER_STATUS: ModbusDataProxy(REGISTER_TYPE_INPUT, 1, 1, self._modbus_client),
            CONST_REGISTER_AREA_INDOOR_UNIT_CONNECTION_STATE: ModbusDataProxy(REGISTER_TYPE_INPUT, 2,
                                                                              int(CONST_MAX_INDOOR_UNIT_COUNT / CONST_CELL_BIT_SIZE),
                                                                              self._modbus_client),
            CONST_REGISTER_AREA_INDOOR_UNIT_COMMUNICATION_STATE: ModbusDataProxy(REGISTER_TYPE_INPUT, 6,
                                                                                 int(CONST_MAX_INDOOR_UNIT_COUNT / CONST_CELL_BIT_SIZE),
                                                                                 self._modbus_client),
            CONST_REGISTER_AREA_INDOOR_UNIT_ABILITY_1: IndoorUnitInfoProxy(REGISTER_TYPE_INPUT, 1001, 3,
                                                                           self._modbus_client),
            CONST_REGISTER_AREA_INDOOR_UNIT_ABILITY_2: IndoorUnitInfoProxy(REGISTER_TYPE_INPUT, 1401, 4,
                                                                           self._modbus_client),
            CONST_REGISTER_AREA_INDOOR_UNIT_STATE_1: IndoorUnitInfoProxy(REGISTER_TYPE_INPUT, 2001, 6,
                                                                         self._modbus_client),
            CONST_REGISTER_AREA_INDOOR_UNIT_STATE_2: IndoorUnitInfoProxy(REGISTER_TYPE_INPUT, 2801, 4,
                                                                         self._modbus_client),
            CONST_REGISTER_AREA_INDOOR_UNIT_STATE_3: IndoorUnitInfoProxy(REGISTER_TYPE_INPUT, 4001, 2,
                                                                         self._modbus_client),
            CONST_REGISTER_AREA_INDOOR_UNIT_CONTROL_1: IndoorUnitInfoProxy(REGISTER_TYPE_HOLDING, 2001, 3,
                                                                           self._modbus_client),
            CONST_REGISTER_AREA_INDOOR_UNIT_CONTROL_2: IndoorUnitInfoProxy(REGISTER_TYPE_HOLDING, 2401, 4,
                                                                           self._modbus_client),
            CONST_REGISTER_AREA_INDOOR_UNIT_CONTROL_3: IndoorUnitInfoProxy(REGISTER_TYPE_HOLDING, 2433, 2,
                                                                           self._modbus_client),
        }

    def get_area(self, area_name):
        return self._areas.get(area_name)

    @property
    def all_areas(self):
        return self._areas

    # fetch all area data
    def update_all(self):
        for proxy in self._areas.values():
            proxy.update_all()


